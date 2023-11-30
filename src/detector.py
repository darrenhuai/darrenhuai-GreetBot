import cv2
import numpy as np
import face_recognition as fr

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

def generate_encodings(directory, verbose=False):
    '''
    Given a directory path, returns a list of the encodings and names of the directory.
    '''
    encodings, names = [], []
    length = len(os.listdir(directory))
    for i,filename in enumerate(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(filename)
            _, enc, _ = find_face(fr.load_image_file(f))
            encodings.append(enc)
            names.append(filename.split('.')[0])
        printProgressBar (iteration=i+1, total=length)
    return encodings, names

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
