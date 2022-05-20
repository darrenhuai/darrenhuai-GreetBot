# import numpy as np
from ast import parse
import cv2
import timeit
import sys
import argparse
from pyfirmata import Arduino, SERVO, util
from time import sleep
from playsound import playsound

import torch

# YOLO v5 Models
tt_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./best.pt')  # or yolov5n - yolov5x6, custom
mask_model = torch.hub.load('ultralytics/yolov5', 'custom', path='./mask_yolov5.pt')

# Images
img = './1.png'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
# results = model(img)
# Results
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# results.show()
# exit()

# Initializing Cascade Classifiers
haar_path = 'haas_cascade_test/'
face_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier(haar_path + 'haarcascade_smile.xml')

# Initializing Arduino Port
port = '/dev/cu.usbmodem144301'
pin=9
board = None 
arduino = False  

def main(no_arduino=False):
    # If arduino is enabled, initialize
    arduino = not no_arduino
    print('no_arduino', no_arduino)
    print('arduino', arduino)
    if arduino:
        board=Arduino(port)
        board.digital[pin].mode=SERVO  

    video_capture = cv2.VideoCapture(0)
    smile_queue, tt_queue = [], []
    while video_capture.isOpened():
    # Captures video_capture frame by frame
        _, frame = video_capture.read()
    
        # To capture image in monochrome                   
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        
        # detect smile  
        canvas, is_smiling = detect_smile(gray, frame)  
        if len(smile_queue) > 30:
            smile_queue.pop(0)
        
        # detect theta tau logo
        canvas, is_tt = detect_tt(gray, frame)
        if len(tt_queue) > 30:
            tt_queue.pop(0)

        # Detect if mask if being worn
        canvas, is_mask = detect_mask(gray, frame)
        
        smile_queue.append(is_smiling)
        tt_queue.append(is_tt)
        if len([True for s in smile_queue if s]) > 5 or is_tt or is_mask:
            # print('is smiling')
            signal()
            smile_queue, tt_queue = [], []


        # Displays the result on camera feed                    
        cv2.imshow('Video', canvas)
    
        # The control breaks once q key is pressed                       
        if cv2.waitKey(1) & 0xff == ord('q'):              
            break
    
    # Release the capture once all the processing is done.
    video_capture.release()                                
    cv2.destroyAllWindows()

def signal():
    if not arduino:
        return

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

def rotateservo(pin, angle):
    if not arduino:
        return
    
    board.digital[pin].write(angle)
    sleep(.015)

    for k in range(0,90):
        rotateservo(pin,k) 

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
    
    results = tt_model(frame)
    tt_detections = results.pandas().xyxy[0].to_json(orient="records")

    # print(tt_detections)
    is_tt = tt_detections != '[]'
    if is_tt:
        print('found tt!')

    return frame, is_tt

def detect_mask(gray, frame):
    results = mask_model(frame)
    mask_detections = results.pandas().xyxy# .to_json(orient="records")
    
    is_mask = False

    for mask_detection in mask_detections:
        if mask_detection.name.size > 0 and mask_detection.name.iloc[0] == 'with_mask':
            is_mask = True
            print('found mask!')
            break

    return frame, is_mask

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--no-arduino', action='store_true', help='true when running without arduino')
    opt = parser.parse_args()
    return opt

if __name__ == '__main__':
    opt = parse_opt()
    main(**vars(opt))