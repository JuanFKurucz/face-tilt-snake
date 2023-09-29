import threading

from face import run_face_tilt_detection
from game import run_game


if __name__ == "__main__":
    face_detection_thread = threading.Thread(target=run_face_tilt_detection)
    face_detection_thread.start()

    run_game()
