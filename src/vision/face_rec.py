import cv2
import numpy as np
import threading
import face_recognition
import os


class FaceRecognizer:
    def __init__(self, photos_dir='photos', threshold=0.6):
        self.PHOTO_SIZE = (300, 300)
        self.THRESHOLD = threshold

        # Yüz tanıma modelini yükle
        self.model = cv2.dnn.readNetFromCaffe(
            'cascades/opencv_dnn_model.prototxt',
            'cascades/opencv_dnn_model.caffemodel'
        )

        # Bilinen yüz kodlamalarını yükle
        self.encode_list_known, self.class_names = self._load_known_faces(photos_dir)
        print(
            f"Encoding Complete. {len(self.encode_list_known)} faces loaded from {len(set(self.class_names))} persons.")

        # Thread güvenliği için lock
        self.lock = threading.Lock()
        self.current_names = []

    def _load_known_faces(self, photos_dir):
        images = []
        class_names = []

        if not os.path.exists(photos_dir):
            os.makedirs(photos_dir)
            return [], []

        for person_dir in os.listdir(photos_dir):
            person_path = os.path.join(photos_dir, person_dir)
            if os.path.isdir(person_path):
                for img_file in os.listdir(person_path):
                    cur_img = cv2.imread(os.path.join(person_path, img_file))
                    if cur_img is not None:
                        images.append(cur_img)
                        class_names.append(person_dir)

        encode_list = self._find_encodings(images)
        return encode_list, class_names

    def _find_encodings(self, images):
        encode_list = []
        for img in images:
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodes = face_recognition.face_encodings(img)
            if encodes:
                encode_list.append(encodes[0])
        return encode_list

    def _detect_faces(self, img):
        if img is None:
            return []

        blob = cv2.dnn.blobFromImage(cv2.resize(img, self.PHOTO_SIZE), 1.0,
                                     self.PHOTO_SIZE, [104.0, 117.0, 123.0])
        self.model.setInput(blob)
        detections = self.model.forward()

        if detections.size == 0:
            return []

        detections = detections.squeeze()
        if len(detections.shape) == 1:
            detections = np.expand_dims(detections, axis=0)
        detections = detections[detections[:, 2] > self.THRESHOLD]

        h, w = img.shape[:2]
        boxes = (detections[:, 3:] * np.array([w, h, w, h])).astype(int)
        return boxes.tolist()

    def _recognize_faces(self, img, face_boxes):
        if not face_boxes:
            return []

        face_names = []
        for box in face_boxes:
            if len(box) != 4:
                continue

            x1, y1, x2, y2 = box
            face_img = img[y1:y2, x1:x2]

            if face_img.size == 0:
                face_names.append("Unknown")
                continue

            try:
                rgb_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                encodes = face_recognition.face_encodings(rgb_face)
                name = "Unknown"
                if encodes:
                    face_encode = encodes[0]
                    matches = face_recognition.compare_faces(
                        self.encode_list_known, face_encode, tolerance=0.6)
                    face_dist = face_recognition.face_distance(
                        self.encode_list_known, face_encode)
                    best_match_index = np.argmin(face_dist)
                    if matches[best_match_index]:
                        name = self.class_names[best_match_index]
                        name = name.replace("_", " ")
                face_names.append(name)
            except Exception as e:
                print(f"Recognition error: {e}")
                face_names.append("Unknown")

        return face_names

    def process_frame(self, frame):
        """
        Dışarıdan frame alır ve tanınan yüzlerin isimlerini döner
        Args:
            frame: numpy array - BGR formatında görüntü
        Returns:
            list: Tanınan yüzlerin isimleri ("Unknown" içerebilir)
        """
        if frame is None:
            return []

        # Yüz tespiti
        face_boxes = self._detect_faces(frame)

        # Yüz tanıma
        recognized_names = self._recognize_faces(frame, face_boxes)

        return recognized_names
