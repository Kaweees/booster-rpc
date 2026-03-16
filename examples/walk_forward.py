"""Walk the robot forward for 3 seconds."""

import time

from booster_rpc import (
    BoosterConnection,
    GetRobotStatusResponse,
    RobotChangeModeRequest,
    RobotMode,
    RobotMoveRequest,
    RpcApiId,
)

MOVE_INTERVAL = 0.05


def main():
    conn = BoosterConnection()

    resp = conn.call(RpcApiId.GET_ROBOT_STATUS)
    status = GetRobotStatusResponse().parse(resp.payload)
    print(f"Current mode: {status.mode.name}")

    if status.mode != RobotMode.WALKING:
        if status.mode == RobotMode.DAMPING:
            conn.call(RpcApiId.ROBOT_CHANGE_MODE, bytes(RobotChangeModeRequest(mode=RobotMode.PREPARE)))
            print("Mode -> Prepare")
            time.sleep(3)
        conn.call(RpcApiId.ROBOT_CHANGE_MODE, bytes(RobotChangeModeRequest(mode=RobotMode.WALKING)))
        print("Mode -> Walking")
        time.sleep(3)

    print("Moving forward...")
    end_time = time.time() + 3.0
    while time.time() < end_time:
        conn.call(RpcApiId.ROBOT_MOVE, bytes(RobotMoveRequest(vx=0.5)))
        time.sleep(MOVE_INTERVAL)

    conn.call(RpcApiId.ROBOT_MOVE, bytes(RobotMoveRequest()))
    print("Stopped")


if __name__ == "__main__":
    main()
