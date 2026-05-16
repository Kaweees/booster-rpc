"""Walk the robot forward for 3 seconds."""

import time

from booster_rpc import (
    BoosterConnection,
    RobotMode,
)

MOVE_INTERVAL = 0.05
MODE_POLL_INTERVAL = 0.5
MODE_CHANGE_TIMEOUT = 30.0


def change_mode(
    conn: BoosterConnection, mode: RobotMode, timeout=MODE_CHANGE_TIMEOUT, poll_interval=MODE_POLL_INTERVAL
):
    """Request a mode change and poll until the robot reports it has taken effect.

    The transition latency depends on the robot's current pose, so a single call
    plus a fixed sleep is unreliable.
    """
    conn.change_mode(mode)
    deadline = time.perf_counter() + timeout
    while time.perf_counter() < deadline:
        if conn.get_mode() == mode:
            return
        time.sleep(poll_interval)
    raise TimeoutError(f"Robot did not enter {mode.name} within {timeout}s")


def main():
    conn = BoosterConnection()

    status = conn.get_status()
    print(f"Current mode: {status.mode.name}")

    if status.mode != RobotMode.WALKING:
        if status.mode == RobotMode.DAMPING:
            change_mode(conn, RobotMode.PREPARE)
            print("Mode -> Prepare")

            conn.get_up()
            print("Getting up...")

        change_mode(conn, RobotMode.WALKING)
        print("Mode -> Walking")

    print("Moving forward...")
    deadline = time.perf_counter() + 3.0
    while time.perf_counter() < deadline:
        conn.move(vx=0.5)
        time.sleep(MOVE_INTERVAL)

    conn.move()
    print("Stopped")


if __name__ == "__main__":
    main()
