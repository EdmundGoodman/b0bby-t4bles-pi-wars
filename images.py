import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def draw_histogram(clt):
    #Generate and show a histogram of the $NO_CLUSTERS most prevalent colours
    print("Generating histogram")
    hist = find_histogram(clt)
    print(hist, clt.cluster_centers_)
    bar = plot_colors2(hist, clt.cluster_centers_)
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

def find_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist

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

def load_image(IMAGE):
    #Read the image, and switch the colour channels to RGB
    print("Loading images")
    img = cv2.imread(IMAGE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.reshape((img.shape[0] * img.shape[1],3)) #represent as row*column,channel number
    return img

def cluster_colours(img, NO_CLUSTERS):
    #Cluster the image into the $NO_CLUSTERS most prevalent colours, using the KMeans class
    print("Clustering colours")
    clt = KMeans(n_clusters=NO_CLUSTERS)
    clt.fit(img)
    return clt

NO_CLUSTERS = 3
IMAGE = "redBlock.jpg"

img = load_image(IMAGE)
clt = cluster_colours(img, NO_CLUSTERS)
print(clt.labels_, clt.cluster_centers_)
draw_histogram(clt)
