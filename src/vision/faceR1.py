#fotoğrafları karşılaştırır

import cv2
import numpy as np
import face_recognition

imgMec = face_recognition.load_image_file('photos/Emre Cengiz/mec.jpg')
imgMec = cv2.cvtColor(imgMec,cv2.COLOR_BGR2RGB)
imgMec = cv2.resize(imgMec,(700,700))

imgTest = face_recognition.load_image_file('photos/Emre Cengiz/mec2.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
imgTest = cv2.resize(imgTest,(700,700))

faceLoc = face_recognition.face_locations(imgMec)[0]
encodeMec = face_recognition.face_encodings(imgMec)[0]
cv2.rectangle(imgMec,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(0,255,0),2)

faceLocTest = face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(0,255,0),2)

results = face_recognition.compare_faces([encodeMec],encodeTest)
faceDis = face_recognition.face_distance([encodeMec],encodeTest)
print(results,faceDis)
cv2.putText(imgMec,f"{results} {round(faceDis[0],2)}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)


cv2.imshow('mec',imgMec)
cv2.imshow('test',imgTest)
cv2.waitKey(0)