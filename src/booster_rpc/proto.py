from dataclasses import dataclass

import betterproto2


class RpcApiId(betterproto2.Enum):
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


class OperationStatus(betterproto2.Enum):
    """Outcome codes returned by the robot RPC gateway."""

    UNKNOWN = 0
    SUCCESS = 1
    FAIL = 2


class RobotMode(betterproto2.Enum):
    """Robot motion modes reported by the status RPCs."""

    DAMPING = 0
    PREPARE = 1
    WALKING = 2
    CUSTOM = 3
    SOCCER = 4


class HandAction(betterproto2.Enum):
    """Open/close action for hand gestures."""

    OPEN = 0
    CLOSE = 1


class HandIndex(betterproto2.Enum):
    """Identifies the left or right hand."""

    LEFT = 0
    RIGHT = 1


class DanceId(betterproto2.Enum):
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


class WholeBodyDanceId(betterproto2.Enum):
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


class GaitType(betterproto2.Enum):
    """Gait presets exposed by the motion-control interface."""

    WHOLE_BODY_HUMANLIKE_GAIT = 0
    HALF_BODY_HUMANLIKE_GAIT = 1
    HALF_BODY_HUMANLIKE_GAIT_V2 = 2


class VisualKickVersion(betterproto2.Enum):
    """Visual-kick behavior variants."""

    V1 = 0
    V2 = 1


class Frame(betterproto2.Enum):
    """Reference frames accepted by the transform RPC."""

    BODY = 0
    HEAD = 1
    LEFT_HAND = 2
    RIGHT_HAND = 3
    LEFT_FOOT = 4
    RIGHT_FOOT = 5


@dataclass
class RpcRequest(betterproto2.Message):
    """Envelope sent to the Booster gRPC gateway."""

    api_id: RpcApiId = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RpcApiId.UNKNOWN_API_ID)
    uuid: str = betterproto2.field(2, betterproto2.TYPE_STRING)
    payload: bytes = betterproto2.field(3, betterproto2.TYPE_BYTES)
    token: str = betterproto2.field(4, betterproto2.TYPE_STRING)
    client_version: int = betterproto2.field(5, betterproto2.TYPE_INT32)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.api_id = RpcApiId(self.api_id)


@dataclass
class RpcResponse(betterproto2.Message):
    """Envelope returned by the Booster gRPC gateway."""

    api_id: RpcApiId = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RpcApiId.UNKNOWN_API_ID)
    uuid: str = betterproto2.field(2, betterproto2.TYPE_STRING)
    payload: bytes = betterproto2.field(3, betterproto2.TYPE_BYTES)
    operation_status: OperationStatus = betterproto2.field(
        4, betterproto2.TYPE_ENUM, default_factory=lambda: OperationStatus.UNKNOWN
    )
    server_version: int = betterproto2.field(5, betterproto2.TYPE_INT32)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.api_id = RpcApiId(self.api_id)
        self.operation_status = OperationStatus(self.operation_status)


@dataclass
class RobotInfo(betterproto2.Message):
    """Static robot identity and endpoint metadata."""

    serial_number: str = betterproto2.field(1, betterproto2.TYPE_STRING)
    name: str = betterproto2.field(2, betterproto2.TYPE_STRING)
    version: str = betterproto2.field(3, betterproto2.TYPE_STRING)
    model: str = betterproto2.field(4, betterproto2.TYPE_STRING)
    delivery_time: int = betterproto2.field(5, betterproto2.TYPE_INT64)
    ip: str = betterproto2.field(6, betterproto2.TYPE_STRING)
    rpc_port: int = betterproto2.field(7, betterproto2.TYPE_INT32)
    websocket_port: int = betterproto2.field(8, betterproto2.TYPE_INT32)


@dataclass
class GetRobotStatusRequest(betterproto2.Message):
    """Request the robot status for a specific serial number."""

    serial_id: str = betterproto2.field(1, betterproto2.TYPE_STRING)


@dataclass
class GetRobotStatusResponse(betterproto2.Message):
    """Current robot mode and identity payload."""

    mode: RobotMode = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RobotMode.DAMPING)
    robot_info: RobotInfo | None = betterproto2.field(2, betterproto2.TYPE_MESSAGE, optional=True)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.mode = RobotMode(self.mode)


@dataclass
class GetModeResponse(betterproto2.Message):
    """Standalone mode response used by the documented GetMode RPC."""

    mode: RobotMode = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RobotMode.DAMPING)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.mode = RobotMode(self.mode)


@dataclass
class RobotMoveRequest(betterproto2.Message):
    """Base velocity command in meters per second and radians per second."""

    vx: float = betterproto2.field(1, betterproto2.TYPE_FLOAT)
    vy: float = betterproto2.field(2, betterproto2.TYPE_FLOAT)
    vyaw: float = betterproto2.field(3, betterproto2.TYPE_FLOAT)


