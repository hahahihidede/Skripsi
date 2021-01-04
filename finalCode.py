import cv2
from base64 import b64encode, b64decode
import pyrebase
from math import pow, sqrt
import numpy as np
import glob
import time
import requests
import os 


#website dashboard skripsi https://tecorp.me/dede/fsp/retrieve.php

#firebase config
config = config = {
   "apiKey": "AIzaSyBRkht4RH7OFyhH1UU35eLJGsGCc8zGhDM",
   "authDomain": "skripsi-edc2c.firebaseapp.com",
   "databaseURL": "https://skripsi-edc2c-default-rtdb.firebaseio.com",
   "storageBucket": "skripsi-edc2c.appspot.com",
   "appId": "1:659985226910:web:bdf1992762c7f03fd52f8f",
   "service_account": "skripsi2.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


#global config
preprocessing = False
calculateConstant_x = 300
calculateConstant_y = 615
personLabelID = 15.00
debug = True
accuracyThreshold = 0.4
RED = (0,0,255)
YELLOW = (0,255,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
write_video = False
d = 0



def CLAHE(bgr_image: np.array) -> np.array:
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    hsv_planes = cv2.split(hsv)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv_planes[2] = clahe.apply(hsv_planes[2])
    hsv = cv2.merge(hsv_planes)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def centroid(startX,endX,startY,endY):
    c_x = round((startX+endX)/2,4)
    c_y = round((startY+endY)/2,4)
    boundBoxHeight = round(endY-startY,4)
    return c_x,c_y,boundBoxHeight

def calcDistance(boundBoxHeight):
    distance = (calculateConstant_x * calculateConstant_y) / boundBoxHeight
    return distance

def drawResult(frame,position):
    for i in position.keys():
        if i in highRisk:
            rectangleColor = RED
        elif i in mediumRisk:
            rectangleColor = YELLOW
        else:
            rectangleColor = GREEN
        (startX, startY, endX, endY) = detectionCoordinates[i]

        cv2.rectangle(frame, (startX, startY), (endX, endY), rectangleColor, 2)
        
        # print (distance)

if __name__== "__main__":

    caffeNetwork = cv2.dnn.readNetFromCaffe("./SSD_MobileNet_prototxt.txt", "./SSD_MobileNet.caffemodel")
    cap = cv2.VideoCapture("./pedestrians.mp4")
    d = 0

    while cap.isOpened():

        debug_frame, frame = cap.read()
        highRisk = set()
        mediumRisk = set()
        position = dict()
        detectionCoordinates = dict()

        if not debug_frame:
            # print("Video Error Gaes")
            break
        if preprocessing:
            frame = CLAHE(frame)
            print(frame)

        (imageHeight, imageWidth) = frame.shape[:2]
        pDetection = cv2.dnn.blobFromImage(cv2.resize(frame, (imageWidth, imageHeight)), 0.007843, (imageWidth, imageHeight), 127.5)

        caffeNetwork.setInput(pDetection)
        detections = caffeNetwork.forward()

        for i in range(detections.shape[2]):

            accuracy = detections[0, 0, i, 2]
            if accuracy > accuracyThreshold:

                idOfClasses = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([imageWidth, imageHeight, imageWidth, imageHeight])
                (startX, startY, endX, endY) = box.astype('int')

                if idOfClasses == personLabelID:

                    boundBoxDefaultColor = (255,255,255)
                    cv2.rectangle(frame, (startX, startY), (endX, endY), boundBoxDefaultColor, 2)
                    detectionCoordinates[i] = (startX, startY, endX, endY)


                    c_x, c_y, boundBoxHeight = centroid(startX,endX,startY,endY)                    
                    distance = calcDistance(boundBoxHeight)

                    c_x_centimeters = (c_x * distance) / calculateConstant_y
                    c_y_centimeters = (c_y * distance) / calculateConstant_y
                    position[i] = (c_x_centimeters, c_y_centimeters, distance)


        for i in position.keys():
            
            for j in position.keys():
                if i < j:
                    distanceOfboundBoxes = sqrt(pow(position[i][0]-position[j][0],2) 
                                          + pow(position[i][1]-position[j][1],2) 
                                          + pow(position[i][2]-position[j][2],2)
                                          )

                    if distanceOfboundBoxes < 150: # jarak tidak aman
                        highRisk.add(i),highRisk.add(j)
                        desimal= round (distanceOfboundBoxes,1)

                        for i in highRisk:
                            if desimal < 150:
                                print(desimal)
                                filename = "cropped/file_%d.png"%d
                                cv2.imwrite(filename, frame)
                                d+=1
                                print("Cropped")
                    elif distanceOfboundBoxes < 200 > 150: # Jarak rawan
                        mediumRisk.add(i),mediumRisk.add(j) 
            

        
        cv2.putText(frame, "Sangat Rawan Penularan : " + str(len(highRisk)) , (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Rawan Penularan : " + str(len(mediumRisk)) , (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
        cv2.putText(frame, "Jumlah Terdeteksi : " + str(len(detectionCoordinates)), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        drawResult(frame, position)
        cv2.imshow('Dashboard', frame)
        waitkey = cv2.waitKey(1)
        if waitkey == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Sending to Firebase")



def sendData():
    folder = 'cropped'
    for img in glob.glob(folder + "/*.png"):
        with open(img, 'rb') as f:
                data = f.read()

        str = b64encode(data).decode('UTF-8')
        db.child("image").push({'data': str})
        print("An image has been sent")
sendData()
print("image has been sent")