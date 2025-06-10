#göz burun ağıza noktalar koyar, yan duran yüzleri algılayamaz

import cv2
from facenet_pytorch import MTCNN

camera = cv2.VideoCapture(0)

model = MTCNN(image_size=300, margin=0, min_face_size=40, thresholds=[0.6,0.7,0.7], factor=0.709, post_process=True)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

while True:
    ret, frame = camera.read()
    if not ret:
        print("No image received.")
        break
    frame = cv2.flip(frame, 1)

    faces, olasiliklar, face_points = model.detect(frame, landmarks=True)

    if faces is not None:
        for (x, y, w, h), olasilik, face_point in zip(faces, olasiliklar, face_points):
            x, y, w, h = list(map(int, (x, y, w, h)))
            cv2.rectangle(frame, (x, y), (w, h), (0, 0, 225), 2)
            olasilik = f"{olasilik:.2f}"
            cv2.putText(frame, olasilik, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            for n in face_point:
                nx, ny = list(map(int, n))
                cv2.circle(frame, (nx, ny), 2, (0, 0, 255), -1)

    cv2.namedWindow('Face Recognition',cv2.WINDOW_NORMAL)
    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

camera.release()
cv2.destroyAllWindows()