# test_recognizer.py
import cv2
from face_rec import FaceRecognizer


def main():
    # 1. FaceRecognizer'ı başlat
    recognizer = FaceRecognizer(photos_dir='photos')

    # 2. Kamera bağlantısı (sadece test için, siz PyQt'nin kamerayı kullanacaksınız)
    cap = cv2.VideoCapture(0)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Kameradan görüntü alınamadı")
                break

            # 3. Frame'i işle ve sonuçları al
            names = recognizer.process_frame(frame)

            if names:
                print("Tanınan kişiler:", names)
                # Burada PyQt'ye sinyal gönderebilirsiniz
            else:
                print("Yüz tespit edilemedi veya tanınmadı")

            # Test için görüntüyü göster (gerçek uygulamada gerek yok)
            cv2.imshow("Test", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()