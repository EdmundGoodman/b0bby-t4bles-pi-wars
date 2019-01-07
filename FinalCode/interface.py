from robotFunctions import *
import time
import xbox
try:
    controller=xbox.Joystick()
except:
    print("controller not found, exiting...")
    robot.shutdown()
while True:
    time.sleep(0.05)
    print("attempting initiation")
    if robot.controller.A():
        from speedTest import *
    elif robot.controller.B():
        from nebula import *
    elif robot.controller.C():
        from maze import *
    elif robot.controller.D():
        from manual import *
    exit()
