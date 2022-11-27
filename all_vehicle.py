from imutils.video import VideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy.core.multiarray
import numpy as np
import argparse
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import time
import cv2
import os
import dlib
import time
import threading
import math
import json
import requests
from requests.auth import HTTPBasicAuth
from websocket import create_connection
import argparse
import sys
import os
#from pushbullet.pushbullet import PushBullet
from requests.exceptions import HTTPError
from requests.exceptions import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import winsound
import sqlite3
#import playsound
HOST = "https://api.pushbullet.com/v2"


class PushBullet():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def _request(self, method, url, postdata=None, params=None, files=None):
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "User-Agent": "pyPushBullet"}

        if postdata:
            postdata = json.dumps(postdata)

        r = requests.request(method,
                             url,
                             data=postdata,
                             params=params,
                             headers=headers,
                             files=files,
                             auth=HTTPBasicAuth(self.apiKey, ""))

        r.raise_for_status()
        return r.json()

    def getDevices(self):
        """ Get devices
            https://docs.pushbullet.com/v2/devices

            Get a list of devices, and data about them.
        """

        return self._request("GET", HOST + "/devices")["devices"]

    def pushNote(self, recipient, title, body, recipient_type="device_iden"):

        data = {"type": "note",
                "title": title,
                "body": body}

        data[recipient_type] = recipient
        #data['title']="Threat Detected"

        return self._request("POST", HOST + "/pushes", data)

#labelsPath = os.path.sep.join([args["yolo"], "coco.names"])

def database(num):
	conn = sqlite3.connect('Vehicle_DB.db') 
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS RecordONE (Number REAL, Name TEXT)')
	name = "Vehicles Log"
	c.execute("INSERT INTO RecordONE (Number, Name) VALUES(?, ?)", (num, name))
	conn.commit()
	c.close() 
	conn.close()
def estimateSpeed(location1, location2):
	d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2))
	# ppm = location2[2] / carWidht
	ppm = 8.8
	d_meters = d_pixels / ppm
	#print("d_pixels=" + str(d_pixels), "d_meters=" + str(d_meters))
	fps = 18
	speed = d_meters * fps * 3.6
	return speed
	

