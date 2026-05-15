from dataclasses import dataclass

import betterproto


class RpcApiId(betterproto.Enum):
    """Known RPC identifiers exposed by the Booster robot service."""

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
    """Outcome codes returned by the robot RPC gateway."""

    UNKNOWN = 0
    SUCCESS = 1
    FAIL = 2


class RobotMode(betterproto.Enum):
    """Robot motion modes reported by the status RPCs."""

    DAMPING = 0
    PREPARE = 1
    WALKING = 2
    CUSTOM = 3
    SOCCER = 4


class HandAction(betterproto.Enum):
    """Open/close action for hand gestures."""

    OPEN = 0
    CLOSE = 1


class HandIndex(betterproto.Enum):
    """Identifies the left or right hand."""

    LEFT = 0
    RIGHT = 1


class DanceId(betterproto.Enum):
    """Standard dance identifiers supported by the motion service."""

    NEW_YEAR = 0
    NEZHA = 1
    TOWARDS_FUTURE = 2
    POGBA_GESTURE = 3
    ULTRAMAN_GESTURE = 4
    CHINESE_GREETING_GESTURE = 5
    CHEERING_GESTURE = 6
    MANEKI_GESTURE = 7
    STOP = 1000


class WholeBodyDanceId(betterproto.Enum):
    """Whole-body dance identifiers supported by the motion service."""

    ARBIC_DANCE = 0
    MICHAEL_DANCE_1 = 1
    MICHAEL_DANCE_2 = 2
    MICHAEL_DANCE_3 = 3
    MOON_WALK = 4
    BOXING_STYLE_KICK = 5
    ROUNDHOUSE_KICK = 6
    SHAN_HE_GU_REN_DANCE = 7
    GAI_GE_CHUN_FENG_DANCE = 8


class GaitType(betterproto.Enum):
    """Gait presets exposed by the motion-control interface."""

    WHOLE_BODY_HUMANLIKE_GAIT = 0
    HALF_BODY_HUMANLIKE_GAIT = 1
    HALF_BODY_HUMANLIKE_GAIT_V2 = 2


class VisualKickVersion(betterproto.Enum):
    """Visual-kick behavior variants."""

    V1 = 0
    V2 = 1


class Frame(betterproto.Enum):
    """Reference frames accepted by the transform RPC."""

    BODY = 0
    HEAD = 1
    LEFT_HAND = 2
    RIGHT_HAND = 3
    LEFT_FOOT = 4
    RIGHT_FOOT = 5


@dataclass
class RpcRequest(betterproto.Message):
    """Envelope sent to the Booster gRPC gateway."""

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
    """Envelope returned by the Booster gRPC gateway."""

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
    """Static robot identity and endpoint metadata."""

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
    """Request the robot status for a specific serial number."""

    serial_id: str = betterproto.string_field(1)


@dataclass
class GetRobotStatusResponse(betterproto.Message):
    """Current robot mode and identity payload."""

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
class GetModeResponse(betterproto.Message):
    """Standalone mode response used by the documented GetMode RPC."""

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
class RobotMoveRequest(betterproto.Message):
    """Base velocity command in meters per second and radians per second."""

    vx: float = betterproto.float_field(1)
    vy: float = betterproto.float_field(2)
    vyaw: float = betterproto.float_field(3)


@dataclass
class Posture(betterproto.Message):
    """Target posture passed to the hand end-effector RPC."""

    position: list[float] = betterproto.float_field(1)
    orientation: list[float] = betterproto.float_field(2)


@dataclass
class MoveHandEndEffectorRequest(betterproto.Message):
    """Request a hand end-effector motion to a target posture."""

    target_posture: Posture = betterproto.message_field(1)
    time_millis: int = betterproto.int32_field(2)
    hand_index: HandIndex = betterproto.enum_field(3)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.hand_index = HandIndex(self.hand_index)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotWaveHandRequest(betterproto.Message):
    """Start or stop a hand-waving gesture."""

    action: HandAction = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.action = HandAction(self.action)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotHandshakeRequest(betterproto.Message):
    """Start or stop a handshake gesture."""

    action: HandAction = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.action = HandAction(self.action)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class RobotChangeModeRequest(betterproto.Message):
    """Request a robot motion-mode transition."""

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
    """Head pitch and yaw command in radians."""

    pitch: float = betterproto.float_field(1)
    yaw: float = betterproto.float_field(2)


@dataclass
class UpperBodyCustomControlRequest(betterproto.Message):
    """Enable or disable upper-body custom control."""

    start: bool = betterproto.bool_field(1)


@dataclass
class GetUpWithModeRequest(betterproto.Message):
    """Stand the robot up and enter a specific motion mode."""

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
class DanceRequest(betterproto.Message):
    """Standard dance selection request."""

    dance_id: DanceId = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.dance_id = DanceId(self.dance_id)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class WholeBodyDanceRequest(betterproto.Message):
    """Whole-body dance selection request."""

    dance_id: WholeBodyDanceId = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.dance_id = WholeBodyDanceId(self.dance_id)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class VisualKickRequest(betterproto.Message):
    """Start or stop the visual-kick behavior."""

    start: bool = betterproto.bool_field(1)
    version: VisualKickVersion = betterproto.enum_field(2)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.version = VisualKickVersion(self.version)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class SwitchGaitRequest(betterproto.Message):
    """Select the active gait preset."""

    gait_type: GaitType = betterproto.enum_field(1)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.gait_type = GaitType(self.gait_type)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class GetFrameTransformRequest(betterproto.Message):
    """Request the transform between two robot frames."""

    src: Frame = betterproto.enum_field(1)
    dst: Frame = betterproto.enum_field(2)

    def __post_init__(self):
        super().__post_init__()
        self._convert_enums()

    def _convert_enums(self):
        self.src = Frame(self.src)
        self.dst = Frame(self.dst)

    def parse(self, data: bytes):
        super().parse(data)
        self._convert_enums()
        return self


@dataclass
class Transform(betterproto.Message):
    """Flattened 4x4 transform matrix stored row-major."""

    matrix: list[float] = betterproto.float_field(1)


@dataclass
class GetFrameTransformResponse(betterproto.Message):
    """Response wrapper containing the requested frame transform."""

    transform: Transform = betterproto.message_field(1)
