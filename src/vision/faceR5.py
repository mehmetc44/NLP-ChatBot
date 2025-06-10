import cv2
import numpy as np
import os
import insightface
from insightface.app import FaceAnalysis
from numpy.linalg import norm

# 1- Kayıtlı yüzlerin olduğu klasör
path = 'photos'
images = []
classNames = []
myList = os.listdir(path)

for cl in myList:
    img_path = os.path.join(path, cl)
    img = cv2.imread(img_path)
    if img is None:
        continue
    images.append(img)
    classNames.append(os.path.splitext(cl)[0])

print("Loaded faces:", classNames)

# 2- InsightFace modeli hazırla
model = FaceAnalysis(name='buffalo_l')  # veya başka bir model ismi
model.prepare(ctx_id=-1)  # 0: GPU, -1: CPU

# 3- Kayıtlı yüzlerden embedding çıkar
def get_embedding(img):
    faces = model.get(img)
    if len(faces) == 0:
        return None
    return faces[0].embedding

encodeListKnown = []
for img in images:
    embedding = get_embedding(img)
    if embedding is not None:
        encodeListKnown.append(embedding)
print("Embeddings extracted for known faces")

# 4- Benzerlik hesaplama (cosine similarity)
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# 5- Kamera aç
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # İstersen frame küçült (hız için)
    imgS = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)

    # 6- Kameradan yüz tespit et
    faces = model.get(imgS)

    for face in faces:
        bbox = face.bbox.astype(int)
        embedding = face.embedding

        # 7- Tanıma için en iyi eşleşmeyi bul
        name = "Unknown"
        max_sim = 0.5  # Eşik değer, 0.5 civarı deneyebilirsin
        for known_emb, known_name in zip(encodeListKnown, classNames):
            sim = cosine_similarity(embedding, known_emb)
            if sim > max_sim:
                max_sim = sim
                name = known_name

        # 8- Koordinatları orijinal frame ölçeğine çevir
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = x1*2, y1*2, x2*2, y2*2  # Çünkü frame 0.5 küçültülmüştü

        # 9- Kutuyu çiz ve ismi yaz
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("InsightFace Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('0'):
        break

cam.release()
cv2.destroyAllWindows()