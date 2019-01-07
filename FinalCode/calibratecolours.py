from robotFunctions import *
robot.camera.start()
input("Point at Blue")
BluePic = robot.camera.DanielPhoto2()
input("Point at Green")
GreenPic = robot.camera.DanielPhoto2()
input("Point at Red")
RedPic = robot.camera.DanielPhoto2()
input("Point at Yellow")
YellowPic = robot.camera.DanielPhoto2()

with open("ColourValues.txt", "r+") as f:
	f.truncate(0)
	f.write(str(RedPic[0]) + " " + str(RedPic[1]) + " " +  str(RedPic[2]) + "\n")
	f.write(str(GreenPic[0]) + " " + str(GreenPic[1]) + " " +  str(GreenPic[2]) + "\n")
	f.write(str(BluePic[0]) + " " + str(BluePic[1]) + " " +  str(BluePic[2]) + "\n")
	f.write(str(YellowPic[0]) + " " + str(YellowPic[1]) + " " + str(YellowPic[2]))
