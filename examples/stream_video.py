"""Stream the robot's camera to an OpenCV window. Press q to quit."""

import asyncio

import cv2
import numpy as np

from booster_rpc import BoosterConnection


def main():
    conn = BoosterConnection()
    window = "Booster K1 Camera"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)

    def on_frame(frame: bytes):
        img = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow(window, img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            raise KeyboardInterrupt

    try:
        asyncio.run(conn.stream_video(on_frame))
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
