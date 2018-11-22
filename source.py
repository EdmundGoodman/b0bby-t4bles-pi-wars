from collections import Counter
from time import sleep, time
from PIL import Image
import numpy
import math
import cv2
import io

#import xbox

#Pi only libraries
try:
    import RPi.GPIO as GPIO
    import ThunderBorg3
    TB = ThunderBorg3.ThunderBorg()

    import Adafruit_LSM303
    lsm303 = Adafruit_LSM303.LSM303()

    from picamera import PiCamera
    camera = PiCamera()

    piOnlyLibraries = True
except ImportError:
    piOnlyLibraries = False

def cleanup():
    if piOnlyLibraries:
        camera.close()



class Robot:
    def __init__(self, name, leftMotors, rightMotors, rangeSensors, webcam, compass, nerfGun, imgClassifier):
        self._name = name
        self._leftMotors = leftMotors
        self._rightMotors = rightMotors
        self._rangeSensors = rangeSensors
        self._webcam = webcam
        self._compass = compass
        self._nerfGun = nerfGun
        self._classifier = imgClassifier

    def showMotors(self):
        print(self._leftMotors)
        print(self._rightMotors)

    def showRangeSensors(self):
        for rangeSensor in self._rangeSensors:
            print(rangeSensor)

    def showPeripherals(self):
        print(self._webcam)
        print(self._compass)
        print(self._nerfGun)

    def showSoftware(self):
        print(self._classifier)

    def getMotorVoltage(self):
        return TB.GetBatteryReading()

    def diagnostics(self):
        print("Diagnostics for \"{}\": ".format(self))
        print("Motors: ")
        self.showMotors()
        print("Motor voltage: {}".format(self.getMotorVoltage))
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

    def forward(self, speed):
        #Include code to statefully stay on fixed bearing
        self._leftMotors.drive(speed)
        self._rightMotors.drive(speed)

    def backward(self, speed):
        #Include code to statefully stay on fixed bearing
        self._leftMotors.drive(speed*-1)
        self._rightMotors.drive(speed*-1)

    def left(self, angle, tolerance=10):
        endAngle = (self._compass.read()-angle)%360
        while False: #Turn until the current angle is within a tolerance of the target angle
            self._leftMotors.drive(speed*-1)
            self._rightMotors.drive(speed)

    def right(self, angle, tolerance=10):
        endAngle = (self._compass.read()-angle)%360
        while False: #Turn until the current angle is within a tolerance of the target angle
            self._leftMotors.drive(speed)
            self._rightMotors.drive(speed*-1)

    def doCanyonsOfMars(self, step=5, threshold=100):
        #Use the right hand follow to solve the maze
        while True:
            #Check for alien sign, then do output
            img = self._webcam.read(library="PIL")
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
                print("There is nowhere to turn... Bobby Tables has fallen in the callous canyons of Mars")
                break


    def doNebula(self, targetOrder=["red","green","blue","yellow"], step=5, threshold=50):
        #To do, add pathing, so it doesn't return to the center each time

        #Use image classifier to find positions on first run
        #Store and re-use positions for 2nd and 3rd runs

        #Turn by 45 degrees, then 4 times by 90, to look at each of the 4 corners
        self.right(45)
        colours = []
        for _ in range(4):
            img = self._webcam.read(library="PIL")
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

    def remoteControl(self):
        #Remotely control the robot
        pass

    def __repr__(self):
        return "{}".format(self._name)




class ColourClassifier:
    def __init__(self, distanceThreshold, numberPixelThreshold, roundBase):
        self._roundBase = roundBase
        self._distanceThreshold = distanceThreshold
        self._numberPixelThreshold = numberPixelThreshold

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
        img = img.point(lambda x: int(x/self._roundBase)*self._roundBase)
        pixels = img.getdata()
        #Count pixels & reject outliers
        pixelsCount = Counter(pixels)
        for k in list(pixelsCount):
            if pixelsCount[k] < self._numberPixelThreshold:
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
        if piOnlyLibraries:
            accel, mag = lsm303.read()
            #Processing code in here
            return mag
        else:
            return 0

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
    def __init__(self, number, resolution, framerate):
        Component.__init__(self, None, number)
        #Add resolution param?
        self._resolution = resolution
        self._framerate = framerate
        self.config()

    def config(self):
        if piOnlyLibraries:
            camera.resolution = self._resolution
            camera.framerate = self._framerate

    def getResolution(self):
        return self._resolution

    def setResolution(self, resolution):
        self._resolution = resolution
        self.config()

    def getFramerate(self):
        return self._framerate

    def setFramerate(self, framerate):
        self._framerate = framerate
        self.config()

    def read(self, library="PIL"):

        if piOnlyLibraries:
            #Load the image
            if library=="PIL":
                stream = io.BytesIO()
                camera.capture(stream, format="bmp", use_video_port=True)
                frame = Image.open(io.BytesIO(stream))
            else: #cv2
                #camera.framerate = 24; sleep(2)
                frame = np.empty((240*320*3), dtype=np.uint8)
                camera.capture(frame, format="rgb", use_video_port=True)
                frame = frame.reshape((240,320,3))

                #Using the PIL Image frame
                #frame = numpy.array(frame)[:,:,::-1]

        else:
            print("Using test image, as webcam not available")
            frame = cv2.imread("images/alien.png")
            #Change the colour order from BGR to RGB for ease of use
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if library=="PIL":
                frame = Image.fromarray(frame)
            else: #cv2
                frame = frame.reshape((frame.shape[0] * frame.shape[1],3))

            """
            print("Using test image, as webcam not available")
            frame = Image.open("images/alien.png")
            print("Finished reading image")

            if library=="PIL":
                pass
            else: #cv2
                frame = np.array(Images)
            print("Finished casting image")

            """

        return frame

    def __repr__(self):
        return "\tWebcam with resolution: {} and framerate: {}".format(
            self.getResolution(),
            self.getFramerate(),
        )


