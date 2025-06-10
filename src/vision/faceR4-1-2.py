import src.vision.faceR4-1-1.FaceRecognizer

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