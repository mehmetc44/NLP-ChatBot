import cv2
import numpy as np
import face_recognition
import os
from multiprocessing import Process, Queue


class FaceRecognizer:
    def __init__(self, photos_dir='photos'):
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces(photos_dir)

        self.face_detector = cv2.dnn.readNetFromCaffe(
            'cascades/opencv_dnn_model.prototxt',
            'cascades/opencv_dnn_model.caffemodel'
        )

    def load_known_faces(self, photos_dir):
        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)
            return

        for person_dir in os.listdir(photos_dir):
            person_path = os.path.join(photos_dir, person_dir)
            if os.path.isdir(person_path):
                for img_file in os.listdir(person_path):
                    img_path = os.path.join(person_path, img_file)
                    img = cv2.imread(img_path)
                    if img is not None:
                        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encodings = face_recognition.face_encodings(rgb_img)
                        if encodings:
                            self.known_encodings.append(encodings[0])
                            self.known_names.append(person_dir)

        print(f"Loaded {len(self.known_encodings)} known faces")

    def recognize_faces(self, frame):
        if frame is None or frame.size == 0:
            return []

        # Yüz tespiti
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()

        faces = []
        h, w = frame.shape[:2]
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                faces.append(box.astype("int"))

        # Yüz tanıma
        names = []
        for (x1, y1, x2, y2) in faces:
            face_img = frame[y1:y2, x1:x2]
            if face_img.size == 0:
                continue

            rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_face)

            name = "Unknown"
            if encodings:
                matches = face_recognition.compare_faces(
                    self.known_encodings, encodings[0], tolerance=0.6)
                face_distances = face_recognition.face_distance(
                    self.known_encodings, encodings[0])
                best_match_idx = np.argmin(face_distances)

                if matches[best_match_idx]:
                    name = self.known_names[best_match_idx]
                    name = name.replace("_", " ")

            names.append(name)

        return names


def recognition_service(input_queue, output_queue):
    recognizer = FaceRecognizer()
    print("Face recognition service started...")

    while True:
        if not input_queue.empty():
            frame = input_queue.get()

            # None gönderilirse servisi kapat
            if frame is None:
                break

            names = recognizer.recognize_faces(frame)
            output_queue.put(names)


if __name__ == "__main__":
    input_queue = Queue()
    output_queue = Queue()

    p = Process(target=recognition_service, args=(input_queue, output_queue))
    p.start()

    try:
        while True:
            # Servis çalışırken başka işlemler yapılabilir
            pass
    except KeyboardInterrupt:
        input_queue.put(None)
        p.join()