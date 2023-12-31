import math

import cv2
import mediapipe as mp

from queue import Queue

frame_queue = Queue()


def run_face_tilt_detection(middle_angle=90.0, threshold=50.0, update_method=None):
    """
    Run face tilt detection using OpenCV and Mediapipe.

    Args:
        middle_angle (float): The middle angle representing the neutral head position.
        threshold (float): The angle threshold to determine left/right head tilt.
        update_method (callable): A method to update the detected head tilt direction.

    Raises:
        ValueError: If the provided update_method is not callable.
    """
    # Initialize the Mediapipe face detection and landmark detection components
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh

    # Open a video capture stream (you can also use a webcam)
    cap = cv2.VideoCapture(0)
    past_direction = "middle"

    with mp_face_detection.FaceDetection(
        min_detection_confidence=0.5
    ) as face_detection, mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame to RGB format (required by Mediapipe)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform face detection
            results_detection = face_detection.process(frame_rgb)

            if results_detection.detections:
                # Perform face landmark detection
                results_landmarks = face_mesh.process(frame_rgb)
                if results_landmarks.multi_face_landmarks:
                    for detection in results_detection.detections:
                        bboxC = detection.location_data.relative_bounding_box
                        ih, iw, _ = frame.shape
                        x, y, w, h = (
                            int(bboxC.xmin * iw),
                            int(bboxC.ymin * ih),
                            int(bboxC.width * iw),
                            int(bboxC.height * ih),
                        )
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    landmarks = results_landmarks.multi_face_landmarks[0]

                    # Extract relevant facial landmarks (e.g., eyes and nose)
                    left_eye = landmarks.landmark[33]
                    right_eye = landmarks.landmark[263]
                    nose_tip = landmarks.landmark[168]

                    # Calculate the tilt of the head
                    eye_midpoint = (
                        (left_eye.x + right_eye.x) / 2,
                        (left_eye.y + right_eye.y) / 2,
                    )
                    head_tilt_angle = math.degrees(
                        math.atan2(
                            nose_tip.y - eye_midpoint[1],
                            nose_tip.x - eye_midpoint[0],
                        )
                    )

                    direction = "middle"
                    abs_head_tilt_angle = abs(head_tilt_angle)
                    if abs_head_tilt_angle > middle_angle + threshold:
                        direction = "right"
                    elif abs_head_tilt_angle < middle_angle - threshold:
                        direction = "left"
                    # Call the update method with the detected direction
                    if past_direction != direction:
                        past_direction = direction
                        update_method(direction)

                    cv2.putText(
                        frame,
                        f"Angulo: {head_tilt_angle:.2f} grados; Direccion: {direction}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )

            # Display the frame
            frame_queue.put(frame)

    cap.release()


# Example usage:
# def update_head_tilt(direction):
#     print(f"Head tilt direction: {direction}")
#
# run_face_tilt_detection(update_method=update_head_tilt)
