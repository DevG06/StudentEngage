import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cv2
import pickle
from keras.models import load_model

def empty(img):
    pass

def cond(img):
    pred=model.predict(img,verbose=0)
    if (pred[0][0]==1):
        return 'confused'
    elif (pred[0][1]==1):
        return 'Looking Away'
    elif (pred[0][2]==1):
        return 'bored'
    elif (pred[0][3]==1):
        return 'drowsy'
    elif (pred[0][4]==1):
        return 'engaged'
    elif (pred[0][5]==1):
        return 'Not Interested'

def preprocessing(img):
    img = cv2.resize(img, dsize=(256, 256))
    img=  img.reshape((1, 256, 256, 3))
    return img

cap=cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_COMPLEX
model=load_model('./models/student_engagement.h5')

while True:
    _,imgOrig=cap.read()
    img=np.asarray(imgOrig)
    img=preprocessing(img)
    cv2.putText(imgOrig,str(cond(img)),(120,35),font,0.75,(0,0,255),2,cv2.LINE_AA)
    cv2.imshow("Result",imgOrig)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()