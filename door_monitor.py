import cv2
import time
import math

import json
from watson_developer_cloud import VisualRecognitionV3

import pyrebase
import time
from configuration import *
from helpers import *

#initialize
api_key = ''
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    iam_apikey=api_key
)

#set up firebase
fb = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = fb.auth()
db = fb.database()
storage = fb.storage()

user = authenticate_user(auth)

#print(user)

def log_faces(faces, img):

    ppl_num = len(faces['images'][0]['faces'])
    if ppl_num == 1:
        print("A PERSON!!! \(OoO)/")
    elif ppl_num > 1:
        print( ppl_num, "people! \(OoO)/" )

    for i in range(ppl_num): 
        x = faces['images'][0]['faces'][i]['face_location']['left']
        y = faces['images'][0]['faces'][i]['face_location']['top']
        dx = faces['images'][0]['faces'][i]['face_location']['width']
        dy = faces['images'][0]['faces'][i]['face_location']['height']

        '''
        #makes sure pictures are square
        delta = math.floor(abs(dx - dy))
        if dx > dy:
            if y - math.floor(.5*delta) <= 0:
                y = 0
            elif y + dy + (.5*delta) > max_y:
                y = max_y - delta
            else:
                y -= math.floor(.5*delta)
            dy += delta

        if dx > dx:
            if x - math.floor(.5*delta) <= 0:
                x = 0
            elif x + dx + (.5*delta) > max_x:
                x = max_x - delta
            else:
                x -= math.floor(.5*delta)
            dx += delta
        '''

        face_crop = resize(img[y:y+dy, x:x+dx])
        cv2.imwrite("face"+str(i)+".jpg", face_crop)
        cv2.imshow("face"+str(i)+".jpg", face_crop)

    return ppl_num

def resize(img):
    #resize for fitbit screen
    ratio = 200 / img.shape[0]
    width = int(img.shape[1] * ratio) 
    height = int(img.shape[0] * ratio) 
    
    dim = (width, height)

    resized = cv2.resize(img, dim)

    return resized

def parser(face):

    #picks out useful information
    age_range = str(face['age']['min']) + "-" + str(face['age']['max']) 
    gender = face['gender']['gender']
    date = time.strftime("%b %d, %I:%M %p")

    data = {"age_range" : age_range,
            "gender" : gender,
            "time" : date
            }
    return data

def send_push(user, faces):
    #x = faces['images'][0]['faces'][i]['face_location']['left']
    db.child("users").child("9DZklrkXnYYGhtjTgb57ViG68Vn1").remove()

    for i in faces['images'][0]['faces']:
        face_data = parser(i)
        metadata_store = db.child("users").child(user['localId']).push(face_data, user['idToken'])

def upload_pics(ppl_num):

    for i in range(ppl_num):
        media_store = storage.child('images/' + user['localId'] + '/' +
                "face"+str(i)+ '.jpg').put("face"+str(i)+".jpg", user['idToken'])

def face_search(img):
    cv2.imwrite("0.jpg", img)

    with open('./0.jpg', 'rb') as images_file:
        faces = visual_recognition.detect_faces(images_file).get_result()

    if len(faces['images'][0]['faces']) > 0:
        print(json.dumps(faces, indent=2))
        ppl_num = log_faces(faces, img)
        send_push(user, faces)
        upload_pics(ppl_num)
    else:
        print("no person -.-")

def main():
    last_frame = 0

    #specifies where you are getting your video feed from
    cap = cv2.VideoCapture(1)
    while(cap.isOpened()):
        
        #captures frame from video feed
        ret, img = cap.read()

        #cv2.imshow("face_cam", img)

        #checks for faces every 5 seconds
        if time.time() - last_frame > 5:
            last_frame = time.time()

            face_search(img)
                
        #hold escape to exit program
        k = cv2.waitKey(10)
        if k == 27:
            cap.release()
            break

if __name__ == "__main__":
    main()
