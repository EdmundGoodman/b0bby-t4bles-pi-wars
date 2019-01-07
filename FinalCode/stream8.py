import io
import time
import picamera
from PIL import Image
import numpy as np

def softEval(val1,val2):
    return val1/val2<1.4 and val1/val2>0.7

def classify(r,g,b):
    m=r
    r,g,b=r/m,g/m,b/m
    if g>r and not softEval(g,r):
        return "green"

    elif r>g and not softEval(r,g) and r>b and not softEval(r,b):
        return "red"
    elif b>r and not softEval(b,r) and b>g and not softEval(b,g):
        return "blue"
    elif r>b and not softEval(r,b) and g>b and not softEval(g,b):
        return "yellow"
    else:
        return "black"


def outputs():
    stream = io.BytesIO()
    for i in range(8000000):
        time.sleep(0.05)
        rTotal=0
        bTotal=0
        gTotal=0
        # This returns the stream for the camera to capture to
        yield stream
        # Once the capture is complete, the loop continues here
        # (read up on generator functions in Python to understand
        # the yield statement). Here you could do some processing
        # on the image...
        stream.seek(0)
        img = Image.open(stream)
        for pixle in list(img.getdata()):
            rTotal+=pixle[0]
            gTotal+=pixle[1]
            bTotal+=pixle[2]
        # Finally, reset the stream for the next capture
        """time.sleep(0.5)"""
        stream.seek(0)
        stream.truncate()
        print(rTotal,gTotal,bTotal)
        print(classify(rTotal,gTotal,bTotal))

with picamera.PiCamera() as camera:
    camera.resolution = (32, 32)
    camera.framerate = 80
    time.sleep(2)
    print("go")
    start = time.time()
    camera.capture_sequence(outputs(), 'jpeg', use_video_port=True)
    finish = time.time()
    print('Captured 80 images at %.2ffps' % (80 / (finish - start)))
