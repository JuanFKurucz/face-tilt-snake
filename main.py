import threading

from face.main import run_face_tilt_detection, frame_queue
from game.main import run_game
from utils import update_face_direction, get_face_direction, face_direction_lock

if __name__ == "__main__":
    face_detection_thread = threading.Thread(
        target=run_face_tilt_detection,
        kwargs={
            "middle_angle": 90.0,
            "threshold": 50.0,
            "update_method": update_face_direction,
        },
    )
    face_detection_thread.start()

    run_game(
        get_method=get_face_direction, lock=face_direction_lock, frame_queue=frame_queue
    )
