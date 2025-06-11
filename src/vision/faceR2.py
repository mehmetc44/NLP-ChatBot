import cv2
import numpy as np
import time
from multiprocessing import Queue, Process, Lock
from face_rec_2 import recognition_worker


def main():
    # İletişim kuyruklarını oluştur
    frame_queue = Queue(maxsize=1)
    result_queue = Queue(maxsize=1)
    lock = Lock()

    # Yüz tanıma servisini başlat
    p = Process(target=recognition_worker,
                args=(frame_queue, result_queue, lock))
    p.daemon = True
    p.start()

    # Kamera bağlantısı
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    last_time = time.time()
    fps = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # FPS hesaplama
            current_time = time.time()
            fps = 1 / (current_time - last_time)
            last_time = current_time

            # Frame'i servise gönder
            if frame_queue.empty():
                frame_queue.put(frame.copy())

            # Sonuçları al
            names = []
            if not result_queue.empty():
                names = result_queue.get()

            # Görüntüyü göster (yüksek FPS)
            display_frame = frame.copy()

            # FPS bilgisini ekrana yaz
            cv2.putText(display_frame, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Tanınan yüzleri göster
            if names:
                cv2.putText(display_frame, f"Recognized: {', '.join(names)}",
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0), 2)

            cv2.imshow("Camera", display_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        p.terminate()
        p.join()


if __name__ == "__main__":
    main()