from django.http import StreamingHttpResponse
import cv2
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cv2
import pickle
from keras.models import load_model
import matplotlib.pyplot as plt


part=[0,0,0,0,0,0,0]
model=load_model('./models/student_engagement.h5')
def empty(img):
    pass

def cond(img):
    pred=model.predict(img,verbose=0)
    if (pred[0][0]==1):
        part[0]=part[0]+1
        return 'confused'
    elif (pred[0][1]==1):
        part[1]=part[1]+1
        return 'Looking Away'
    elif (pred[0][2]==1):
        part[2]=part[2]+1
        return 'bored'
    elif (pred[0][3]==1):
        part[3]=part[3]+1
        return 'drowsy'
    elif (pred[0][4]==1):
        part[4]=part[4]+1
        return 'engaged'
    elif (pred[0][5]==1):
        part[5]=part[5]+1
        return 'Not Interested'
    else:
        part[6]=part[6]+1

def preprocessing(img):
    img = cv2.resize(img, dsize=(256, 256))
    img=  img.reshape((1, 256, 256, 3))
    return img

def video_feed(request):
    def generate_frames():
        cap=cv2.VideoCapture(0)
        font=cv2.FONT_HERSHEY_COMPLEX
        

        while True:
            _,imgOrig=cap.read()
            img=np.asarray(imgOrig)
            img=preprocessing(img)
            cv2.putText(imgOrig,str(cond(img)),(120,35),font,0.75,(124,100,213),2,cv2.LINE_AA)
            #print(part)
            
            #embedding into webpage
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', imgOrig)[1].tobytes() + b'\r\n')
            #cap.release()
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace;boundary=frame')
