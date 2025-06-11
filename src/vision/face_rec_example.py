import src.vision
import cv2

# Kullanım örneği:
if __name__ == "__main__":
    # Initialize once
    recognizer = FaceRecognizer(photos_dir='photos')

    # Test için basit bir kamera döngüsü (siz kullanmayacaksınız)
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Frame işleme (sizin uygulamanızda bu frame PyQt'den gelecek)
        names = recognizer.process_frame(frame)
        print("Tanınan yüzler:", names)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


self.face_recognizer = FaceRecognizer(photos_dir='photos')


# Yeni frame geldiğinde (örneğin QTimer timeout'unda)
def process_camera_frame(self):
    frame = self.get_frame_from_camera()  # Kendi frame alma metodunuz
    recognized_names = self.face_recognizer.process_frame(frame)

    if recognized_names:
        print("Tanınan kişiler:", recognized_names)
    else:
        print("Yüz tespit edilemedi veya tanınmadı")