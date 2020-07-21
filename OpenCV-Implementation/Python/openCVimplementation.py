import cv2
import numpy as np
import time

face_classifier = cv2.CascadeClassifier('/Users/ashankbehara/GitHub/GotMask/Pure-OpenCV/HAAR Cascade/haarcascade_frontalface_default.xml')
mouth_classifier = cv2.CascadeClassifier('/Users/ashankbehara/GitHub/GotMask/Pure-OpenCV/HAAR Cascade/haarcascade_mcs_mouth.xml')

capture = cv2.VideoCapture(0)
if  not capture.isOpened():
    print("Capture initialization failed")

while (capture.isOpened()):
    ret, color = capture.read()
    frame = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    
    faces = face_classifier.detectMultiScale(frame, 1.3, 5)    
    mouths = mouth_classifier.detectMultiScale(frame,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(color, (x,y), (x+w,y+h), (127,0,255), 2)

        flag = False
        for (mx,my,mw,mh) in mouths:
            if ((mx >= x and mx <= x + w) and (my >= y and my <= y + h) ):
                flag = True        
        if flag:
            cv2.putText(color, "Not Masked :(", (x,y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1 ,(127,0,255), 2, cv2.LINE_AA)
        else:
            cv2.putText(color, "Masked :)", (x,y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (127,0,255), 2, cv2.LINE_AA)

    cv2.imshow("Frame", color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
capture.release()
cv2.destroyAllWindows()