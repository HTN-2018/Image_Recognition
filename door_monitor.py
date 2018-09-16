import cv2
import time

import json
from watson_developer_cloud import VisualRecognitionV3

import pyrebase
import time
from configuration import *
from helpers import *


#def initialize():

visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    #iam_apikey='3JFeQ9NxcJjESkniWwfQzMaKin3ff2hbmzfpze7YkdrT'
    iam_apikey='v7YXRuo_CXPRmOz3QmpbqPQlSfuFHkEKG43YB5urqyJV'
)


#set up firebase
fb = pyrebase.initialize_app(FIREBASE_CONFIG)
auth = fb.auth()
db = fb.database()
storage = fb.storage()

user = authenticate_user(auth)


#print(user)

def log_faces(faces, img):

    print("A PERSON!!! \(OoO)/")
    ppl_num = len(faces['images'][0]['faces'])

    for i in range(ppl_num): 
        x = faces['images'][0]['faces'][i]['face_location']['left']
        y = faces['images'][0]['faces'][i]['face_location']['top']
        dx = faces['images'][0]['faces'][i]['face_location']['width']
        dy = faces['images'][0]['faces'][i]['face_location']['height']

        face_crop = img[y:y+dy, x:x+dx]
        cv2.imwrite("face"+str(i)+".jpg", face_crop)
        cv2.imshow("face"+str(i)+".jpg", face_crop)

    return ppl_num

def send_push(user, faces):

    metadata_store = db.child("users").child(user['localId']).push(faces, user['idToken'])

def upload_pics(ppl_num):
    for i in range(ppl_num):
        media_store = storage.child('images/' + user['localId'] + '/' + str(time.time()) + '.jpg').put("face"+str(i)+".jpg", user['idToken'])

def face_search(img):
    cv2.imwrite("test.jpg", img)

    with open('./test.jpg', 'rb') as images_file:
        faces = visual_recognition.detect_faces(images_file).get_result()

    if len(faces['images'][0]['faces']) > 0:
        print(json.dumps(faces, indent=2))
        ppl_num = log_faces(faces, img)
        send_push(user, faces)
        upload_pics(ppl_num)
    else:
        print("no person -.-")


def main():
    #user, visual_recongnition = initialize()

    last_frame = 0

    #for i in range(2):
    #    media_store = storage.child('images/' + user['localId'] + '/' + str(time.time()) + '.png').put("face"+str(i)+".jpg", user['idToken'])

    cap = cv2.VideoCapture(1)
    while(cap.isOpened()):
        
        #captures frame from video feed
        ret, img = cap.read()
        
        #checks for faces every second
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


'''
#Get data video/images/metadata/etc from an event

###TEST EVENTS
event_1 = {
    'time': time.time(),
    'metadata': {'type': 'usps delivery', 'gender': 'female'},
}

event_1_photo = './photos/twitter_banner.png'

event_2 = {
    'time': time.time(),
    'metadata': {'type': 'metronet salesperson', 'gender': 'male'},
}

event_2_photo = './photos/amazon.png'

# Pass the user's idToken to the push method
metadata_store = db.child("users").child(user['localId']).push(event_1, user['idToken'])

#Store the image
#def media_upload(localId, photo, idToken):
media_store = storage.child('images/' + user['localId'] + '/' + str(time.time()) + '.png').put(event_1_photo, user['idToken'])
'''