class RangeSensor(Component):
    def __init__(self, pins, number, sleepTime=1):
        Component.__init__(self, pins, number)
        self._sleepTime = sleepTime #This num needs to be tinkered with and can be a lot smaller with slightly less reliable readings
        self.config()

    def config(self):
        if piOnlyLibraries:
            #Assumimg pins is an array of the actual number pin with first one being trigger and second being echo
            self._pinTrigger = self._pins[0]
            self._pinEcho = self._pins[1]
            GPIO.setup(self._pinTrigger, GPIO.OUT)
            GPIO.setup(self._pinEcho, GPIO.IN)

    def read(self):
        #Read from the sensor
        if piOnlyLibraries:
            try:
                sleep(self._sleepTime)
                GPIO.output(self._pinTrigger, GPIO.HIGH)
                sleep(0.00001)
                GPIO.output(self._pinTrigger, GPIO.LOW)
                while GPIO.input(self._pinEcho)==0:
                    pulse_start_time = time()
                while GPIO.input(self._pinEcho)==1:
                    pulse_end_time = time()
                pulse_duration = pulse_end_time - pulse_start_time
                distance = round(pulse_duration * 17150, 2)
            except Exception as e:
                print(e)
                distance = None
            finally:
                GPIO.cleanup()
                return distance #Distance is in cm
        else:
            return None

    def __repr__(self):
        #Please check first one is connected to pin Trig and second to pin Echo
        return "\tUltrasonic range sensor #{}, on pins: {}".format(
            self.getNumber(),
            self.getPins(),
        )


class Motors(Component):
    def __init__(self, number, noMotors, offset, direction):
        Component.__init__(self, None, number)
        self._noMotors = noMotors
        self._offset = offset
        self._direction = direction
        self.config()

    def config(self):
        pass

    def drive(self, speed):
        #Drive motor at given speed
        if piOnlyLibraries:
            offsetSpeeds = (speed/self._offset)*self._direction
            if offsetSpeed < -1 or offsetSpeed > 1:
                raise Exception("Motor speed too high")
            TB.SetMotor1(offsetSpeed)

    def getNumberMotors(self):
        return self._noMotors

    def getOffest(self):
        return self._offset

    def getDirection(self):
        return self._direction

    def __repr__(self):
        return "\t{} motors #{}, on pins: {}, with speed offset {} and direction offset {}".format(
            self.getNumberMotors(),
            self.getNumber(),
            self.getPins(),
            self.getOffest(),
            self.getDirection()
        )




def main():
    if piOnlyLibraries:
        TB.Init()
        TB.SetBatteryMonitoringLevels(9,12)
        GPIO.setmode(GPIO.BOARD)

    LeftMotors = Motors(number=1,noMotors=2,offset=1,direction=1)
    RightMotors = Motors(number=1,noMotors=2,offset=1,direction=1)

    RangeSensor1 = RangeSensor(pins=[],number=1)
    RangeSensor2 = RangeSensor(pins=[],number=2)
    RangeSensor3 = RangeSensor(pins=[],number=3)
    RangeSensor4 = RangeSensor(pins=[],number=4)
    rangeSensors = [RangeSensor1,RangeSensor2,RangeSensor3,RangeSensor4]

    Webcam1 = Webcam(number=1, resolution=(32,32), framerate=10)
    Compass1 = Compass(pins=[],number=1)
    NerfGun1 = NerfGun(pins=[],number=1)

    Classifier1 = ColourClassifier(
        distanceThreshold=100,
        numberPixelThreshold=100,
        roundBase=20,
    )

    BobbyTables = Robot(
        name="Robert'); DROP TABLE Students; -- ",
        leftMotors=LeftMotors,
        rightMotors=RightMotors,
        rangeSensors=rangeSensors,
        webcam=Webcam1,
        compass=Compass1,
        nerfGun=NerfGun1,
        imgClassifier=Classifier1,
    )
    BobbyTables.diagnostics()

    BobbyTables.doCanyonsOfMars()

    cleanup()

if __name__ == "__main__":
    exit(main())
