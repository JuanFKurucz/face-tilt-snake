import cv2
import mediapipe as mp

import math


def run_face_tilt_detection(middle_angle=90.0, treshold=50.0, update_method=None):
    # Initialize the Mediapipe face detection and landmark detection components
    mp_face_detection = mp.solutions.face_detection
    mp_face_mesh = mp.solutions.face_mesh

    # Open a video capture stream (you can also use a webcam)
    cap = cv2.VideoCapture(0)

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
                for detection in results_detection.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    x, y, w, h = (
                        int(bboxC.xmin * iw),
                        int(bboxC.ymin * ih),
                        int(bboxC.width * iw),
                        int(bboxC.height * ih),
                    )
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Perform face landmark detection
                    results_landmarks = face_mesh.process(frame_rgb)
                    if results_landmarks.multi_face_landmarks:
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
                        if abs_head_tilt_angle > middle_angle + treshold:
                            direction = "right"
                        elif abs_head_tilt_angle < middle_angle - treshold:
                            direction = "left"

                        update_method(direction)

    cap.release()
