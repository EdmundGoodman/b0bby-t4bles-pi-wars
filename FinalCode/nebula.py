
#code for the nebula challenge
from robotFunctions import *
import numpy
def ManDis(x,y):
	return abs(x[0]-y[0]) + abs(x[1] - y[1]) + abs(x[2] - y[2])
robot.camera.start()
#robot.TurnDegrees(45)
input("done")
pic1 = robot.camera.DanielPhoto2()
r1,g1,b1 = pic1
input("done")
#robot.TurnDegrees(90)
pic2 = robot.camera.DanielPhoto2()
r2,g2,b2 = pic2
input("done")
#robot.TurnDegrees(90)
pic3 = robot.camera.DanielPhoto2()
r3,g3,b3 = pic3
input("done")
#robot.TurnDegrees(90)
pic4 = robot.camera.DanielPhoto2()
r4,g4,b4 = pic4
#RedNum = np.argmax(np.array([r1-b1-g1,r2-g2-b2,r3-b3-g3,r4-b4-g4]))
#BlueNum = np.argmax(np.array([b1-r1-g1,b2-r2-g2,b3-r3-g3,b4-g4-r4]))
#GreenNum = np.argmax(np.array([g1-b1-r1,g2-b2-r2,g3-b3-r3,g4-b4-r4]))
#YellowNum = np.argmax(np.array([r1+g1-b1,r2+g2-b2,r3+g3-b3,r4+g4-b4]))
f = open("ColourValues.txt", 'r')
calibratedColours = []
for line in f.read().splitlines():
	calibratedColours.append(tuple([float(i) for i in line.split()]))
options = [pic1,pic2,pic3,pic4]
f.close()
RedNum = np.argmin(np.array([ManDis(i,calibratedColours[0]) for i in options]))
GreenNum = np.argmin(np.array([ManDis(i,calibratedColours[1]) for i in options]))
BlueNum = np.argmin(np.array([ManDis(i,calibratedColours[2]) for i in options]))
YellowNum = np.argmin(np.array([ManDis(i,calibratedColours[3]) for i in options]))
print("Red pos is {} Blue pos is {} Green pos is {} Yellow pos is {}".format(RedNum,BlueNum,GreenNum,YellowNum))
