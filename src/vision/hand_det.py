import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=4, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

camera = cv2.VideoCapture(0)

gestures = {
    (0, 1, 1, 0, 0): "Peace",
    (1, 0, 0, 0, 0): "Okay",
    (1, 1, 1, 1, 1): "Stop",
    (0, 0, 0, 0, 0): "Punch",
    (0, 1, 0, 0, 0): "Forward",
    (0, 1, 0, 0, 1): "Rock",
    (0, 0, 1, 0, 0): "oe",

}

while True:
    ret, frame = camera.read()
    if not ret:
        print("No image received.")
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    total_fingers = 0
    detected_gesture = ""

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm = hand_landmarks.landmark
            finger_states = []

            thumb_tip = lm[4]
            thumb_ip = lm[2]
            pinky_tip = lm[17]

            if not (min(thumb_ip.x, pinky_tip.x) < thumb_tip.x < max(thumb_ip.x, pinky_tip.x)):
                finger_states.append(1)
            else:
                finger_states.append(0)

            for tip_id in [8, 12, 16, 20]:
                if lm[tip_id].y < lm[tip_id - 2].y:
                    finger_states.append(1)
                else:
                    finger_states.append(0)

            finger_count = sum(finger_states)
            total_fingers += finger_count

            gesture_tuple = tuple(finger_states)
            if gesture_tuple in gestures:
                detected_gesture = gestures[gesture_tuple]

    if detected_gesture:
        text = f"Fingers: {total_fingers} | Gesture: {detected_gesture}"
    else:
        text = f"Fingers: {total_fingers}"

    cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 255), 2)

    cv2.imshow("Hand Recognition and Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

camera.release()
cv2.destroyAllWindows()