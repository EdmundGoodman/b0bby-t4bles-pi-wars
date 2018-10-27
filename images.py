import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


class image_classifier:
    def __init__(self, NO_CLUSTERS, DISTANCE_THRESHOLD):
        self.no_clusters = NO_CLUSTERS
        self.distance_threshold = DISTANCE_THRESHOLD


    def draw_histogram(self, hist, clt):
        #Draw the histogram
        bar = self.plot_colors2(hist, clt.cluster_centers_)
        plt.axis("off")
        plt.imshow(bar)
        plt.show()


    def find_histogram(self, clt):
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)
        hist = hist.astype("float")
        hist /= hist.sum()
        return hist


    def plot_colors2(self, hist, centroids):
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX
        return bar


    def cluster_colours(self, img):
        #Cluster the image into the $NO_CLUSTERS most prevalent colours, using the KMeans class
        print("Clustering colours")
        clt = KMeans(n_clusters=self.no_clusters)
        clt.fit(img)
        return clt


    def generate_histogram(self, clt):
        #Generate and show a histogram of the $NO_CLUSTERS most prevalent colours
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


    def classify(self, img):
        clt = self.cluster_colours(img)
        hist = self.generate_histogram(clt)
        self.draw_histogram(hist, clt)

        predominantColour, maxIntensity = None, 0
        for i in range(len(hist)):
            cluster, intensity = clt.cluster_centers_[i], hist[i]
            colour, distance = self.get_base_colour(cluster)
            #print(cluster, colour, distance, intensity)
            if colour != "white" and colour != "black" and distance < DISTANCE_THRESHOLD:
                if intensity > maxIntensity:
                    predominantColour, maxIntensity = colour, intensity
        return predominantColour


def load_image(IMAGE):
    #Read the image, and switch the colour channels to RGB
    print("Loading images")
    img = cv2.imread(IMAGE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    return img

NO_CLUSTERS = 2
DISTANCE_THRESHOLD = 255*2

IMAGE = "redBlock.jpg"
img = load_image(IMAGE)
classifier = image_classifier(NO_CLUSTERS, DISTANCE_THRESHOLD)
colour = classifier.classify(img)
print(colour)
