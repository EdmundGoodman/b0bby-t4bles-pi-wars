import xbox
import ThunderBorg3

joy = xbox.Joystick()
ZB = ThunderBorg3.ThunderBorg()
ZB.Init()
#ZB.SetLedShowBattery(True)
#ZB.SetBatteryMonitoringLimits(9, 12)
print(ZB.GetBatteryReading())
ZB.SetLed1(0,0,0)
while True:
	if joy.connected():
		Turn = joy.leftX()
		Speed = joy.rightY()

		forwardPowerL = Speed
		forwardPowerR = Speed
		if Turn > 0.1:
			forwardPowerL -= forwardPowerL * 0.8 * Turn
		if Turn < -0.1:
			forwardPowerR += forwardPowerR * 0.8 * Turn
		if Speed > -0.1 and Speed < 0.1:
			if Turn > 0.2:
				forwardPowerL = -Turn * 0.7
				forwardPowerR = Turn * 0.7
			if Turn < 0.2:
				forwardPowerL = -Turn *  0.7
				forwardPowerR = Turn * 0.7
		ZB.SetMotor1(forwardPowerR)
		ZB.SetMotor2(-forwardPowerL)
	else:
		ZB.SetMotor1(0)
		ZB.SetMotor2(0)
	if joy.X():
		ZB.SetMotor1(0)
		ZB.SetMotor2(0)
		break
joy.close()

