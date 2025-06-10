import cv2
import numpy as np
import face_recognition
import os
import threading
import time

# -------------------- VERİLERİ YÜKLE -------------------- #
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
        encodings = face_recognition.face_encodings(img, num_jitters=2, model='large')
        if encodings:
            encodeList.append(encodings[0])
    return encodeList

encodeListKnown = findEncodings(images)
print("Encoding Complete")

# -------------------- GLOBAL DEĞİŞKENLER -------------------- #
frame = None
resized_rgb_frame = None
face_locations = []
face_names = []

lock = threading.Lock()

# -------------------- DETECTION THREAD -------------------- #
def face_detection_thread():
    global resized_rgb_frame, face_locations
    while True:
        time.sleep(0.01)
        with lock:
            if resized_rgb_frame is None:
                continue
            face_locations = face_recognition.face_locations(resized_rgb_frame)

# -------------------- RECOGNITION THREAD -------------------- #
def face_recognition_thread():
    global resized_rgb_frame, face_locations, face_names
    while True:
        time.sleep(0.01)
        with lock:
            if resized_rgb_frame is None or not face_locations:
                continue

            encodesCurFrame = face_recognition.face_encodings(resized_rgb_frame, face_locations)
            local_names = []

            for i, faceLoc in enumerate(face_locations):
                name = "Unknown"
                if i < len(encodesCurFrame):
                    encodeFace = encodesCurFrame[i]
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    if len(faceDis) > 0:
                        matchIndex = np.argmin(faceDis)
                        if matches[matchIndex]:
                            name = classNames[matchIndex].upper()
                local_names.append(name)

            face_names = local_names

# -------------------- ANA THREAD (GÖRÜNTÜ ve EKRANA YAZMA) -------------------- #
def main():
    global frame, resized_rgb_frame, face_locations, face_names
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı.")
        return

    # Thread’leri başlat
    threading.Thread(target=face_detection_thread, daemon=True).start()
    threading.Thread(target=face_recognition_thread, daemon=True).start()

    while True:
        ret, img = cap.read()
        if not ret:
            print("Kare alınamadı.")
            break

        small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        with lock:
            frame = img.copy()
            resized_rgb_frame = rgb_small_frame.copy()
            current_locations = face_locations.copy()
            current_names = face_names.copy()

        for (top, right, bottom, left), name in zip(current_locations, current_names):
            # Orijinal boyuta çevir (x4)
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Threaded Face Detection & Recognition", img)

        if cv2.waitKey(1) & 0xFF == ord('0'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()