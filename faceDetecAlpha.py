import cv2
import face as face
import numpy as np
import requests, json
import urllib.parse
import sys

LINE_ACCESS_TOKEN = "M7DVShId2nSX9RHFIbkjyrAurMpyFObLOmqhqWx1jel"
URL_LINE = "https://notify-api.line.me/api/notify" 

def line_text(message):	
    msg = urllib.parse.urlencode({"message":message})
    LINE_HEADERS = {'Content-Type':'application/x-www-form-urlencoded',"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    session_post = session.post(URL_LINE, headers=LINE_HEADERS, data=msg)
    print(session_post.text)

def line_pic(message, path_file):
    file_img = {'imageFile': open(path_file, 'rb')}
    msg = ({'message': message})
    LINE_HEADERS = {"Authorization":"Bearer "+LINE_ACCESS_TOKEN}
    session = requests.Session()
    session_post = session.post(URL_LINE, headers=LINE_HEADERS, files=file_img, data=msg)
    print(session_post.text)

font = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10, 500)
fontScale = 1
fontColor = (255, 255, 255)
lineType = 2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
i = 0
timeCount = 0
imgCount = 0
Detect = False
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if type(faces) == tuple:
        Detect = False
    else:
        Detect = True
        i += 1
    for (x, y, w, h) in faces:
        
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(img, 'Imposter',
                    (x,y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)
    cv2.imshow('img', img)
    print(i)
    if Detect == True and  i%50 == 0:
        img_name = "opencv{}.png".format(imgCount)
        cv2.imwrite(img_name,img)
        imgCount+=1
        line_pic('มีคนเล่นคอมมม!!!',img_name)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()

