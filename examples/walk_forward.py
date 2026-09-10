"""Walk the robot forward for three seconds then stop."""

import time

from booster_rpc import BoosterConnection

MOVE_INTERVAL = 0.05


def main():
    conn = BoosterConnection()

    status = conn.get_status()
    print(f"Current mode: {status.mode.name}")

    conn.stand_up()
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
