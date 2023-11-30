# import numpy as np
from ast import parse
import cv2
import timeit
import sys
import argparse
from pyfirmata import Arduino, SERVO, util
from time import sleep
from playsound import playsound
from random import randint

import torch

# YOLO v5 Models
tt_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')  # or yolov5n - yolov5x6, custom
mask_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./mask_yolov5.pt')

# Initializing Cascade Classifiers
haar_path = 'haas_cascade_test/'
face_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_smile.xml')

# Initializing Arduino Port
port = '/dev/cu.usbmodem144301'
pin=9
#board = None 
board=Arduino(port)
board.digital[pin].mode=SERVO
arduino = False  

def main(
        no_arduino=False,
        verbose=False,
        no_smile=False,
        no_tt=False,
        no_mask=False
):
    # If arduino is enabled, initialize
    #arduino = not no_arduino
    #print('no_arduino', no_arduino)
    #print('arduino', arduino)
    #if arduino:
        #print("arduino initilaized")
        # board=Arduino(port)
        # board.digital[pin].mode=SERVO  
    smile = not no_smile
    tt = not no_tt
    mask = not no_mask

    video_capture = cv2.VideoCapture(0)
    smile_queue, tt_queue = [], []
    while video_capture.isOpened():
    # Captures video_capture frame by frame
        _, frame = video_capture.read()
    
        # To capture image in monochrome                   
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # detect smile
        if smile:
            frame, is_smiling = detect_smile(gray, frame)  
            if len(smile_queue) > 30:
                smile_queue.pop(0)
        
        # detect theta tau logo
        if tt:
            frame, is_tt = detect_tt(gray, frame)
            if len(tt_queue) > 30:
                tt_queue.pop(0)

        # Detect if mask if being worn
        if mask:
            frame, is_mask = detect_mask(gray, frame)
        
        #smile_queue.append(is_smiling)
        tt_queue.append(is_tt)
        if (smile and len([True for s in smile_queue if s]) > 2) or (tt and is_tt) or (mask and is_mask):
            # print('is smiling')
            signal()
            smile_queue, tt_queue = [], []


        # Displays the result on camera feed                    
        cv2.imshow('Video', frame)
    
        # The control breaks once q key is pressed                       
        if cv2.waitKey(1) & 0xff == ord('q'):              
            break
    
    # Release the capture once all the processing is done.
    video_capture.release()                                
    cv2.destroyAllWindows()


def rotateservo(pin, angle):
    #if not arduino:
       # return
    
    board.digital[pin].write(angle)
    sleep(.015)


for k in range(0,60):
   rotateservo(pin,k) 


def signal():
    print("now")
    #if not arduino:
     #   print("stopping")
     #   return

    #while True:
        #x=input("input: ")
        #rotateservo(pin,45)
        #sleep(1)
        #if x=="1":
        # for playing note.mp3 file
        
        #print('playing sound using  playsound') 
    for i in range(60,125):
        rotateservo(pin,i)

    soundint = randint(1,14)
    print(soundint)
    filename = '/Users/krishshah/Desktop/rose_'
    filename += str(soundint)
    filename += '.m4a'
    playsound(filename)

    sleep(2)
    print("hello")
    h = 125
    while h!= 60:
        rotateservo(pin,h)
        h-= 1

    sleep(10)

'''
detectMultiScale() recommended parameters
https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
'''
def detect_smile(gray, frame):
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
            print('is smiling!')
 
    return frame, is_smiling

def detect_tt(gray, frame):
    '''
    Given a frame, uses the trained model to detect the tt logo
    and draws the predicted bounding box around the object.
    '''
    results = tt_model(frame)
    tt_detections = results.pandas().xyxy
    is_tt = False

    for tt_detection in tt_detections:
        if tt_detection.name.size > 0:
            is_tt = True
            print('found tt!')
            xmin, ymin, xmax, ymax = get_coords(tt_detection)
            cv2.rectangle(frame, (xmin, ymin), ((xmax), (ymax)), (3, 239, 3), 2)
            break

    return frame, is_tt

def detect_mask(gray, frame):
    '''
    Given a frame, uses the pre-trained model to detect if the mask is worn properly
    and draws the predicted bounding box around the object.
    '''
    results = mask_model(frame)
    mask_detections = results.pandas().xyxy
    is_mask = False

    for mask_detection in mask_detections:
        if mask_detection.name.size > 0 and mask_detection.name.iloc[0] == 'with_mask':
            is_mask = True
            print('found mask!')
            xmin, ymin, xmax, ymax = get_coords(mask_detection)
            cv2.rectangle(frame, (xmin, ymin), ((xmax), (ymax)), (239, 134, 119), 2)
            break

    return frame, is_mask

def get_coords(detection_df):
    '''
    Helper function that takes a Pandas DataFrame generated from a prediction,
    and returns the coordinates that describe that bounding box.
    '''
    xmin = int(detection_df.xmin.iloc[0])
    xmax = int(detection_df.xmax.iloc[0])
    ymin = int(detection_df.ymin.iloc[0])
    ymax = int(detection_df.ymax.iloc[0])
    return xmin, ymin, xmax, ymax

def parse_opt():
    '''
    Parses optional arguments for runner.py
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-arduino', action='store_true', help='true when running without arduino')
    parser.add_argument('--verbose', action='store_true', help='prints to terminal when object is detected')
    parser.add_argument('--no-smile', action='store_true', help='disables smile detection')
    parser.add_argument('--no-tt', action='store_true', help='disables tt detection')
    parser.add_argument('--no-mask', action='store_true', help='disables mask detection')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    main(**vars(opt))