from dataclasses import dataclass

import betterproto


class RpcApiId(betterproto.Enum):
    UNKNOWN_API_ID = 0
    GET_ROBOT_STATUS = 1000
    GET_ROBOT_PARAMS = 1001
    SET_ROBOT_PARAMS = 1002
    ROBOT_MOVE = 1003
    ROBOT_CHANGE_MODE = 1004
    ROBOT_ROTATE_HEAD = 1005
    ROBOT_KICK = 1006
    ROBOT_STAND_STILL = 1007
    ROBOT_STEP_ON_SPOT = 1008
    SET_ROBOT_INFO = 1009
    ROBOT_RESTART = 1010
    PROCESS_RESTART = 1011
    ROBOT_WAVE_HAND = 1012
    ROBOT_ZERO_POSE_SET = 1013
    ROBOT_ROTATE_HEAD_WITH_POSITION = 1014
    ROBOT_LIE_DOWN = 1015
    ROBOT_GET_UP = 1016
    ROBOT_MOVE_HAND_END_EFFECTOR_WITH_AUX = 1017
    ROBOT_MOVE_HAND_END_EFFECTOR = 1018
    ROBOT_CONTROL_GRIPPER = 1019
    GET_FRAME_TRANSFORM = 1020
    ROBOT_SWITCH_HAND_END_EFFECTOR_CONTROL_MODE = 1021
    ROBOT_SHAKE_HAND = 1022
    ROBOT_DANCE = 1023
    UPDATE_PASSWORD = 1024
    AUTH_USER = 1025
    AUTH_GET_SETTINGS = 1026
    ROBOT_COMMON_CHANNEL = 1027
    ROBOT_WHOLE_BODY_DANCE = 1028
    ROBOT_STOP_DANCE = 1029
    SWITCH_AP_SERVICE = 1030
    ROBOT_SNIFFING = 1031


class OperationStatus(betterproto.Enum):
    UNKNOWN = 0
    SUCCESS = 1
    FAIL = 2


class RobotMode(betterproto.Enum):
    DAMPING = 0
    PREPARE = 1
    WALKING = 2
    CUSTOM = 3
    SOCCER = 4


@dataclass
class RpcRequest(betterproto.Message):
    api_id: RpcApiId = betterproto.enum_field(1)
    uuid: str = betterproto.string_field(2)
    payload: bytes = betterproto.bytes_field(3)
    token: str = betterproto.string_field(4)
    client_version: int = betterproto.int32_field(5)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.api_id = RpcApiId(self.api_id)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RpcResponse(betterproto.Message):
    api_id: RpcApiId = betterproto.enum_field(1)
    uuid: str = betterproto.string_field(2)
    payload: bytes = betterproto.bytes_field(3)
    operation_status: OperationStatus = betterproto.enum_field(4)
    server_version: int = betterproto.int32_field(5)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.api_id = RpcApiId(self.api_id)
        self.operation_status = OperationStatus(self.operation_status)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotInfo(betterproto.Message):
    serial_number: str = betterproto.string_field(1)
    name: str = betterproto.string_field(2)
    version: str = betterproto.string_field(3)
    model: str = betterproto.string_field(4)
    delivery_time: int = betterproto.int64_field(5)
    ip: str = betterproto.string_field(6)
    rpc_port: int = betterproto.int32_field(7)
    websocket_port: int = betterproto.int32_field(8)


@dataclass
class GetRobotStatusRequest(betterproto.Message):
    serial_id: str = betterproto.string_field(1)


@dataclass
class GetRobotStatusResponse(betterproto.Message):
    mode: RobotMode = betterproto.enum_field(1)
    robot_info: RobotInfo = betterproto.message_field(2)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.mode = RobotMode(self.mode)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotMoveRequest(betterproto.Message):
    vx: float = betterproto.float_field(1)
    vy: float = betterproto.float_field(2)
    vyaw: float = betterproto.float_field(3)


@dataclass
class RobotChangeModeRequest(betterproto.Message):
    mode: RobotMode = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.mode = RobotMode(self.mode)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotRotateHeadRequest(betterproto.Message):
    pitch: float = betterproto.float_field(1)
    yaw: float = betterproto.float_field(2)
