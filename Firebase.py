import firebase
import random
import time
import uuid

chat_id = str(uuid.uuid4())

# Firebase configuration
config = {
  "apiKey": "AIzaSyAamS-omT7i-1fFFuwHr5k8_ILt0ptNl3E",
  "authDomain": "pidrowsiness-277a4.firebaseapp.com",
  "databaseURL": "https://pidrowsiness-277a4-default-rtdb.firebaseio.com",
  "projectId": "pidrowsiness-277a4",
  "storageBucket": "pidrowsiness-277a4.appspot.com",
  "messagingSenderId": "443787716450",
  "appId": "1:443787716450:web:c7033070895e50b0e56e3b",
  "measurementId": "G-KBBZSE34Y3"
}

# Instantiates a Firebase app
app = firebase.initialize_app(config)

db = app.database()

# File to store in storage
file_path = '/home/pi/PBL4/buglarly.jpg'

storage = app.storage()
storage.child('buglarly.jpg').put(file_path)
print('Send image successfully')
body = "http://meet.jit.si/"+str(chat_id)

while True:
  data = {
  "AlertTime": body,
    
  }

  db.child("Status").set(data)

  # Add a 5-second delay between pushes
  time.sleep(1)
  print(data)
