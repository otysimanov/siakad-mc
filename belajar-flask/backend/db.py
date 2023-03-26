import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)


db = firestore.client()

import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyDpKXdBaE9xQ_JJr5oiwNZ_THVc39yR4EM",
    "authDomain": "siakad18-ee235.firebaseapp.com",
    "databaseURL": "https://siakad18-ee235-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "siakad18-ee235",
    "storageBucket": "siakad18-ee235.appspot.com",
    "messagingSenderId": "196494079081",
    "appId": "1:196494079081:web:e88d3e56b53e7c2c79def8"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()