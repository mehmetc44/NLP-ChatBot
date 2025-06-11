#çok iyi algılar

import cv2
import numpy as np

camera = cv2.VideoCapture(0)

model_path = ('cascades/opencv_dnn_model.caffemodel')
model_config = ('cascades/opencv_dnn_model.prototxt')
model = cv2.dnn.readNetFromCaffe(model_config,model_path)
esik_degeri = 0.8

photo_size = (300,300)

if not camera.isOpened():
    print("Camera could not be opened.")
    exit()

while True:
    ret, frame = camera.read()

    if not ret:
        print("No image received.")
        break

    frame = cv2.flip(frame, 1)

    blob = cv2.dnn.blobFromImage(cv2.resize(frame,photo_size),1.0,photo_size,[104.0, 117.0,123.0])
    model.setInput(blob)
    faces = model.forward().squeeze()[:,2:]
    faces = faces[faces[:,0] > esik_degeri]

    olasiliklar, faces = faces[:,0], faces[:,1:]
    h, w = frame.shape[:2]
    faces *= np.array([w, h, w, h])

    for (x, y, w, h),olasilik in zip(faces,olasiliklar):
        x, y, w, h = list(map(int, (x, y, w, h)))
        cv2.rectangle(frame, (x, y), (w, h), (0, 0, 225), 2)
        olasilik = f"{olasilik:.2f}"
        cv2.putText(frame, olasilik, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

camera.release()
cv2.destroyAllWindows()