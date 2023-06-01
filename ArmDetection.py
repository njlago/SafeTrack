import cv2
import mediapipe as mp
from djitellopy import Tello

# Connect to the Tello drone
tello = Tello()
tello.connect()

tello.streamon()

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Constants for gesture recognition
ARM_RAISED = 0
ARM_LOWERED = 1

# Variables to store current gesture and drone state
current_gesture = None
drone_state = "landed"

# Function to perform gesture recognition
def recognize_gesture(pose_landmarks):
    left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]

    if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
        return ARM_RAISED
    elif left_wrist.y > left_shoulder.y and right_wrist.y > right_shoulder.y:
        return ARM_LOWERED
    else:
        return None

# Main loop
while True:
    frame = tello.get_frame_read().frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(image)

    if results.pose_landmarks:
        gesture = recognize_gesture(results.pose_landmarks)

        if gesture is not None:
            if current_gesture != gesture:
                current_gesture = gesture

                if current_gesture == ARM_RAISED and drone_state == "landed":
                    tello.takeoff()
                    drone_state = "flying"
                elif current_gesture == ARM_LOWERED and drone_state == "flying":
                    tello.land()
                    drone_state = "landed"
                    
                current_gesture = None

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

    cv2.imshow('Tello Stream', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.land()
tello.streamoff()
tello.end()
cv2.destroyAllWindows()
