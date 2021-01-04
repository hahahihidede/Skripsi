import numpy as np
import cv2
from base64 import b64encode, b64decode
import pyrebase
import glob
import os

config = config = {
   "apiKey": "AIzaSyBRkht4RH7OFyhH1UU35eLJGsGCc8zGhDM",
   "authDomain": "skripsi-edc2c.firebaseapp.com",
   "databaseURL": "https://skripsi-edc2c-default-rtdb.firebaseio.com",
   "storageBucket": "skripsi-edc2c.appspot.com",
   "appId": "1:659985226910:web:bdf1992762c7f03fd52f8f",
   "service_account": "skripsi2.json"
}

# Initialise and connect to Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

with open('./bukti/file_5.png', 'rb') as f:
    data = f.read()
str = b64encode(data).decode('UTF-8')
db.child("image").push({'data': str})


# # Retrieve image from Firebase


# retrieved = db.child("image/-MQ1Uo-a9tYLWxSQAUuf").get().val()
# retrData = retrieved["data"]
# JPEG = b64decode(retrData)

# image = cv2.imdecode(np.frombuffer(JPEG,dtype=np.uint8), cv2.IMREAD_COLOR)
# cv2.imwrite('result10.jpg',image)