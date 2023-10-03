import threading


face_direction = "middle"

# semaphore threading
face_direction_lock = threading.Lock()


def update_face_direction(direction):
    with face_direction_lock:
        global face_direction
        face_direction = direction


def get_face_direction():
    global face_direction
    return face_direction
