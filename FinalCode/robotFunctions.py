#SetupSensors
import RPi.GPIO as GPIO
import ThunderBorg3
import time
GPIO.setmode(GPIO.BCM)
import xbox
import logging
import sys
from Adafruit_BNO055 import BNO055
import io
import picamera
from PIL import Image
import numpy as np
import atexit

class Compass:
	def __init__(self):
		self.started = False
	def Start(self):
		if not self.started:
			operational = False
			self.bno = BNO055.BNO055(serial_port='/dev/serial0')
			for i in range(10):
				try:
					if not self.bno.begin():
						raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')
					else:
						operational = True
						break
				except RuntimeError:
					pass
			if not operational:
				raise RuntimeError('Cant connect to compass after 10 attempts')
			self.started = True
	def Calibrate(self):
		for i in range(100):
			print(self.CalibValues)

	def ShowLED(self):
		sys, gyro, accel, mag = self.CalibValues
		if sys == 3:
			robot.controller.TopRightOn()
		else:
			robot.controller.TopRightOff()
		if gyro == 3:
			robot.controller.BottomLeftOn()
		else:
			robot.controller.BottomeLeftOff()
		if accel == 3:
			robot.controller.BottomRightOn()
		else:
			robot.controller.BottomRightOff()
		if mag == 3:
			robot.controller.TopRightOn()
		else:
			robot.controller.TopRightOff()

	def Heading(self):
		# Read the Euler angles for heading, roll, pitch (all in degrees).
		heading = 0
		while heading == 0:
			heading, roll, pitch = self.bno.read_euler()
		#sys, gyro, accel, mag = bno.get_calibration_status()
		return heading
	def Calibrated(self):
		sys, gyro, accel, mag = self.bno.get_calibration_status()
		return True if min([sys,gyro,accel,mag]) == 3 else False
	def CalibValues(self):
		sys, gyro, accel, mag = self.bno.get_calibration_status()
		return (sys,gyro,accel,mag)

	def Values():
		return bno.get_calibration()
	def SetValues(values):
		bno.set_calibration(values)


rTotal = 0
bTotal = 0
gTotal = 0
class Camera:
	def __init__(self):
		import picamera
		self.started = False
	def start(self,res=(32,32),frate=80):
		if not self.started:
			self.cam=picamera.PiCamera()
			self.resolution=res
			#self.cam.resolution=res
			self.cam.framerate=frate
			time.sleep(2)
			self.started = True

	def DanielPhoto2(self, numPhotos=5):
		rTotal = 0
		gTotal = 0
		bTotal = 0
		count = 0
		stream = io.BytesIO()
		for foo in self.cam.capture_continuous(stream, format='jpeg' , resize=self.resolution, use_video_port=True):
			# Truncate the stream to the current position (in case
			# prior iterations output a longer image)
			stream.truncate()
			stream.seek(0)
			img = Image.open(stream)
			pixels = list(img.getdata())
			pixels = pixels[5*32:-16*32]
			for pixle in pixels:
				rTotal+=pixle[0]
				gTotal+=pixle[1]
				bTotal+=pixle[2]
			count += 1
			if count >= numPhotos:
				return (rTotal/numPhotos,gTotal/numPhotos,bTotal/numPhotos)

	def DanielPhoto(self, numPhotos):
		self.cam.resolution=self.resolution
		global rTotal
		global bTotal
		global gTotal
		rTotal = 0
		bTotal = 0
		gTotal = 0
		def outputs(numPhotos):
			global rTotal
			global bTotal
			global gTotal
			stream = io.BytesIO()
			for i in range(numPhotos):
				yield stream
				stream.seek(0)
				img = Image.open(stream)
				for pixle in list(img.getdata()):
					rTotal+=pixle[0]
					gTotal+=pixle[1]
					bTotal+=pixle[2]
				stream.seek(0)
				stream.truncate()

		self.cam.capture_sequence(outputs(numPhotos), 'jpeg', use_video_port=True)
		rTotal = rTotal/numPhotos
		gTotal = gTotal/numPhotos
		bTotal = bTotal/numPhotos
		return (rTotal,gTotal,bTotal)



