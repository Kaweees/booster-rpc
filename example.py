"""Example usage of BoosterRPCConnection — walk forward then stop."""

import time

from booster_rpc import (
    BoosterRPCConnection,
    GetRobotStatusResponse,
    RobotChangeModeRequest,
    RobotMode,
    RobotMoveRequest,
    RpcApiId,
)

MOVE_INTERVAL = 0.05  # seconds between move commands


def main():
    conn = BoosterRPCConnection()

    # Check current mode
    resp = conn._call(RpcApiId.GET_ROBOT_STATUS)
    status = GetRobotStatusResponse().parse(resp.payload)
    print(f"Current mode: {status.mode.name}")

    # Switch to walking if not already
    if status.mode != RobotMode.WALKING:
        if status.mode == RobotMode.DAMPING:
            payload = bytes(RobotChangeModeRequest(mode=RobotMode.PREPARE))
            conn._call(RpcApiId.ROBOT_CHANGE_MODE, payload)
            print("Mode -> Prepare")
            time.sleep(3)

        payload = bytes(RobotChangeModeRequest(mode=RobotMode.WALKING))
        conn._call(RpcApiId.ROBOT_CHANGE_MODE, payload)
        print("Mode -> Walking")
        time.sleep(3)

    # Walk forward for 3 seconds by sending continuous move commands
    print("Moving forward...")
    end_time = time.time() + 3.0
    while time.time() < end_time:
        payload = bytes(RobotMoveRequest(vx=0.5, vy=0.0, vyaw=0.0))
        conn._call(RpcApiId.ROBOT_MOVE, payload)
        time.sleep(MOVE_INTERVAL)

    # Stop by sending zero velocity
    payload = bytes(RobotMoveRequest(vx=0.0, vy=0.0, vyaw=0.0))
    conn._call(RpcApiId.ROBOT_MOVE, payload)
    print("Stopped")


if __name__ == "__main__":
    main()