def trackMultipleObjects(video):
	rectangleColor = (0, 255, 0)
	frameCounter = 0
	currentCarID = 0
	fps = 0
	
	carTracker = {}
	carNumbers = {}
	carLocation1 = {}
	carLocation2 = {}
	speed = [None] * 1000
	u=[]
	z=[]
	# Write output to video file
	#out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (WIDTH,HEIGHT))


	while True:
		start_time = time.time()
		rc, image = video.read()
		if type(image) == type(None):
			break
		
		image = cv2.resize(image, (WIDTH, HEIGHT))
		resultImage = image.copy()
		Y_THRESH = 290
		cv2.line(resultImage,(0, Y_THRESH),(1280, Y_THRESH),(255,0,0),2)
		frameCounter = frameCounter + 1
		
		carIDtoDelete = []
		
		for carID in carTracker.keys():
			trackingQuality = carTracker[carID].update(image)
			
			if trackingQuality < 7:
				carIDtoDelete.append(carID)
				
		for carID in carIDtoDelete:
			print ('Removing carID ' + str(carID) + ' from list of trackers.')
			print ('Removing carID ' + str(carID) + ' previous location.')
			print ('Removing carID ' + str(carID) + ' current location.')
			carTracker.pop(carID, None)
			carLocation1.pop(carID, None)
			carLocation2.pop(carID, None)
		
		if not (frameCounter % 10):
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24))
			
			for (_x, _y, _w, _h) in cars:
				x = int(_x)
				y = int(_y)
				w = int(_w)
				h = int(_h)
			
				x_bar = x + 0.5 * w
				y_bar = y + 0.5 * h
				
				matchCarID = None
			
				for carID in carTracker.keys():
					trackedPosition = carTracker[carID].get_position()
					
					t_x = int(trackedPosition.left())
					t_y = int(trackedPosition.top())
					t_w = int(trackedPosition.width())
					t_h = int(trackedPosition.height())
					
					t_x_bar = t_x + 0.5 * t_w
					t_y_bar = t_y + 0.5 * t_h
				
					if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))):
						matchCarID = carID
				
				if matchCarID is None:
					print ('Creating new tracker ' + str(currentCarID))
					
					tracker = dlib.correlation_tracker()
					tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))
					
					carTracker[currentCarID] = tracker
					carLocation1[currentCarID] = [x, y, w, h]

					currentCarID = currentCarID + 1
		
		#cv2.line(resultImage,(0,480),(1280,480),(255,0,0),5)


		for carID in carTracker.keys():
			trackedPosition = carTracker[carID].get_position()
					
			t_x = int(trackedPosition.left())
			t_y = int(trackedPosition.top())
			t_w = int(trackedPosition.width())
			t_h = int(trackedPosition.height())
			
			cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4)
			
			# speed estimation
			carLocation2[carID] = [t_x, t_y, t_w, t_h]
		
		end_time = time.time()
		
		if not (end_time == start_time):
			fps = 1.0/(end_time - start_time)
		
		#cv2.putText(resultImage, 'FPS: ' + str(int(fps)), (620, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


		for i in carLocation1.keys():	
			if frameCounter % 1 == 0:
				[x1, y1, w1, h1] = carLocation1[i]
				[x2, y2, w2, h2] = carLocation2[i]
		
				# print 'previous location: ' + str(carLocation1[i]) + ', current location: ' + str(carLocation2[i])
				carLocation1[i] = [x2, y2, w2, h2]
		
				# print 'new previous location: ' + str(carLocation1[i])
				if [x1, y1, w1, h1] != [x2, y2, w2, h2]:
					if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285:
						speed[i] = estimateSpeed([x1, y1, w1, h1], [x2, y2, w2, h2])
						if int(speed[i])>65:
							winsound.PlaySound('speed_car_sound.wav', winsound.SND_FILENAME)
							u.append(speed[i])
							cv2.imwrite('speeding_%s.png' % i, resultImage)
							options = Options()
							options.add_argument("--use-fake-ui-for-media-stream")
							timeout = 20
							driver = webdriver.Chrome(executable_path = 'D:/project/computervision/garbage detection/pyPushBullet-master/chromedriver_win32/chromedriver.exe', chrome_options=options)
							driver.get("https://mycurrentlocation.net/")
							wait = WebDriverWait(driver, timeout)
							longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
							longitude = [x.text for x in longitude]
							longitude = str(longitude[0])
							latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
							latitude = [x.text for x in latitude]
							latitude = str(latitude[0])
							driver.quit()
							m=(latitude,longitude)
							num=speed[i]
							database(num)
							z.append(m)
					#if y1 > 275 and y1 < 285:
					if speed[i] != None and y1 >= 180:
						cv2.putText(resultImage, str(int(speed[i])) + " km/hr", (int(x1 + w1/2), int(y1-5)),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
						#winsound.PlaySound('speed_car_sound.wav', winsound.SND_FILENAME) 
					#print ('CarID ' + str(i) + ': speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')

					#else:
					#	cv2.putText(resultImage, "Far Object", (int(x1 + w1/2), int(y1)),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

						#print ('CarID ' + str(i) + ' Location1: ' + str(carLocation1[i]) + ' Location2: ' + str(carLocation2[i]) + ' speed is ' + str("%.2f" % round(speed[i], 0)) + ' km/h.\n')
		cv2.imshow('result', resultImage)
		# Write the frame into the file 'output.avi'
		#out.write(resultImage)


		key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	
	cv2.destroyAllWindows()
	return u,z
carCascade = cv2.CascadeClassifier('myhaar.xml')
video = cv2.VideoCapture('cars.mp4')

WIDTH = 1280
HEIGHT = 720
x,z=trackMultipleObjects(video)

def getDevices(args):
    p = PushBullet(args.api_key)
    devices = p.getDevices()
    if args.json:
        print(json.dumps(devices))
        return
    for device in devices:
        if "manufacturer" in device:
            print("%s %s %s" % (device["iden"],
                            device["manufacturer"],
                            device["model"]))
        else:
            print(device["iden"])

def pushNote(args):
    p = PushBullet(args.api_key)
    args.title='Speed Limit Exceded'
    args.body='Speed recorded more than 65 km/h and their respective coordinates are:'+str(x)+"...."+str(z)

    note = p.pushNote(args.device, args.title, " ".join(args.body))
    if args.json:
        print(json.dumps(note))
        return
    if args.device and args.device[0] == '#':
        print("Note broadcast to channel %s" % (args.device))
    elif not args.device:
        print("Note %s sent to all devices" % (note["iden"]))
    else:
        print("Note %s sent to %s" % (note["iden"], note["target_device_iden"]))



parser = argparse.ArgumentParser()
parser.add_argument("--json", default=False, action="store_const", const=True)
parser.add_argument("api_key")
subparser = parser.add_subparsers(dest="type")

getdevices = subparser.add_parser("getdevices", help="Get a list of devices")
getdevices.set_defaults(vars=getDevices)


note = subparser.add_parser("note", help="Send a note")
note.add_argument('device', type=str, help="Device ID")
#note.add_argument('title')
#note.add_argument('body', nargs=argparse.REMAINDER)
note.set_defaults(vars=pushNote)
args = parser.parse_args()
args.vars(args)
