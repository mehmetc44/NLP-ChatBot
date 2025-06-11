import cv2
import numpy as np
from multiprocessing import Queue, Process
from src.gui.pages.face_rec_3 import recognition_service


def main():
    # İletişim kuyruklarını oluştur
    input_queue = Queue()
    output_queue = Queue()

    # Servisi başlat
    p = Process(target=recognition_service, args=(input_queue, output_queue))
    p.daemon = True
    p.start()

    # 1. SEÇENEK: Kamera ile çalışma
    use_camera = True  # False yaparak kamera kullanımını kapatabilirsiniz

    if use_camera:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    else:
        # 2. SEÇENEK: Boş frame ile çalışma
        blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)  # Siyah boş frame
        # Veya örnek bir frame oluşturabilirsiniz:
        # blank_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    try:
        while True:
            if use_camera:
                ret, frame = cap.read()
                if not ret:
                    break
            else:
                # Boş frame kullan
                frame = blank_frame.copy()

                # Örnek olarak frame'e rastgele gürültü ekleyelim
                # (Gerçek uygulamada buraya kendi frame'inizi vereceksiniz)
                cv2.putText(frame, "Custom Frame", (50, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Frame'i servise gönder
            if input_queue.empty():
                input_queue.put(frame)

            # Sonuçları al ve print et
            if not output_queue.empty():
                names = output_queue.get()
                if names:
                    print(f"Tanınan yüzler: {names}")
                else:
                    print("Yüz tespit edilemedi")

            # Görüntüyü göster (opsiyonel)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        if use_camera:
            cap.release()
        cv2.destroyAllWindows()
        input_queue.put(None)
        p.join()


if __name__ == "__main__":
    main()
