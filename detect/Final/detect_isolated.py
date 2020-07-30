import cv2
import numpy as np
import tensorflow as tf

# Initialize classifiers
mouth_classifier = cv2.CascadeClassifier('../OpenCV/HAAR/haarmouth.xml')
face_classifier = cv2.CascadeClassifier('../OpenCV/HAAR/haarface.xml')

model = tf.keras.models.load_model('../Tensorflow/model.h5')
model.compile(loss='binary_crossentropy',
            optimizer='rmsprop',
            metrics=['accuracy'])

capture = cv2.VideoCapture(0)
if  not capture.isOpened():
    print("Capture initialization failed")

while (capture.isOpened()):
    mask_flag = False
    left_flag = False
    right_flag = False
    ret, color = capture.read()
    color = cv2.flip(color,1)
    frame = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    
    faces = face_classifier.detectMultiScale(frame, 1.3, 5)    
    mouths = mouth_classifier.detectMultiScale(frame,1.3,5)

    for (x,y,w,h) in faces:

        flag = False
        for (mx,my,mw,mh) in mouths:
            if ((mx >= x and mx <= x + w) and (my >= y and my <= y + h) ):
                flag = True        
        if flag:
            cv2.putText(color, "Not Masked :(", (x,y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1 ,(0,0,255), 2, cv2.LINE_AA)
            cv2.rectangle(color, (x,y), (x+w,y+h), (0,0,255), 2)
        else:
            cv2.putText(color, "Masked :)", (x,y - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)
            cv2.rectangle(color, (x,y), (x+w,y+h), (0,255,0), 2)
            mask_flag = True


    cap_width  = int(capture.get(3))
    cap_height = int(capture.get(4)) 


    #get cropped images
    left_hand  = color[int(cap_height/5):int(cap_height*4/5), 0:int(cap_width/3)]
    right_hand =  color[int(cap_height/5):int(cap_height*4/5), int(cap_width*2/3):cap_width]
    

    #left prediction
    left_prediction = ""
    BGRcolor = (0,0,0)
    img = cv2.resize(left_hand,(150,150))
    img = np.reshape(img,[1,150,150,3])
    classes = model.predict(img)
    if (classes[0][0] == 1) :
        left_prediction = "Wear a glove!"
        BGRcolor = (0,0,255)
    else:
        left_prediction = "Nice glove!"
        left_flag = True
        BGRcolor = (0,255,0)
    leftcoord = (0,int(cap_height*4/5) + int(cap_height/13))

    # draw according box and text
    cv2.rectangle(color,(0,int(cap_height/5)), (int(cap_width/3),int(cap_height*4/5)), BGRcolor, 2)
    cv2.putText(color, left_prediction, leftcoord , cv2.FONT_HERSHEY_SIMPLEX,1, BGRcolor, 2, cv2.LINE_AA)

    #right prediction
    right_prediction = ""
    img = cv2.resize(right_hand,(150,150))
    img = np.reshape(img,[1,150,150,3])
    classes = model.predict(img)
    if (classes[0][0] == 1) :
        right_prediction = "Wear a glove!"
        BGRcolor = (0,0,255)
    else:
        right_prediction = "Nice glove!"
        BGRcolor = (0,255,0)
        right_flag = True
    rightcoord = (int(cap_width*2/3),int(cap_height*4/5) + int(cap_height/13))

    # draw according box and text
    cv2.rectangle(color,(int(cap_width*2/3),int(cap_height/5)), (int(cap_width),int(cap_height*4/5)), BGRcolor, 2)
    cv2.putText(color, right_prediction, rightcoord, cv2.FONT_HERSHEY_SIMPLEX,1,BGRcolor, 2, cv2.LINE_AA)

    #safety check
    if (mask_flag and left_flag and right_flag):
        cv2.putText(color, "Safety Check Passed", (int(cap_width/3) + 30, int(cap_height/10)) , cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,0), 2, cv2.LINE_AA)
    else :
        cv2.putText(color, "Safety Check Failed", (int(cap_width/3) + 30, int(cap_height/10)) , cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imshow("Frame", color)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

capture.release()
cv2.destroyAllWindows()