@dataclass
class Posture(betterproto2.Message):
    """Target posture passed to the hand end-effector RPC."""

    position: list[float] = betterproto2.field(1, betterproto2.TYPE_FLOAT, repeated=True)
    orientation: list[float] = betterproto2.field(2, betterproto2.TYPE_FLOAT, repeated=True)


@dataclass
class MoveHandEndEffectorRequest(betterproto2.Message):
    """Request a hand end-effector motion to a target posture."""

    target_posture: Posture | None = betterproto2.field(1, betterproto2.TYPE_MESSAGE, optional=True)
    time_millis: int = betterproto2.field(2, betterproto2.TYPE_INT32)
    hand_index: HandIndex = betterproto2.field(3, betterproto2.TYPE_ENUM, default_factory=lambda: HandIndex.LEFT)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.hand_index = HandIndex(self.hand_index)


@dataclass
class RobotWaveHandRequest(betterproto2.Message):
    """Start or stop a hand-waving gesture."""

    action: HandAction = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: HandAction.OPEN)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.action = HandAction(self.action)


@dataclass
class RobotHandshakeRequest(betterproto2.Message):
    """Start or stop a handshake gesture."""

    action: HandAction = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: HandAction.OPEN)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.action = HandAction(self.action)


@dataclass
class RobotChangeModeRequest(betterproto2.Message):
    """Request a robot motion-mode transition."""

    mode: RobotMode = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RobotMode.DAMPING)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.mode = RobotMode(self.mode)


@dataclass
class RobotRotateHeadRequest(betterproto2.Message):
    """Head pitch and yaw command in radians."""

    pitch: float = betterproto2.field(1, betterproto2.TYPE_FLOAT)
    yaw: float = betterproto2.field(2, betterproto2.TYPE_FLOAT)


@dataclass
class UpperBodyCustomControlRequest(betterproto2.Message):
    """Enable or disable upper-body custom control."""

    start: bool = betterproto2.field(1, betterproto2.TYPE_BOOL)


@dataclass
class GetUpWithModeRequest(betterproto2.Message):
    """Stand the robot up and enter a specific motion mode."""

    mode: RobotMode = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: RobotMode.DAMPING)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.mode = RobotMode(self.mode)


@dataclass
class DanceRequest(betterproto2.Message):
    """Standard dance selection request."""

    dance_id: DanceId = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: DanceId.NEW_YEAR)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.dance_id = DanceId(self.dance_id)


@dataclass
class WholeBodyDanceRequest(betterproto2.Message):
    """Whole-body dance selection request."""

    dance_id: WholeBodyDanceId = betterproto2.field(
        1, betterproto2.TYPE_ENUM, default_factory=lambda: WholeBodyDanceId.ARBIC_DANCE
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.dance_id = WholeBodyDanceId(self.dance_id)


@dataclass
class VisualKickRequest(betterproto2.Message):
    """Start or stop the visual-kick behavior."""

    start: bool = betterproto2.field(1, betterproto2.TYPE_BOOL)
    version: VisualKickVersion = betterproto2.field(
        2, betterproto2.TYPE_ENUM, default_factory=lambda: VisualKickVersion.V1
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.version = VisualKickVersion(self.version)


@dataclass
class SwitchGaitRequest(betterproto2.Message):
    """Select the active gait preset."""

    gait_type: GaitType = betterproto2.field(
        1, betterproto2.TYPE_ENUM, default_factory=lambda: GaitType.WHOLE_BODY_HUMANLIKE_GAIT
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        self.gait_type = GaitType(self.gait_type)


@dataclass
class GetFrameTransformRequest(betterproto2.Message):
    """Request the transform between two robot frames."""

    src: Frame = betterproto2.field(1, betterproto2.TYPE_ENUM, default_factory=lambda: Frame.BODY)
    dst: Frame = betterproto2.field(2, betterproto2.TYPE_ENUM, default_factory=lambda: Frame.BODY)

    def __post_init__(self) -> None:
        super().__post_init__()
        self.src = Frame(self.src)
        self.dst = Frame(self.dst)


@dataclass
class Transform(betterproto2.Message):
    """Flattened 4x4 transform matrix stored row-major."""

    matrix: list[float] = betterproto2.field(1, betterproto2.TYPE_FLOAT, repeated=True)


@dataclass
class GetFrameTransformResponse(betterproto2.Message):
    """Response wrapper containing the requested frame transform."""

    transform: Transform | None = betterproto2.field(1, betterproto2.TYPE_MESSAGE, optional=True)
