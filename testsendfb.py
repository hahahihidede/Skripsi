import numpy as np
import cv2
from base64 import b64encode, b64decode
import pyrebase
import glob
import os
from pathlib import Path
import json
from numpyencoder import NumpyEncoder

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

folder = 'bukti'
i = 0
for img in glob.glob(folder + "/*.png"):
        imgs = cv2.imread(img)
        with open(img, 'rb') as f:
                data = f.read()

        str = b64encode(data).decode('UTF-8')
        db.child("image").push({'data': str})