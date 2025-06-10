#yolo kullanılır, iyi algılar ama fps minik düşer gibi

import cv2
from ultralytics import YOLO

model = YOLO("cascades/yolov8n-face-lindevs.pt")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("error.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("error.")
        break

    frame = cv2.flip(frame, 1)

    results = model(frame, verbose=False)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])

        if confidence > 0.5:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("YOLOv8-Face Webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

cap.release()
cv2.destroyAllWindows()