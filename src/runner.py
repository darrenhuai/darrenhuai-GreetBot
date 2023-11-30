import os
import cv2
import numpy as np
import pickle
from pyfirmata import Arduino, SERVO, util
from time import sleep
from playsound import playsound
from random import randint

from detector import has_face, find_face, generate_encodings, printProgressBar

port = '/dev/cu.usbmodem144401'
pin=9
#board = None 
board=Arduino(port)
board.digital[pin].mode=SERVO
arduino = False  

def main():
    with open('active_encodings.pkl', 'rb') as f:
        encodings, names = pickle.load(f)
    print('finished generating encodings')
    print(encodings)
    video_capture = cv2.VideoCapture(0)

    while video_capture.isOpened():
        # Captures video_capture frame by frame
        _, frame = video_capture.read()

        if not has_face(frame):
            print('no face')
            continue
        frame, enc, (top, right, bottom, left) = find_face(frame)
        
        results = fr.face_distance(encodings, enc)
        match_i, similarity = np.argmin(results), 1 - np.min(results)
        
        if similarity < 0.6:
            cv2.imshow('Video', frame)
            continue

        cv2.putText(frame, f'{names[match_i]} ({100 * similarity:.2f}%)', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # Displays the result on camera feed                    
        cv2.imshow('Video', frame)
    
        # The control breaks once q key is pressed                       
        if cv2.waitKey(1) & 0xff == ord('q'):              
            break

def test():
    img1, enc1 = find_face(fr.load_image_file('./akshay1.jpg'))
    img2, enc2 = find_face(fr.load_image_file('./akshay3.jpg'))
    img3, enc3 = find_face(fr.load_image_file('./emilia1.jpg'))
    img4, enc4 = find_face(fr.load_image_file('./emilia2.jpg'))
    img5, enc5 = find_face(fr.load_image_file('./krish2.png'))
    img6, enc6 = find_face(fr.load_image_file('./pledges/rudy.png'))
    imgTest, encTest = find_face(fr.load_image_file('./akshay2.jpg'))

    results = fr.compare_faces([enc1, enc2, enc3, enc4, enc5, enc6], encTest)
    print(results)

    cv2.imshow('img1', img1)
    cv2.imshow('img2', img2)
    cv2.imshow('img3', img3)
    cv2.imshow('img4', img4)
    cv2.imshow('img5', img5)
    cv2.imshow('img5', img6)
    cv2.imshow('imgTest', imgTest)

    cv2.waitKey(0)

def rotateservo(pin, angle):
    board.digital[pin].write(angle)
    sleep(.015)

for k in range(0,60):
   rotateservo(pin,k) 

def signal(match):
    print(match)
    
    for i in range(60,115):
        rotateservo(pin,i)

    filename = '/Users/krishshah/Desktop/BES22/'
    filename += match
    filename += '.m4a'
    playsound(filename)

    sleep(2)
    print("hello")
    h = 115
    while h!= 60:
        rotateservo(pin,h)
        h-= 1

    sleep(10)

if __name__ == '__main__':
    main()
    # test()