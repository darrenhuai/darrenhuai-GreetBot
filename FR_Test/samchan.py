import os
import cv2
import numpy as np
import face_recognition as fr

def generate_encodings(directory):
    '''
    Given a directory path, returns a list of the encodings and names of the directory.
    '''
    count = 0
    encodings, names = [], []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(names)
            _, enc, _ = find_face(fr.load_image_file(f))
            encodings.append(enc)
            names.append(filename.split('.')[0])
            count += 1
            if count == 0:
                break
    return encodings, names

def main():
    encodings, names = generate_encodings('./pledges/')
    print('finished generating encodings')
    print(encodings)
    video_capture = cv2.VideoCapture(0)
    while video_capture.isOpened():
    # Captures video_capture frame by frame
        _, frame = video_capture.read()

        if not has_face(frame):
            print('no face')
            continue
        
        # imgRudy, encRudy = find_face(fr.load_image_file('./pledges/rudy.JPG'))
        frame, enc, (top, right, bottom, left) = find_face(frame)
        
        results = fr.face_distance(encodings, enc)
        # print(results)
        # print(names)
        match_i, similarity = np.argmin(results), 1 - np.min(results)
        
        print(names[match_i])
        
        cv2.putText(frame, f'{names[match_i]} ({100 * similarity:.2f}%)', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        # imgTest, encTest = find_face(fr.load_image_file('./akshay1.jpg'))


         #results = fr.compare_faces([enc], encTest)
        if results[0] == False:
            print('no match')
        else:
            print('match')

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

def has_face(img):
    '''
    Returns boolean on whether image has face or not.
    '''
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return len(fr.face_locations(img)) > 0

def find_face(img, name=None):
    '''
    Returns the face (cv2 image, encoding) taking up the largest area in the image.
    '''
    ## Load Face
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_locations = fr.face_locations(img)
    if len(face_locations) == 0:
        return None, None
    max_i = 0
    max_area = 0
    for i,(t,r,b,l) in enumerate(face_locations):
        if (b - t) * (r - l) > max_area:
            max_area = (b - t) * (r - l)
            max_i = i
    encoding = fr.face_encodings(img)[max_i]
    top, right, bottom, left = face_locations[max_i]
    cv2.rectangle(img, (left, top), (right, bottom), (255,0,255), 2)
    return img, encoding, (top, right, bottom, left)

if __name__ == '__main__':
    main()
    # test()