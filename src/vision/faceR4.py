#Kabul edilebilir

import cv2
import numpy as np
import threading
import time
import face_recognition
import os

path = 'photos'
images = []
classNames = []
myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encodeList.append(encodes[0])
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete")

model_path = 'cascades/opencv_dnn_model.caffemodel'
model_config = 'cascades/opencv_dnn_model.prototxt'
threshold = 0.8
photo_size = (300, 300)

model = cv2.dnn.readNetFromCaffe(model_config, model_path)

frame = None
faces = []
face_names = []
lock = threading.Lock()

def face_detection_thread():
    global frame, faces, lock
    while True:
        if frame is None:
            time.sleep(0.01)
            continue

        lock.acquire()
        img = frame.copy()
        lock.release()

        blob = cv2.dnn.blobFromImage(cv2.resize(img, photo_size), 1.0, photo_size, [104.0, 117.0, 123.0])
        model.setInput(blob)
        detections = model.forward().squeeze()

        detections = detections[detections[:, 2] > threshold]
        probs, boxes = detections[:, 2], detections[:, 3:]

        h, w = img.shape[:2]
        boxes = boxes * np.array([w, h, w, h])
        boxes = boxes.astype(int)

        lock.acquire()
        faces = boxes.tolist()
        lock.release()

        time.sleep(0.01)

def face_recognition_thread():
    global frame, faces, face_names, lock, encodeListKnown, classNames
    while True:
        if frame is None or not faces:
            time.sleep(0.01)
            continue

        lock.acquire()
        img = frame.copy()
        detected_faces = faces.copy()
        lock.release()

        face_names_local = []

        for (x1, y1, x2, y2) in detected_faces:

            face_img = img[y1:y2, x1:x2]
            rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)

            encodes = face_recognition.face_encodings(rgb_face)
            name = "Unknown"
            if encodes:
                face_encode = encodes[0]
                matches = face_recognition.compare_faces(encodeListKnown, face_encode)
                face_dist = face_recognition.face_distance(encodeListKnown, face_encode)
                best_match_index = np.argmin(face_dist)
                if matches[best_match_index]:
                    name = classNames[best_match_index].upper()

            face_names_local.append(name)

        lock.acquire()
        face_names = face_names_local
        lock.release()
        time.sleep(0.05)

def main():
    global frame, faces, face_names, lock

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera could not be opened.")
        return

    t1 = threading.Thread(target=face_detection_thread, daemon=True)
    t2 = threading.Thread(target=face_recognition_thread, daemon=True)
    t1.start()
    t2.start()

    while True:
        ret, img = cap.read()
        if not ret:
            print("Failed to get frame.")
            break

        frame = cv2.flip(frame, 1)

        img = cv2.flip(img, 1)

        lock.acquire()
        frame = img.copy()
        current_faces = faces.copy()
        current_names = face_names.copy()
        lock.release()

        for (box, name) in zip(current_faces, current_names):
            x1, y1, x2, y2 = box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow("Threaded Face Detection + Recognition", img)

        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()