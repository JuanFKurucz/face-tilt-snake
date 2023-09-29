import threading

directions = ["left", "up", "right", "down"]

face_direction = "middle"

# semaphore threading
face_direction_lock = threading.Lock()


def change_direction(direction):
    snake_direction = (0, 0)
    if direction == "left":
        snake_direction = (-1, 0)
    elif direction == "right":
        snake_direction = (1, 0)
    elif direction == "up":
        snake_direction = (0, -1)
    elif direction == "down":
        snake_direction = (0, 1)
    return snake_direction


def update_face_direction(direction):
    with face_direction_lock:
        global face_direction
        face_direction = direction


def get_face_direction():
    global face_direction
    return face_direction


def translate_direction(snake_direction):
    if snake_direction == (0, 1):
        return "down"
    elif snake_direction == (0, -1):
        return "up"
    elif snake_direction == (1, 0):
        return "right"
    elif snake_direction == (-1, 0):
        return "left"
