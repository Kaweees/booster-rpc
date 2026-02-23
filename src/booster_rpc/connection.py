import uuid

import grpc

from booster_rpc.proto import OperationStatus, RpcRequest, RpcResponse

DEFAULT_IP = "10.0.0.185"
DEFAULT_WS_PORT = 51111
DEFAULT_GRPC_PORT = 50051


class BoosterRPCConnection:
    """Base class for communicating with a Booster robot via gRPC RPC."""

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

    def _call(self, api_id: int, payload: bytes = b""):
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

    def close(self):
        """Close the underlying gRPC channel."""
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
