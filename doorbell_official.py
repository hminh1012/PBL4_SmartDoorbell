import RPi.GPIO as GPIO
import subprocess
import os
import signal
import time
import uuid
import firebase

call_face = False
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
link = "http://meet.jit.si/"+str(chat_id)

data = {"Link_Jitsi_Meet": link}
db.child("Status").set(data)
# Add a 5-second delay between pushes
time.sleep(1)
print(data)


BUTTON = 17
DEBOUNCE_TIME = 0.2  # Debounce time in seconds
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up to handle button state reliably

class VideoChat:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._process = None

    def get_chat_url(self):
        return f"http://meet.jit.si/{self.chat_id}"

    def start(self):
        if not self._process:
            print(f"Accessing Jitsi room: {self.get_chat_url()}")
            self._process = subprocess.Popen(["firefox", "--kiosk", self.get_chat_url()])
        else:
            print("Video chat already started.")

    def end(self):
        if self._process:
            os.kill(self._process.pid, signal.SIGTERM)
            self._process = None
            print("Video chat ended.")

def jitsi():
    video_chat = VideoChat(chat_id)
    print("Ready for button press.")
    video_chat.start()

    try:
        while True:
            state = GPIO.input(BUTTON)
            if not state:  # Button pressed
                print("Button pressed.")
                time.sleep(DEBOUNCE_TIME)  # Debounce delay

                print("Ending video chat...")
                call_face = True
                #if call_face == True:                          
                    #pid_jitsi = os.getpid()
                    #call_face = False
                    #time.sleep(1)
                    #os.kill(pid_jitsi, signal.SIGTERM)
                    #subprocess.Popen(["python", "pi_face_official.py"])  
                video_chat.end()
                break  # Exit the loop after ending the chat

            time.sleep(0.1)  # Polling delay
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        GPIO.cleanup()
        if video_chat._process:
            video_chat.end()
        print("Program exited.")

if __name__ == "__main__":
    jitsi()

        
