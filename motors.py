#https://business.tutsplus.com/tutorials/controlling-dc-motors-using-python-with-a-raspberry-pi--cms-20051

import RPi.GPIO as GPIO
from time import sleep

class Robot:
    def __init__(self):
        self._position = [0,0]

class Motor(Robot):
    def __init__(self,motorPins):
        self._motorPins = motorPins
        self.configMotor()

    def configMotor(self):
        for pin in self._motorPins:
            GPIO.setup(pin,GPIO.OUT)

    def driveMotor(self):
        print("Turning motor on pins: {} on".format(self._motorPins))
        GPIO.output(self._motorPins[0],GPIO.HIGH)
        GPIO.output(self._motorPins[1],GPIO.LOW)
        GPIO.output(self._motorPins[2],GPIO.HIGH)

    def stopMotor(self):
        print("Stopping motor on pins: {}".format(self._motorPins))
        GPIO.output(self._motorPins[2],GPIO.LOW)


def main():
    BobbyTables = Robot()
    Motor1 = Motor([16,18,22])
   
    Motor1.driveMotor()
    sleep(2)
    Motor1.stopMotor()

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    main()
    GPIO.cleanup()
