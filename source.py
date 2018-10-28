#https://piwars.org/2019-competition/challenges/
from time import sleep

class Robot:
    def __init__(self, motors, rangeSensors, webcam):
        self._motors = motors
        self._rangeSensors = rangeSensors
        self._webcam = webcam

    def showMotors(self):
        for motor in self._motors:
            print(motor)

    def showRangeSensors(self):
        for rangeSensor in self._rangeSensors:
            print(rangeSensor)

    def diagnostics(self):
        print("Motors: ")
        self.showMotors()
        print("Range sensors: ")
        self.showRangeSensors()

        self.forward(10)
        self.backward(10)
        self.left(360)
        self.right(360)

    def forward(self, distance):
        pass

    def backward(self, distance):
        pass

    def left(self, angle):
        pass

    def right(self, angle):
        pass

    def doCanyonsOfMars(self):
        #Use the left hand follow to solve the maze
        pass

    def doNebula(self):
        #Use image classifier to find positions on first run
        #Store and re-use positions for 2nd and 3rd runs
        pass

    def doBlastOff(self):
        #Drive in a straight line, at full speed
        pass

    def RCControl(self):
        #RC control
        pass


class NerfGun(Robot):
    def __init__(self):
        pass


class Webcam(Robot):
    def __init__(self):
        pass


class ColourClassifier():
    def __init__(self):
        pass


class RangeSensor(Robot):
    def __init__(self, number, pins):
        self._number = number
        self._pins = pins
        self.config()

    def config(self):
        #Do any necessary setup to allow the sensor to be read from
        for pin in self._pins:
            pass

    def getNumber(self):
        return self._number

    def getPins(self):
        return self._pins

    def read(self):
        #Read from the sensor
        return None

    def __repr__(self):
        return "Ultrasonic range sensor #{}, on pins: {}".format(
            self.getNumber(),
            self.getPins(),
        )


class Motor(Robot):
    def __init__(self, number, pins, offset):
        self._number = number
        self._pins = pins
        self._offset = offset
        self._direction = 1
        self.config()

    def config(self):
        #Do any necessary setup to allow the motor to be driven
        for pin in self._pins:
            pass

    def drive(self, speed):
        #Drive motor at given speed using PWM
        #Implement h-bridge to do bi-directionality
        offsetSpeed = speed / self._offset

    def stop(self):
        #Stop the motor
        pass

    def getNumber(self):
        return self._number

    def getPins(self):
        return self._pins

    def getOffest(self):
        return self._offset

    def setOffest(self, offset):
        self._offset = offset

    def getDirection(self):
        return self._direction

    def reverseDirection(self):
        self._direction *= -1

    def __repr__(self):
        return "Motor #{}, on pins: {}, with speed offset {}".format(
            self.getNumber(),
            self.getPins(),
            self.getOffest(),
        )


def main():
    Motor1 = Motor(number=1,pins=[16,18,22],offset=1)
    Motor2 = Motor(number=2,pins=[24,26,30],offset=1)
    motors = [Motor1, Motor2]

    RangeSensor1 = RangeSensor(number=1, pins=[11,12,13,14])
    rangeSensors = [RangeSensor1]

    Webcam1 = Webcam()

    BobbyTables = Robot(motors=motors, rangeSensors=rangeSensors, webcam=Webcam1)
    BobbyTables.diagnostics()

if __name__ == "__main__":
    exit(main())
