import asyncio
import uuid
from collections.abc import Callable
from typing import Any

import grpc
import websockets

from booster_rpc.proto import (
    Frame,
    DanceId,
    DanceRequest,
    GetFrameTransformRequest,
    GetFrameTransformResponse,
    GetRobotStatusResponse,
    GetUpWithModeRequest,
    HandAction,
    HandIndex,
    OperationStatus,
    Posture,
    RobotChangeModeRequest,
    RobotHandshakeRequest,
    RobotMode,
    RobotMoveRequest,
    RobotRotateHeadRequest,
    MoveHandEndEffectorRequest,
    VisualKickRequest,
    VisualKickVersion,
    WholeBodyDanceId,
    WholeBodyDanceRequest,
    RobotWaveHandRequest,
    RpcApiId,
    RpcRequest,
    RpcResponse,
)

DEFAULT_IP = "10.0.0.185"
DEFAULT_WS_PORT = 51111
DEFAULT_GRPC_PORT = 50051

JPEG_SOI = b"\xff\xd8"
JPEG_EOI = b"\xff\xd9"


class BoosterConnection:
    """Client for communicating with a Booster K1 robot via gRPC and WebSocket."""

    def __init__(self, ip: str = DEFAULT_IP, ws_port: int = DEFAULT_WS_PORT, grpc_port: int = DEFAULT_GRPC_PORT):
        self.ip = ip
        self.ws_port = ws_port
        self.grpc_port = grpc_port
        self.channel = grpc.insecure_channel(f"{ip}:{grpc_port}")
        self._robot_request = self.channel.unary_unary(
            "/booster.proto.rpc.RobotGrpc/RobotRequest",
            request_serializer=bytes,
            response_deserializer=RpcResponse.FromString,
        )

    # -- gRPC RPC --

    def call(self, api_id: RpcApiId, payload: bytes = b""):
        """Send a raw RPC request and return the response envelope.

        Args:
            api_id: The RpcApiId enum value identifying the remote procedure.
            payload: Serialised protobuf bytes for the request body.

        Returns:
            The RpcResponse from the robot.

        Raises:
            RuntimeError: If the robot returns OPERATION_FAIL.
        """
        req = RpcRequest(api_id=api_id, uuid=str(uuid.uuid4()), payload=payload)
        resp = self._robot_request(req, timeout=5)
        if resp.operation_status == OperationStatus.FAIL:
            raise RuntimeError(f"Robot returned OPERATION_FAIL for {api_id}")
        return resp

    def change_mode(self, mode: RobotMode):
        """Request a robot mode transition."""
        return self.call(RpcApiId.ROBOT_CHANGE_MODE, bytes(RobotChangeModeRequest(mode=mode)))

    def get_mode(self) -> RobotMode:
        """Return the current robot mode.

        The documented GetMode RPC is exposed here through the existing robot status
        call, which already returns the current mode.
        """
        resp = self.call(RpcApiId.GET_ROBOT_STATUS)
        status = GetRobotStatusResponse().parse(resp.payload)
        return status.mode

    def move(self, vx: float = 0.0, vy: float = 0.0, vyaw: float = 0.0):
        """Send a base velocity command in the robot's base frame."""
        return self.call(RpcApiId.ROBOT_MOVE, bytes(RobotMoveRequest(vx=vx, vy=vy, vyaw=vyaw)))

    def rotate_head(self, pitch: float, yaw: float):
        """Send a head rotation command in radians."""
        return self.call(RpcApiId.ROBOT_ROTATE_HEAD, bytes(RobotRotateHeadRequest(pitch=pitch, yaw=yaw)))

    def move_hand_end_effector(self, target_posture: Posture, time_millis: int, hand_index: HandIndex):
        """Move a hand end effector to a target posture over a duration."""
        payload = MoveHandEndEffectorRequest(
            target_posture=target_posture,
            time_millis=time_millis,
            hand_index=hand_index,
        )
        return self.call(RpcApiId.ROBOT_MOVE_HAND_END_EFFECTOR, bytes(payload))

    def get_up_with_mode(self, mode: RobotMode):
        """Stand the robot up and enter the requested motion mode."""
        return self.call(RpcApiId.ROBOT_GET_UP, bytes(GetUpWithModeRequest(mode=mode)))

    def reset_odometry(self):
        """Reset the robot's gait odometry."""
        return self.call(RpcApiId.ROBOT_ZERO_POSE_SET)

    def dance(self, dance_id: DanceId):
        """Start a standard dance motion."""
        return self.call(RpcApiId.ROBOT_DANCE, bytes(DanceRequest(dance_id=dance_id)))

    def whole_body_dance(self, dance_id: WholeBodyDanceId):
        """Start a whole-body dance motion."""
        return self.call(RpcApiId.ROBOT_WHOLE_BODY_DANCE, bytes(WholeBodyDanceRequest(dance_id=dance_id)))

    def stop_dance(self):
        """Stop the current dance motion."""
        return self.call(RpcApiId.ROBOT_STOP_DANCE)

    def visual_kick(self, start: bool, version: VisualKickVersion):
        """Start or stop the visual kick behavior."""
        return self.call(RpcApiId.ROBOT_KICK, bytes(VisualKickRequest(start=start, version=version)))

    def wave_hand(self, action: HandAction):
        """Start or stop the waving gesture."""
        return self.call(RpcApiId.ROBOT_WAVE_HAND, bytes(RobotWaveHandRequest(action=action)))

    def handshake(self, action: HandAction):
        """Start or stop the handshake gesture."""
        return self.call(RpcApiId.ROBOT_SHAKE_HAND, bytes(RobotHandshakeRequest(action=action)))

    def get_frame_transform(self, src: Frame, dst: Frame) -> GetFrameTransformResponse:
        """Return the transform between two robot frames."""
        resp = self.call(RpcApiId.GET_FRAME_TRANSFORM, bytes(GetFrameTransformRequest(src=src, dst=dst)))
        return GetFrameTransformResponse().parse(resp.payload)

    # -- WebSocket video stream --

    async def stream_video(self, callback: Callable[[bytes], Any]):
        """Stream JPEG frames from the robot's camera over WebSocket.

        Connects to ws://{ip}:{ws_port}, extracts JPEG frames from
        the binary stream, and passes each frame to ``callback``.

        Args:
            callback: Called with raw JPEG bytes for each frame.
                      May be a coroutine or a plain function.
        """
        uri = f"ws://{self.ip}:{self.ws_port}"
        async with websockets.connect(uri, open_timeout=5) as ws:
            while True:
                data = await ws.recv()
                if not isinstance(data, bytes):
                    continue
                start = data.find(JPEG_SOI)
                end = data.rfind(JPEG_EOI)
                if start >= 0 and end >= 0:
                    frame = data[start : end + 2]
                    result = callback(frame)
                    if asyncio.iscoroutine(result):
                        await result

    # -- lifecycle --

    def close(self):
        """Close the underlying gRPC channel."""
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
