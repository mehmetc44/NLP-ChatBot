import cv2
import mediapipe as mp

class HandGestureRecognizer:
    def __init__(self, max_num_hands=4, min_detection_confidence=0.8):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence
        )
        #self.mp_draw = mp.solutions.drawing_utils

        self.gestures = {
            (0, 1, 1, 0, 0): "Peace",
            (1, 0, 0, 0, 0): "Okay",
            (1, 1, 1, 1, 1): "Stop",
            (0, 0, 0, 0, 0): "Punch",
            (0, 1, 0, 0, 0): "Forward",
            (0, 1, 0, 0, 1): "Rock",
        }
    def process_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        total_fingers = 0
        detected_gesture = ""

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                #self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

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
                    finger_states.append(1 if lm[tip_id].y < lm[tip_id - 2].y else 0)

                total_fingers += sum(finger_states)
                gesture_tuple = tuple(finger_states)
                if gesture_tuple in self.gestures:
                    detected_gesture = self.gestures[gesture_tuple]

        return frame, total_fingers, detected_gesture
