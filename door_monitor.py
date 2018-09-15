import cv2
import time

import json
from watson_developer_cloud import VisualRecognitionV3

#Initialization
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    iam_apikey='vjmKV_6yhL6kBnWZ5rMsHNRgLStIM7LkE-m3pybypuUw'
)

last_frame = 0

cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    
    #captures frame from video feed
    ret, img = cap.read()
    cv2.imshow("Door Feed", img)

    
    if time.time() - last_frame > 1:
        last_frame = time.time()

        cv2.imwrite("test.jpg", img)

        with open('./test.jpg', 'rb') as images_file:
            faces = visual_recognition.detect_faces(images_file).get_result()
        #print(json.dumps(faces, indent=2))

        if len(faces['images'][0]['faces']) > 0:
            print("A PERSON!!! \(OoO)/")

            x = faces['images'][0]['faces'][0]['face_location']['left']
            y = faces['images'][0]['faces'][0]['face_location']['top']
            dx = faces['images'][0]['faces'][0]['face_location']['width']
            dy = faces['images'][0]['faces'][0]['face_location']['height']

            #face_crop = img[x:x+dx, y:y+dy]
            face_crop = img[y:y+dy, x:x+dx]
            cv2.imshow("face_crop", face_crop)
            cv2.imwrite("face_crop.jpg", face_crop)

            
            # for detecting multiple faces
            '''
            for i in range(len(faces['images'][0]['faces'])): 
                x = faces['images'][0]['faces'][i]['face_location']['left']
                y = faces['images'][0]['faces'][i]['face_location']['top']
                dx = faces['images'][0]['faces'][i]['face_location']['width']
                dy = faces['images'][0]['faces'][i]['face_location']['height']

                face_crop = img[x:y, dx:dy]
                cv2.imwrite("face"+str(i)+".jpg", img)

            #send picture of person's face to firebase
            #send video of their actions to firebase
            '''


        else:
            print("no person -.-")
            

        
    #hold escape to exit program
    k = cv2.waitKey(10)
    if k == 27:
        cap.release()
        break


