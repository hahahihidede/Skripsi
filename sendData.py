from base64 import b64encode, b64decode
import pyrebase
import glob
import os
import firebase


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

def sendData():
    folder = 'cropped'
    room = "L203"
    for img in glob.glob(folder + "/*.png"):
        with open(img, 'rb') as f:
                data = f.read()

        str = b64encode(data).decode('UTF-8')
        db.child("image").push({'data': str})
        db.child("room").push({'data': room})
        db.child('room').push({'data': room})      
sendData()
