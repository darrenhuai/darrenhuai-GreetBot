# import numpy as np
import cv2
import timeit
import sys
from pyfirmata import Arduino, SERVO, util
from time import sleep
from playsound import playsound

# Initializing Cascade Classifiers
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

# Initializing Arduino Port
port = '/dev/cu.usbmodem144301'
pin=9

if len(sys.argv) == 1:
    board=Arduino(port)
    board.digital[pin].mode=SERVO



def rotateservo(pin, angle):
    if sys.argv[1] == '-n':
        return
    
    board.digital[pin].write(angle)
    sleep(.015)

    for k in range(0,90):
        rotateservo(pin,k)      

def main():
    video_capture = cv2.VideoCapture(0)
    smile_queue = []
    while video_capture.isOpened():
    # Captures video_capture frame by frame
        _, frame = video_capture.read()
    
        # To capture image in monochrome                   
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # calls the detect() function   
        canvas, is_smiling = detect(gray, frame)  

        # 
        if len(smile_queue) > 30:
            smile_queue.pop(0)
        
        smile_queue.append(is_smiling)
        if len([True for s in smile_queue if s]) > 5:
            print('is smiling')
            signal()
            smile_queue = []


        # Displays the result on camera feed                    
        cv2.imshow('Video', canvas)
    
        # The control breaks once q key is pressed                       
        if cv2.waitKey(1) & 0xff == ord('q'):              
            break
    
    # Release the capture once all the processing is done.
    video_capture.release()                                
    cv2.destroyAllWindows()

def signal():
    #while True:
        #x=input("input: ")
        #rotateservo(pin,45)
        #sleep(1)
        #if x=="1":
        # for playing note.mp3 file
        
        #print('playing sound using  playsound') 
            for i in range(90,180):
                rotateservo(pin,i)
            playsound('/Users/krishshah/Desktop/tester.m4a')
            sleep(2)
        #1print("now")
            h = 180
            while h!= 90:
                rotateservo(pin,h)
                h-= 1

            sleep(10)

'''
detectMultiScale() recommended parameters
https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
'''
def detect(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    is_smiling = False
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (239, 134, 119), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 30)
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (160, 231, 125), 2)
            is_smiling = True

        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex,ey,ew,eh) in eyes:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(130, 182, 217),2)
 
    return frame, is_smiling

if __name__ == '__main__':
    main()
    # main1()