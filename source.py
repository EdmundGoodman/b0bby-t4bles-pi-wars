#https://piwars.org/2019-competition/challenges/
from sklearn.cluster import KMeans
from time import sleep
import numpy as np
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

    def diagnostics(self):
        print("Diagnostics: ")
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

    def doCanyonsOfMars(self, step=5, threshold=100):
        #Use the left hand follow to solve the maze
        while True:
            #Check for alien sign, then do output
            img = self._webcam.read()
            if self._classifier.classify(img) == "green":
                print("Alien!") # Do an output


            sensorValues = [self._rangeSensors[i].read() for i in range(4)]
            #Check for exit condition: open on all four sides?
            if min(sensorValues) > threshold:
                break

            #Try to turn left
            if sensorValues[0] > threshold:
                self.left(90)
                self.forward(step)
            #Try to go forward
            elif sensorValues[1] > threshold:
                self.forward(step)
            #Try to turn right
            elif sensorValues[2] > threshold:
                self.right(90)
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
            colours.append(self._classifier.classify(img))
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

    def doBlastOff(self, length=7500):
        #Drive in a straight line, at full speed
        #Stateful control with compass, and stop at end
        self.forward(length)

    def RCControl(self):
        #RC control
        pass

    def __repr__(self):
        return "{}".format(self._name)


class ColourClassifier():
    def __init__(self, _no_clusters, _distance_threshold):
        self._no_clusters = _no_clusters
        self._distance_threshold = _distance_threshold

    def draw_histogram(self, hist, clt):
        #Draw the histogram#
        import matplotlib.pyplot as plt

        def plot_colors2(hist, centroids):
            bar = np.zeros((50, 300, 3), dtype="uint8")
            startX = 0
            for (percent, color) in zip(hist, centroids):
                # plot the relative percentage of each cluster
                endX = startX + (percent * 300)
                cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                              color.astype("uint8").tolist(), -1)
                startX = endX
            return bar

        bar = plot_colors2(hist, clt.cluster_centers_)
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    def find_histogram(self, clt):
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()
        return hist

    def cluster_colours(self, img):
        #Cluster the image into the $_no_clusters most prevalent colours, using the KMeans class
        print("Clustering colours")
        clt = KMeans(n_clusters=self._no_clusters)
        clt.fit(img)
        return clt

    def generate_histogram(self, clt):
        #Generate and show a histogram of the $_no_clusters most prevalent colours
        print("Generating histogram")
        hist =self.find_histogram(clt)
        return hist

    def get_base_colour(self, rgb_tuple):
        def manhattan(x,y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])

        colours = {
            "red": (255, 0, 0),
            "green" : (0,255,0),
            "blue" : (0,0,255),
            "yellow": (255,255,0),
            "white" : (255,255,255),
            "black" : (0,0,0),
        }
        distances = {k: manhattan(v, rgb_tuple) for k, v in colours.items()}
        color = min(distances, key=distances.get)
        return color, distances[color]

    def classify(self, img, draw_histogram=False):
        clt = self.cluster_colours(img)
        hist = self.generate_histogram(clt)
        if draw_histogram:
            self.draw_histogram(hist, clt)

        predominantColour, maxIntensity = None, 0
        for i in range(len(hist)):
            cluster, intensity = clt.cluster_centers_[i], hist[i]
            colour, distance = self.get_base_colour(cluster)
            #print(cluster, colour, distance, intensity)
            if colour != "white" and colour != "black" and distance < self._distance_threshold:
                if intensity > maxIntensity:
                    predominantColour, maxIntensity = colour, intensity
        return predominantColour

    def getNoClusters(self):
        return self._no_clusters

    def setNoClusters(self, no_clusters):
        self._no_clusters = no_clusters

    def getDistanceThreshold(self):
        return self._distance_threshold

    def setDistanceThreshold(self, distance_threshold):
        self._distance_threshold = distance_threshold


class NerfGun:
    def __init__(self, pins):
        self._pins = pins
        self.config()

    def config(self):
        #Do any necessary setup to allow the sensor to be read from
        for pin in self._pins:
            pass

    def getPins(self):
        return self._pins

    def revMotors(self):
        pass

    def fireDart(self):
        pass

    def __repr__(self):
        return "Nerf gun on pins {}".format(self._pins)


class Compass:
    def __init__(self, pins):
        self._pins = pins
        self.config()

    def config(self):
        #Do any necessary setup to allow the sensor to be read from
        for pin in self._pins:
            pass

    def getPins(self):
        return self._pins

    def read(self):
        return None

    def __repr__(self):
        return "Compass on pins {}".format(self._pins)


class Webcam:
    def __init__(self):
        self._cap = cv2.VideoCapture(0)

    def read(self):
        return self.loadImage("alien.png")

        _, frame =self._cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = frame.reshape((frame.shape[0] * frame.shape[1],3))
        return frame

    def loadImage(self, imageName):
        img = cv2.imread(imageName)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
        return img


    def getCap(self):
        return self._cap

    def __repr__(self):
        return "Webcam"


class RangeSensor:
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


class Motor:
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
    Motor1 = Motor(number=1,pins=[],offset=1)
    Motor2 = Motor(number=2,pins=[],offset=1)
    motors = [Motor1, Motor2]

    RangeSensor1 = RangeSensor(number=1, pins=[])
    rangeSensors = [RangeSensor1]

    Webcam1 = Webcam()
    Compass1 = Compass([])
    NerfGun1 = NerfGun([])

    Classifier1 = ColourClassifier(2, 255*2)

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


    #Testing classifying an image
    print("\nTesting image recognition:")
    imageName = "blueBlock.jpg"
    img = Webcam1.loadImage(imageName)
    colour = Classifier1.classify(img, draw_histogram=True)
    print(colour)

if __name__ == "__main__":
    exit(main())
