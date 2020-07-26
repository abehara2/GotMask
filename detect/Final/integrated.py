import cv2
import numpy as np
import tensorflow as tf
import time
import smbus

#define LCD display functions
BUS = smbus.SMBus(1)
def write_word(addr, data):
    global BLEN
    temp = data
    if BLEN == 1:
        temp |= 0x08
    else:
        temp &= 0xF7
    BUS.write_byte(addr ,temp)

def send_command(comm):
    # Send bit7-4 firstly
    buf = comm & 0xF0
    buf |= 0x04               
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (comm & 0x0F) << 4
    buf |= 0x04               
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               
    write_word(LCD_ADDR ,buf)

def send_data(data):
    # Send bit7-4 firstly
    buf = data & 0xF0
    buf |= 0x05               
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB                
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (data & 0x0F) << 4
    buf |= 0x05                
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB                
    write_word(LCD_ADDR ,buf)

def init(addr, bl):
#   global BUS
#   BUS = smbus.SMBus(1)
    global LCD_ADDR
    global BLEN
    LCD_ADDR = addr
    BLEN = bl
    try:
        send_command(0x33)  
        time.sleep(0.005)
        send_command(0x32)  
        time.sleep(0.005)
        send_command(0x28)  
        time.sleep(0.005)
        send_command(0x0C)  
        time.sleep(0.005)
        send_command(0x01)  
        BUS.write_byte(LCD_ADDR, 0x08)
    except:
        return False
    else:
        return True

def clear():
    send_command(0x01)  

def openlight():  
    BUS.write_byte(0x27,0x08)
    BUS.close()

def write(x, y, str):
    if x < 0:
        x = 0
    if x > 15:
        x = 15
    if y <0:
        y = 0
    if y > 1:
        y = 1

    # Move cursor
    addr = 0x80 + 0x40 * y + x
    send_command(addr)

    for chr in str:
        send_data(ord(chr))    


def setup():
    init(0x27, 1)
    write(0, 0, 'Got a Mask?')
    write(1, 1, 'And your gloves too?')
    time.sleep(2)

def destroy():
    pass  


#define detection function
def detect():
    #initialize HAAR classifiers
    mouth_classifier = cv2.CascadeClassifier('/Users/ashankbehara/GitHub/GotMask/detect/OpenCV/HAAR Cascade/haarcascade_mcs_mouth.xml')
    face_classifier = cv2.CascadeClassifier('/Users/ashankbehara/GitHub/GotMask/detect/OpenCV/HAAR Cascade/haarcascade_frontalface_default.xml')

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
        
        #tensorflow CNN prediction
        model = tf.keras.models.load_model('../Tensorflow/model.h5')
        model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

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
            clear()
            write(0, 0, 'You are safe!')
        else :
            cv2.putText(color, "Safety Check Failed", (int(cap_width/3) + 30, int(cap_height/10)) , cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255), 2, cv2.LINE_AA)
            clear()
            write(0, 0, 'You are not safe!')
            
        cv2.imshow("Frame", color)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            destroy()
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "main":
    try:
        setup()
        detect()
        while True:
            pass
    except KeyboardInterrupt:
        destroy()
