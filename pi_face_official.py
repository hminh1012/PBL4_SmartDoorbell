from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import os
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import apa102
import threading
import os
from threading import Thread
import subprocess
import signal

#Set up User Button, connected to GPIO17
BUTTON = 17 #GPIO17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)

#Set up thu vien cho den RGB LED: 3 APA102 RGB LEDs, connected to SPI interface
try:
    import queue as Queue
except ImportError:
    import Queue as Queue
    
class Pixels:
    PIXELS_N = 3

    def __init__(self):
        self.basis = [0] * 3 * self.PIXELS_N
        self.basis[0] = 2
        self.basis[3] = 1
        self.basis[4] = 1
        self.basis[7] = 2

        self.colors = [0] * 3 * self.PIXELS_N
        self.dev = apa102.APA102(num_led=self.PIXELS_N)

        self.next = threading.Event()
        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def wakeup(self, direction=0):
        def f():
            self._wakeup(direction)

        self.next.set()
        self.queue.put(f)

    def listen(self):
        self.next.set()
        self.queue.put(self._listen)

    def think(self):
        self.next.set()
        self.queue.put(self._think)

    def speak(self):
        self.next.set()
        self.queue.put(self._speak)

    def off(self):
        self.next.set()
        self.queue.put(self._off)

    def _run(self):
        while True:
            func = self.queue.get()
            func()

    def _wakeup(self, direction=0):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _listen(self):
        for i in range(1, 25):
            colors = [i * v for v in self.basis]
            self.write(colors)
            time.sleep(0.01)

        self.colors = colors

    def _think(self):
        colors = self.colors

        self.next.clear()
        while not self.next.is_set():
            colors = colors[3:] + colors[:3]
            self.write(colors)
            time.sleep(0.2)

        t = 0.1
        for i in range(0, 5):
            colors = colors[3:] + colors[:3]
            self.write([(v * (4 - i) / 4) for v in colors])
            time.sleep(t)
            t /= 2

        # time.sleep(0.5)
        self.colors = colors

    def _speak(self):
        colors = self.colors
        gradient = -1
        position = 24

        self.next.clear()
        while not self.next.is_set():
            position += gradient
            self.write([(v * position / 24) for v in colors])

            if position == 24 or position == 4:
                gradient = -gradient
                time.sleep(0.2)
            else:
                time.sleep(0.01)

        while position > 0:
            position -= 1
            self.write([(v * position / 24) for v in colors])
            time.sleep(0.01)

        # self._off()

    def _off(self):
        self.write([0] * 3 * self.PIXELS_N)

    def write(self, colors):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(colors[3*i]), int(colors[3*i + 1]), int(colors[3*i + 2]))

        self.dev.show()
	
# Ham phat ra am thanh
def play_sound(path):
	os.system('aplay ' + path)
	
# Set up cai tham so de? dieu khien den` LED
pixels = Pixels()
pixels_status = True
alarmed_think = False
alarmed_wakeup = False



# Khoi tao cac module detect mat 
face_detect = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Dem so frame co mat nguoi
face_frames = 0
noface_frames = 0

# Threshold so frame lien tuc co nguoi va khong co nguoi, fps xap xi la 20
max_face_frames = 200 #cu' 10s lien tuc co' mat. nguoi` se~ phat' alarm
max_noface_frames = 300 #cu' 15s lien tuc khong co mat nguoi se~ reset tat ca tham so 

# First time
first_time = True

# Check xem da canh bao hay chua
alarmed = False

# Doc tu camera
# vs = VideoStream(src=0).start()
# time.sleep(1.0)
cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"format": 'RGB888', "size": (640, 480)}))
# Start the camera
cam.start()
time.sleep(0.1)
pixels.off()
call_jitsi = False

while True:

	# Doc tu camera
	frame = cam.capture_array()

	# Resize de tang toc do xu ly
	frame = imutils.resize(frame, width=450)

	# Chuyen ve gray
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect cac mat trong anh
	faces = face_detect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100),		flags=cv2.CASCADE_SCALE_IMAGE)

	# Duyet qua cac mat
	for (x, y, w, h) in faces:
		first_time = False
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) #ve~ label tren mat.
		
		#Phat' hien. mat. lan` dau`
		if face_frames <= 0.5:
		    pixels.wakeup()
		    cam.capture_file("buglarly.jpg")
		    #os.system('aplay first_time.wav') # phat' am^ thanh chao` quy' khach'
		    wav_path = "first_time.wav"
		    t = Thread(target=play_sound, args=(wav_path,)) # Tien hanh phat am thanh trong 1 luong rieng
		    t.deamon = True
		    t.start()
		face_frames += 1
		noface_frames = 0
		if face_frames >= max_face_frames:
			if not alarmed:
				alarmed = True
				if not alarmed_think:
					alarmed_think = True
					alarmed_wakeup = False
					pixels.speak() # nhay' den`
					cam.capture_file("buglarly.jpg")
					os.system('aplay alarm.wav')	# phat am thanh canh bao
					#wav_path = "alarm.wav"
					#t = Thread(target=play_sound, args=(wav_path,)) # Tien hanh phat am thanh trong 1 luong rieng
					#t.deamon = True
					#t.start
					#time.sleep(2.5)
					os.system('python testCloud_image.py') #gui? anh? len cloud
											    
	#Neu' khong phai? lan` dau` va` da~ tat' den` thi` bat. den`, neu khong thi` tat' den`
	if not first_time:		
	    if not alarmed_wakeup:
		    alarmed_wakeup = True
		    alarmed_think = False
		    pixels.wakeup() # Bat^. Den`
	else:
	    pixels.off()
	
	#Hien. chu~ tren man` hinh`
	cv2.putText(frame, "Face Detected: {:.3f}".format(face_frames/30), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	cv2.putText(frame, "No Face Detected: {:.3f}".format(noface_frames/30), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2, cv2.LINE_AA,)
	noface_frames += 1
	
	if noface_frames >= max_noface_frames: # Sau khoang? thoi` gian max_noface_frames thi` reset het' chi? so' ve` mac dinh
		face_frames = 0
		alarmed = False
		first_time = True
		alarmed_think = False
		alarmed_wakeup = False

	#Khi khach' hang` nhan' nut' se~ bat. chuong va` thoat' khoi? vong` lap.
	state = GPIO.input(BUTTON)
	if not state:# Button pressed
	    print("button on")
	    os.system('aplay ring_bell.wav') #bat chuong
	    #wav_path = "please_wait.wav"
	    #t = Thread(target=play_sound, args=(wav_path,)) # Tien hanh phat am thanh trong 1 luong rieng
	    #t.deamon = True
	    #t.start
	    pixels.off()
	    time.sleep(0.1)  # Small delay to debounce button
	    call_jitsi = True
	    break	
		
	# Hien thi len man hinh
	cv2.imshow("Camera", frame)

	# Bam Esc de thoat
	key = cv2.waitKey(1) & 0xFF	
	if key == 27:
	    pixels.off()
	    break
	    
#Reset camera     
cv2.destroyAllWindows()
cam.stop()
#Chuyen sang chay file doorbell_official.py de goi cho chu? nha`
if call_jitsi == True:
    subprocess.Popen(["python", "doorbell_official.py"])
    pid = os.getpid()
    call_jitsi = False
    os.kill(pid, signal.SIGTERM)


	    
