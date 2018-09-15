import cv2
import time

import json
from watson_developer_cloud import VisualRecognitionV3

#Initializastion
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    iam_apikey='vjmKV_6yhL6kBnWZ5rMsHNRgLStIM7LkE-m3pybypuUw'
)

last_frame = 0

def save_faces(faces, img):

    print("A PERSON!!! \(OoO)/")
    print(len(faces['images'][0]['faces']))
    for i in range(len(faces['images'][0]['faces'])): 
        x = faces['images'][0]['faces'][i]['face_location']['left']
        y = faces['images'][0]['faces'][i]['face_location']['top']
        dx = faces['images'][0]['faces'][i]['face_location']['width']
        dy = faces['images'][0]['faces'][i]['face_location']['height']

        face_crop = img[y:y+dy, x:x+dx]
        cv2.imwrite("face"+str(i)+".jpg", face_crop)
        cv2.imshow("face"+str(i)+".jpg", face_crop)


def face_search(img):
    cv2.imwrite("test.jpg", img)

    with open('./test.jpg', 'rb') as images_file:
        faces = visual_recognition.detect_faces(images_file).get_result()
    #print(json.dumps(faces, indent=2))

    if len(faces['images'][0]['faces']) > 0:
        save_faces(faces, img)
    else:
        print("no person -.-")


def main():
    cap = cv2.VideoCapture(1)
    while(cap.isOpened()):
        
        #captures frame from video feed
        ret, img = cap.read()
        
        #checks for faces every second
        if time.time() - last_frame > 1:
            last_frame = time.time()

            face_search(img)
                
        #hold escape to exit program
        k = cv2.waitKey(10)
        if k == 27:
            cap.release()
            break

if __name__ == "__main__":
    main()
