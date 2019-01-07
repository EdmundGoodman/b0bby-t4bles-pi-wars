from picamera import PiCamera
from time import sleep, time
import io

import numpy as np
from PIL import Image
import cv2

from collections import Counter


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

    def classify(self, img):
        #Note if no colours are visible (very low light), it returns blue

        #Reduce colour depth
        img = img.point(lambda x: int(x/self.roundBase)*self.roundBase)
        pixels = img.getdata()
        #Count pixels & reject outliers
        pixelsCount = Counter(pixels)
        for k in list(pixelsCount):
            if pixelsCount[k] < self.numberPixelThreshold:
                del pixelsCount[k]
        #Classify colour based on getManhattanDistance distance from component colours
        colourValues = {"red": 0, "green": 0, "blue": 0, "yellow": 0, "black": 0}
        for pixels,number in pixelsCount.items():
            colour = self.getBaseColour(pixels)
            if colour in colourValues.keys():
                colourValues[colour] += number
        #Return the most prevalent colour
        colour = max(colourValues, key=colourValues.get)
        return colourValues

def loadImage(filePath):
    #Read the image
    img = Image.open(filePath)
    return img

DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE = 100,100,20
Classifier = ImageClassifier(DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE)

while True:
    startTime = time()
    with PiCamera() as camera:
        stream = io.BytesIO()
        camera.capture(stream, format="png", use_video_port=True, resize=(32,32))

    image = Image.open(stream)

    area = (400, 400, 800, 800)
    image = image.crop(area)

    colourValues = Classifier.classify(image)
    print(colourValues)
    #print("The object is {0} ({1}), and was classified in {2}s".format(colour, intensity, round(time()-startTime,2)))
exit()
