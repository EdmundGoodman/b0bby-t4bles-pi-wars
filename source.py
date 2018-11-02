from collections import Counter
from time import sleep
from PIL import Image
import cv2


class Robot:
    def __init__(self, name, motors, rangeSensors, webcam, compass, nerfGun, imgClassifier):
        self._name = name
        self._motors = motors
        self._rangeSensors = rangeSensors
        self._webcam = webcam
        self._compass = compass
        self._nerfGun = nerfGun
        self._classifier = imgClassifier

    def showMotors(self):
        for motor in self._motors:
            print(motor)

    def showRangeSensors(self):
        for rangeSensor in self._rangeSensors:
            print(rangeSensor)

    def showPeripherals(self):
        print(self._webcam)
        print(self._compass)
        print(self._nerfGun)

    def showSoftware(self):
        print(self._classifier)

    def diagnostics(self):
        print("Diagnostics for \"{}\": ".format(self))
        print("Motors: ")
        self.showMotors()
        print("Range sensors: ")
        self.showRangeSensors()
        print("Periperals: ")
        self.showPeripherals()
        print("Software: ")
        self.showSoftware()

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

    def doCanyonsOfMars(self, step=5, threshold=100):
        #Use the right hand follow to solve the maze
        while True:
            #Check for alien sign, then do output
            img = self._webcam.read()
            if self._classifier.classifyColour(img) == "green":
                print("Alien!") # Do an output

            sensorValues = [self._rangeSensors[i].read() for i in range(4)]
            #Check for exit condition: open on all four sides?
            if min(sensorValues) > threshold:
                break

            #Try to turn right
            if sensorValues[2] > threshold:
                self.right(90)
                self.forward(step)
            #Try to go forward
            elif sensorValues[1] > threshold:
                self.forward(step)
            #Try to turn left
            elif sensorValues[0] > threshold:
                self.left(90)
                self.forward(step)
            #Go back
            elif sensorValues[3] > threshold:
                self.backward(step)
            else:
                #There is nowhere to turn... Bobby Tables has fallen in the callous canyons of Mars
                break


    def doNebula(self, targetOrder=["red","green","blue","yellow"], step=5, threshold=50):
        #To do, add pathing, so it doesn't return to the center each time

        #Use image classifier to find positions on first run
        #Store and re-use positions for 2nd and 3rd runs

        #Turn by 45 degrees, then 4 times by 90, to look at each of the 4 corners
        self.right(45)
        colours = []
        for _ in range(4):
            img = self._webcam.read()
            colours.append(self._classifier.classifyColour(img))
            self.right(90)

        targetOrder=["red","blue","green","yellow"]

        for i in range(4):
            #Turn to ith colour
            targetNumber = colours.index(targetOrder[i])
            if targetNumber == 0:
                pass
            elif targetNumber == 1:
                self.right(90)
            elif targetNumber == 2:
                self.right(180)
            else:
                self.left(90)

            #Drive until crash
            count = 0
            while True:
                if self._rangeSensors[1] < threshold:
                    break
                self.forward(step)
                count += 1

            #Turn around
            self.right(180)
            #Drive back to the centre
            self.forward(step*count)

            #Turn back to original position
            if targetNumber == 0:
                self.right(180)
            elif targetNumber == 1:
                self.right(90)
            elif targetNumber == 2:
                pass
            else:
                self.left(90)

        #Do the run another two times

    def doBlastOff(self, length=7500):
        #Drive in a straight line, at full speed
        #Stateful control with compass, and stop at end
        self.forward(length)

    def RCControl(self):
        #RC control
        pass

    def __repr__(self):
        return "{}".format(self._name)




