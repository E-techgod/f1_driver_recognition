from pathlib import Path

import cv2
import pickle
import numpy as np
import os

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"

video= cv2.VideoCapture(0) # 0 bc is local camera, if external use 1
faceDetect= cv2.CascadeClassifier(str(DATA_DIR / "haarcascade_frontalface_default.xml"))
facesList=[]
i=0

name= input("Enter your name: ")

while True:
    ret,frame=video.read() 
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # color
    faces= faceDetect.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:  # w=width, h= height draw the frame
        cropImage= frame[y:y+h, x:x+w : ]
        reSizeImage= cv2.resize(cropImage, (50,50))
        if len(facesList)<=100 and i%10==0:
            facesList.append(reSizeImage)
        i=i+1
        cv2.putText(frame, str(len(facesList)), (30,30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 2)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 2)  

    cv2.imshow("frame", frame)  # show frame
    key=cv2.waitKey(1)
    if key==ord('q') or len(facesList)==100:
        break
video.release()
cv2.destroyAllWindows()

facesList= np.asarray(facesList) 
facesList= facesList.reshape(100,-1)

if "listNames.pkl" not in os.listdir(DATA_DIR):
    names= [name]*100
    with open(DATA_DIR / "listNames.pkl", 'wb') as f: 
        pickle.dump(names, f)
else:
    with open(DATA_DIR / "listNames.pkl", 'rb') as f: 
        names= pickle.load(f)
    names= names+[name]*100
    with open(DATA_DIR / "listNames.pkl", 'wb') as f: 
        pickle.dump(names, f)
    

if "listFaces.pkl" not in os.listdir(DATA_DIR):
    with open(DATA_DIR / "listFaces.pkl", 'wb') as f: 
        pickle.dump(facesList, f)
else:
    with open(DATA_DIR / "listFaces.pkl", 'rb') as f: 
        faces= pickle.load(f)
    faces= np.append(faces, facesList, axis=0)
    with open(DATA_DIR / "listFaces.pkl", 'wb') as f: 
        pickle.dump(faces, f)
