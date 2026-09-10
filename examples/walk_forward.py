"""Walk the robot forward for 3 seconds."""

import time

from booster_rpc import (
    BoosterConnection,
    RobotMode,
)

MOVE_INTERVAL = 0.05
GET_UP_SETTLE_TIME = 10.0


def main():
    conn = BoosterConnection()

    status = conn.get_status()
    print(f"Current mode: {status.mode.name}")

    # Skip the get-up sequence if the robot is already walking.
    if status.mode != RobotMode.WALKING:
        # Startup sequence: Prepare -> Get Up -> WALKING.
        conn.change_mode(RobotMode.PREPARE)
        print("Mode -> Prepare")

        # Prepare holds a pose; get_up() performs the stand-up motion.
        conn.get_up()
        print("Getting up...")
        # Allow the get-up motion to settle.
        time.sleep(GET_UP_SETTLE_TIME)

        conn.change_mode(RobotMode.WALKING)
        print("Mode -> Walking")

    print("Moving forward...")
    try:
        deadline = time.perf_counter() + 3.0
        while time.perf_counter() < deadline:
            conn.move(vx=0.5)
            time.sleep(MOVE_INTERVAL)
    finally:
        conn.move()
        print("Stopped")


if __name__ == "__main__":
    main()
