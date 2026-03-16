import asyncio
import uuid
from collections.abc import Callable

import grpc
import websockets

from booster_rpc.proto import OperationStatus, RpcRequest, RpcResponse

DEFAULT_IP = "10.0.0.15"
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

    def call(self, api_id: int, payload: bytes = b""):
        """Send an RPC request and return the response.

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

    # -- WebSocket video stream --

    async def stream_video(self, callback: Callable[[bytes], None]):
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
