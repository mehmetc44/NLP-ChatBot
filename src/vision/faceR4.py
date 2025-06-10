#Kabul edilebilir en iyi

import cv2
import numpy as np
import threading
import time
import face_recognition
import os

def find_encodings(images):
    encode_list = []
    for img in images:
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if encodes:
            encode_list.append(encodes[0])
    return encode_list

def face_detection_thread():
    global frame, faces, lock
    while True:
        if frame is None:
            time.sleep(0.01)
            continue

        with lock:
            img = frame.copy()

        try:
            blob = cv2.dnn.blobFromImage(cv2.resize(img, PHOTO_SIZE), 1.0, PHOTO_SIZE, [104.0, 117.0, 123.0])
            model.setInput(blob)
            detections = model.forward()

            if detections.size == 0:
                with lock:
                    faces = []
                continue

            detections = detections.squeeze()
            if len(detections.shape) == 1:
                detections = np.expand_dims(detections, axis=0)
            detections = detections[detections[:, 2] > THRESHOLD]

            h, w = img.shape[:2]
            boxes = (detections[:, 3:] * np.array([w, h, w, h])).astype(int)

            with lock:
                faces = boxes.tolist()
        except Exception as e:
            print(f"Detection error: {e}")
            with lock:
                faces = []
        time.sleep(0.01)

def face_recognition_thread():
    global frame, faces, face_names, lock, encode_list_known, class_names
    while True:
        if frame is None:
            time.sleep(0.01)
            continue

        with lock:
            img = frame.copy()
            detected_faces = faces.copy()

        face_names_local = []
        for box in detected_faces:
            if len(box) != 4:  # Geçersiz bounding box kontrolü
                continue

            x1, y1, x2, y2 = box
            face_img = img[y1:y2, x1:x2]

            if face_img.size == 0:  # Boş görüntü kontrolü
                continue

            try:
                rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                encodes = face_recognition.face_encodings(rgb_face)
                name = "Unknown"
                if encodes:
                    face_encode = encodes[0]
                    matches = face_recognition.compare_faces(encode_list_known, face_encode)
                    face_dist = face_recognition.face_distance(encode_list_known, face_encode)
                    best_match_index = np.argmin(face_dist)
                    if matches[best_match_index]:
                        name = class_names[best_match_index].upper()
                face_names_local.append(name)
            except Exception as e:
                print(f"Recognition error: {e}")
                face_names_local.append("Unknown")

        with lock:
            face_names = face_names_local
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

        img = cv2.flip(img, 1)

        with lock:
            frame = img.copy()
            current_faces = faces.copy()
            current_names = face_names.copy()

        for box, name in zip(current_faces, current_names):
            if len(box) != 4:
                continue
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
    PATH = 'photos'
    THRESHOLD = 0.8
    PHOTO_SIZE = (300, 300)
    MODEL_PATH = 'cascades/opencv_dnn_model.caffemodel'
    MODEL_CONFIG = 'cascades/opencv_dnn_model.prototxt'

    images = []
    class_names = []
    my_list = os.listdir(PATH)
    for cl in my_list:
        cur_img = cv2.imread(f'{PATH}/{cl}')
        if cur_img is not None:
            images.append(cur_img)
            class_names.append(os.path.splitext(cl)[0])

    encode_list_known = find_encodings(images)
    print("Encoding Complete")

    model = cv2.dnn.readNetFromCaffe(MODEL_CONFIG, MODEL_PATH)

    frame = None
    faces = []
    face_names = []
    lock = threading.Lock()

    main()