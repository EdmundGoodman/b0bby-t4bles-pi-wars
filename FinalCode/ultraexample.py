#!/usr/bin/python
import RPi.GPIO as GPIO
import ThunderBorg3
import time
GPIO.setmode(GPIO.BCM)
class Motors:
	def __init__(self):
		self.ZB = ThunderBorg3.ThunderBorg()
		self.ZB.Init()
		self.LeftSpeed = 0
		self.RightSpeed = 0
	def Turn(self,power):
		self.ZB.SetMotor1(power)
		self.ZB.SetMotor2(power)
		self.RightSpeed = power
		self.LeftSpeed = power
	def Forward(self,speed1,speed2):
		self.ZB.SetMotor1(speed1)
		self.ZB.SetMotor2(-speed2)
		self.RightSpeed = speed1
		self.LeftSpeed = -speed2
	def Stop(self):
		self.ZB.SetMotor1(0)
		self.ZB.SetMotor2(0)
		self.RightSpeed = 0
		self.LeftSpeed = 0
	def Inc(self,IncR,IncL):
		self.RightSpeed += IncR
		self.LeftSpeed += IncL
		self.ZB.SetMotor1(self.RightSpeed)
		self.ZB.SetMotor2(self.LeftSpeed)

class Ultra:
	def __init__(self,Echo,Trigger):
		self.Echo = Echo
		self.Trigger = Trigger
		GPIO.setup(self.Echo,GPIO.IN)
		GPIO.setup(self.Trigger, GPIO.OUT)
	def Distance(self):

		GPIO.output(self.Trigger, GPIO.LOW)

		time.sleep(0.05)

		GPIO.output(self.Trigger, GPIO.HIGH)

		time.sleep(0.00001)

		GPIO.output(self.Trigger, GPIO.LOW)

		while GPIO.input(self.Echo)==0:
			pulse_start_time = time.time()
		while GPIO.input(self.Echo)==1:
			pulse_end_time = time.time()

		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)
		return int(distance)



FrontLeft = Ultra(17,4)
FrontRight = Ultra(21,22)
FrontLeftSide = Ultra(26,27)
BackLeftSide = Ultra(20,23)
FrontRightSide = Ultra(6,18)
BackRightSide = Ultra(16,24)
M = Motors()


M.Forward(0.5,0.5)
try:
	while True:
		ChangeInSpeed = 0.5
		FL = FrontLeftSide.Distance()
		BL = BackLeftSide.Distance()
		if FL < 40 and BL < 40:
			print(ChangeInSpeed)
			ChangeInSpeed += (FL-BL)*1
		M.Forward(0.5,ChangeInSpeed)
finally:
	M.Stop()
	GPIO.cleanup()