class ImageClassifier:
    def __init__(self, DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE):
        self.roundBase = ROUNDBASE
        self.distanceThreshold = DISTANCE_THRESHOLD
        self.numberPixelThreshold = NUMBER_PIXEL_THRESHOLD

    def getBaseColour(self, rgb_tuple):
        def getManhattanDistance(x,y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

        colours = {
            "red": (255, 0, 0),
            "green" : (0,255,0),
            "blue" : (0,0,255),
            "yellow": (255,255,0),
            "white" : (255,255,255),
            "black" : (0,0,0),
        }
        distances = {k: getManhattanDistance(v, rgb_tuple) for k, v in colours.items()}
        color = min(distances, key=distances.get)
        return color #, distances[color]

    def classifyColour(self, img):
        #Reduce colour depth
        img = img.point(lambda x: int(x/self.roundBase)*self.roundBase)
        pixels = img.getdata()
        #Count pixels & reject outliers
        pixelsCount = Counter(pixels)
        for k in list(pixelsCount):
            if pixelsCount[k] < self.numberPixelThreshold:
                del pixelsCount[k]
        #Classify colour based on getManhattanDistance distance from component colours
        colourValues = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
        for pixels,number in pixelsCount.items():
            colour = self.getBaseColour(pixels)
            if colour in colourValues.keys():
                colourValues[colour] += number
        #Return the most prevalent colour
        colour = max(colourValues, key=colourValues.get)
        return colour

    def __repr__(self):
        return "\tImage classifier" #include properties?




class Component:
    def __init__(self, pins, number):
        self._pins = pins
        self._number = number

    def config(self):
        raise NotImplementedError

    def getPins(self):
        return self._pins

    def getNumber(self):
        return self._number

class Compass(Component):
    def __init__(self, pins, number):
        Component.__init__(self, pins, number)
        self.config()

    def config(self):
        pass

    def read(self):
        return None

    def __repr__(self):
        return "\tCompass on pins: {}".format(self.getPins())


class NerfGun(Component):
    def __init__(self, pins, number):
        Component.__init__(self, pins, number)
        self.config()

    def config(self):
        pass

    def revMotors(self):
        pass

    def fireDart(self):
        pass

    def __repr__(self):
        return "\tNerf gun on pins: {}".format(self._pins)


class Webcam(Component):
    def __init__(self, number):
        Component.__init__(self, None, number)
        self._cap = cv2.VideoCapture(0)
        self.config()

    def config(self):
        pass

    def read(self):
        _, frame =self._cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.reshape((frame.shape[0] * frame.shape[1],3))
        return frame

    def getCap(self):
        return self._cap

    def __repr__(self):
        return "\tWebcam"


class RangeSensor(Component):
    def __init__(self, pins, number):
        Component.__init__(self, pins, number)
        self.config()

    def config(self):
        pass

    def read(self):
        #Read from the sensor
        return None

    def __repr__(self):
        return "\tUltrasonic range sensor #{}, on pins: {}".format(
            self.getNumber(),
            self.getPins(),
        )

class Motor(Component):
    def __init__(self, pins, number, offset):
        Component.__init__(self, pins, number)
        self._offset = offset
        self._direction = 1
        self.config()

    def config(self):
        pass

    def drive(self, speed):
        #Drive motor at given speed using PWM
        #Implement h-bridge to do bi-directionality
        offsetSpeed = speed / self._offset

    def getOffest(self):
        return self._offset

    def setOffest(self, offset):
        self._offset = offset

    def getDirection(self):
        return self._direction

    def reverseDirection(self):
        self._direction *= -1

    def __repr__(self):
        return "\tMotor #{}, on pins: {}, with speed offset {}".format(
            self.getNumber(),
            self.getPins(),
            self.getOffest(),
        )





def main():
    Motor1 = Motor(pins=[],number=1,offset=1)
    Motor2 = Motor(pins=[],number=2,offset=1)
    motors = [Motor1, Motor2]

    RangeSensor1 = RangeSensor(pins=[],number=1)
    rangeSensors = [RangeSensor1]

    Webcam1 = Webcam(number=1)
    Compass1 = Compass(pins=[],number=1)
    NerfGun1 = NerfGun(pins=[],number=1)

    Classifier1 = ImageClassifier(
        DISTANCE_THRESHOLD=100,
        NUMBER_PIXEL_THRESHOLD=100,
        ROUNDBASE=20,
    )

    BobbyTables = Robot(
        name="Robert'); DROP TABLE Students; -- ",
        motors=motors,
        rangeSensors=rangeSensors,
        webcam=Webcam1,
        compass=Compass1,
        nerfGun=NerfGun1,
        imgClassifier=Classifier1,
    )
    BobbyTables.diagnostics()


if __name__ == "__main__":
    exit(main())
