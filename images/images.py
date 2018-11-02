from collections import Counter
from PIL import Image

class image_classifier:
    def __init__(self, DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE):
        self.roundBase = ROUNDBASE
        self.distanceThreshold = DISTANCE_THRESHOLD
        self.numberPixelThreshold = NUMBER_PIXEL_THRESHOLD

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
        return color #, distances[color]

    def classify(self, img):
        #Reduce colour depth
        img = img.point(lambda x: int(x/self.roundBase)*self.roundBase)
        pixels = img.getdata()
        #Count pixels & reject outliers
        pixelsCount = Counter(pixels)
        for k in list(pixelsCount):
            if pixelsCount[k] < self.numberPixelThreshold:
                del pixelsCount[k]
        #Classify colour based on manhattan distance from component colours
        colourValues = {"red": 0, "green": 0, "blue": 0, "yellow": 0}
        for pixels,number in pixelsCount.items():
            colour = self.get_base_colour(pixels)
            if colour in colourValues.keys():
                colourValues[colour] += number
        #Return the most prevalent colour
        colour = max(colourValues, key=colourValues.get)
        return colour

def load_image(filePath):
    #Read the image
    img = Image.open(filePath)
    return img

filePath = "redBlock.png"
img = load_image(filePath)
DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE = 100,100,20
classifier = image_classifier( DISTANCE_THRESHOLD, NUMBER_PIXEL_THRESHOLD, ROUNDBASE)
print(classifier.classify(img))
