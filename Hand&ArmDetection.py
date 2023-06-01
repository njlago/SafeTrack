import cv2
import mediapipe as mp
from djitellopy import Tello

# Connect to the Tello drone
tello = Tello()
tello.connect()

tello.streamon()

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Constants for gesture recognition
THUMBS_UP = 0
THUMBS_DOWN = 1
OPEN_PALM = 2
CLOSED_PALM = 3
ARM_RAISED = 4
ARM_LOWERED = 5

# Variables to store current gesture
current_gesture = None

# Function to perform gesture recognition
def recognize_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

    thumb_to_index = thumb_tip.y - index_finger_tip.y
    thumb_to_pinky = thumb_tip.y - pinky_tip.y
    thumb_to_middle = thumb_tip.y - middle_finger_tip.y
    wrist_y = wrist.y

    if thumb_to_index > 0.05 and thumb_to_pinky > 0.05 and thumb_to_middle < 0:
        return THUMBS_UP
    elif thumb_to_index < -0.1 and thumb_to_pinky < -0.1 and thumb_to_middle < 0:
        return THUMBS_DOWN
    elif thumb_to_index > 0.05 and thumb_to_pinky > 0.05 and thumb_to_middle > 0.1:
        return OPEN_PALM
    elif thumb_to_index < -0.1 and thumb_to_pinky < -0.1 and thumb_to_middle < -0.1:
        return CLOSED_PALM
    elif wrist_y < 0.2:
        return ARM_RAISED
    elif wrist_y > 0.5:
        return ARM_LOWERED
    else:
        return None

# Main loop
while True:
    frame = tello.get_frame_read().frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = recognize_gesture(hand_landmarks)

            if gesture is not None:
                if current_gesture != gesture:
                    current_gesture = gesture

                    if current_gesture == ARM_RAISED:
                        tello.move_up(40)
                    elif current_gesture == ARM_LOWERED:
                        tello.move_down(40)
                    elif current_gesture == OPEN_PALM:
                        tello.takeoff()
                    elif current_gesture == CLOSED_PALM:
                        tello.land()
                    
                    # Reset current_gesture after performing an action
                    current_gesture = None

            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )

    cv2.imshow('Tello Stream', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Disconnect from the Tello drone
tello.streamoff()
tello.disconnect()
cv2.destroyAllWindows()