class Ultra:
	def __init__(self,echo,trigger):
		self.echo = echo
		self.trigger = trigger
		GPIO.setup(self.echo,GPIO.IN)
		GPIO.setup(self.trigger, GPIO.OUT)

	def distance(self):
		GPIO.output(self.trigger, GPIO.LOW)
		time.sleep(0.05)
		GPIO.output(self.trigger, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(self.trigger, GPIO.LOW)
		while GPIO.input(self.echo)==0:
			pulse_start_time = time.time()
		while GPIO.input(self.echo)==1:
			pulse_end_time = time.time()

		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)
		return int(distance)

class Robot:
	def __init__(self):
		self.ultraFrontLeft = Ultra(17,4)
		self.ultraFrontRight = Ultra(21,22)
		self.ultraFrontLeftSide = Ultra(26,27)
		self.ultraBackLeftSide = Ultra(20,23)
		self.ultraFrontRightSide = Ultra(6,18)
		self.ultraBackRightSide = Ultra(16,24)
		self.ZB = ThunderBorg3.ThunderBorg()
		self.ZB.Init()
		self.leftSpeed = 0
		self.rightSpeed = 0
		try:
			self.controller=xbox.Joystick()
			#self.controller.startstart()
		except:
			pass
		self.camera=Camera()
		self.compass=Compass()




	def setController(controller):
		self.controller=controller
		self.camera.cam.close()

	def shutdown(self):
		GPIO.cleanup()
		try:
			self.controller.close()
			self.camera.cam.close()
		except:
			pass
		print("Processes Safely Stopped")

	def turn(self,power):
		self.forward(power,-power)

	def forward(self,speed1,speed2):
		self.ZB.SetMotor1(speed1)
		self.ZB.SetMotor2(-speed2)
		self.RightSpeed = speed2
		self.LeftSpeed = speed1

	def SoftStop(self,time = 0.5):
		DecL = (self.LeftSpeed/100) * -1
		DecR = (self.RightSpeed/100) * -1
		for i in range(100):
			inc(DecL, DecR)
			sleep(time/100)
	def stop(self):
		self.forward(0,0)

	def inc(self,IncL,IncR):
		if self.rightSpeed + IncR > 1 or self.rightSpeed + IncR < -1 or self.leftSpeed + IncL > 1 or self.leftSpeed < -1:
			raise Exception("Cant increment motors above 1 or below -1")
		self.rightSpeed += IncR
		self.leftSpeed += IncL
		self.forward(self.leftSpeed,self.rightSpeed)

	def TurnDegrees(Degrees):
			SlowestTurningSpeed = 0.3 # Need to find out SlowestTurningSpeed
			EndDeg = (self.compass.Heading() + Degrees) % 360

			while True:
				heading = self.Heading()
				if abs(180-abs(180-abs(heading-EndDeg))) < 5:
						self.SoftStop()
						break

				LeftToTurn = (EndDeg - heading) % 360
				LeftToTurn = (((LeftToTurn-0)/(180-0)) * (1-SlowestTurningSpeed)) + SlowestTurningSpeed
				self.turn(LeftToTurn)

	def getSpeed():
		return (self.leftSpeed,self.rightSpeed)

	def softEval(self, val1,val2):
	    return val1/val2<1.4 and val1/val2>0.7

	def classify(self, r,g,b):
	    m=r
	    r,g,b=r/m,g/m,b/m
	    if g>r and not softEval(g,r):
	        return "green"

	    elif r>g and not softEval(r,g) and r>b and not softEval(r,b):
	        return "red"
	    elif b>r and not softEval(b,r) and b>g and not softEval(b,g):
	        return "blue"
	    elif r>b and not softEval(r,b) and g>b and not softEval(g,b):
	        return "yellow"
	    else:
	        return "black"
robot=Robot()
atexit.register(robot.shutdown) #GREAT LINE
'''import io
import time
import picamera
with picamera.PiCamera() as camera:
stream = io.BytesIO()
for foo in camera.capture_continuous(stream, format='jpeg'):
# Truncate the stream to the current position (in case
# prior iterations output a longer image)
stream.truncate()
stream.seek(0)
if process(stream):
break '''
