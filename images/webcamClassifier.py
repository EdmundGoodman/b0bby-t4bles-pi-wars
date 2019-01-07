from collections import Counter
import io
import time
import picamera
from PIL import Image


class ImageClassifier:
    def __init__(self, DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE):
        self.roundBase = ROUNDBASE
        self.distanceThreshold = DISTANCE_THRESHOLD
        self.numberPixelThreshold = NUMBER_PIXEL_THRESHOLD

        self.colours = {
            "red": (255, 0, 0),
            "green" : (0,255,0),
            "blue" : (0,0,255),
            "yellow": (255,255,0),
            "white" : (255,255,255),
            "black" : (0,0,0),
        }

    def setColourValue(self, colour, value):
        self.colours[colour] = value

    def getColours(self):
        return self.colours

    def getBaseColour(self, rgb_tuple):
        def getManhattanDistance(x,y):
            return abs(x[0] - y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
        
        distances = {k: getManhattanDistance(v, rgb_tuple) for k, v in self.colours.items()}
        colour = min(distances, key=distances.get)
        return colour #, distances[color]

    def formatImage(self, img):
        #Reduce colour depth
        img = img.point(lambda x: int(x/self.roundBase)*self.roundBase)
        pixels = img.getdata()
        #Count pixels & reject outliers
        pixelsCount = Counter(pixels)
        for k in list(pixelsCount):
            if pixelsCount[k] < self.numberPixelThreshold:
                del pixelsCount[k]
        return pixelsCount
        
    def classify(self, img):
        pixelsCount = self.formatImage(img)
        #Classify colour based on getManhattanDistance distance from component colours
        colourValues = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "white": 0, "black": 0}
        for pixels,number in pixelsCount.items():
            colour = self.getBaseColour(pixels)
            if colour in colourValues.keys():
                colourValues[colour] += number
        #Return the most prevalent colour
        colour = max(colourValues, key=colourValues.get)
        if (colour == "white" or colour == "black") and False:
            del colourValues["white"]
            del colourValues["black"]
            colour += " " + max(colourValues, key=colourValues.get)
        return colour, colourValues[colour]

    def getMeanRGB(self, img):
        pixelsCount = self.formatImage(img)
        colour = [0,0,0]
        for pixels in pixelsCount:
            for i in range(3):
                colour[i] += pixels[i]
        for i in range(3):
            colour[i] /= len(pixelsCount)
        return colour

def outputs():
    stream = io.BytesIO()
    while True:
        yield stream
        stream.seek(0)
        img = Image.open(stream)
        print(Classifier.classify(img))
        stream.seek(0)
        stream.truncate()

def calibrate():
    for colour in "red green blue yellow".split(" "):
        input("Show the camera {}: ".format(colour))
        stream = io.BytesIO()
        camera.capture(stream, "jpeg")
        stream.seek(0)
        img = Image.open(stream)
        colourValues = Classifier.getMeanRGB(img)        
        Classifier.setColourValue(colour, colourValues)

with picamera.PiCamera() as camera:
    DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE = 100,100,20
    Classifier = ImageClassifier(DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE)

    camera.resolution = (640, 480)
    camera.resolution = (80,60)
    camera.framerate = 80


    calibrate()

    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
print('Captured 40 images at %.2ffps' % (40 / (finish - start)))
