from time import sleep
import math

from tomotoio.navigator import Mat
from utils import createCubes, createNavigators, releaseCubes

cubes = createCubes()

(drawBot, moveBot, flipBot, dealBot) = (cubes[0], cubes[1], cubes[2], cubes[3])

#hard code robots start and task location

drawBotStart = [379, 328, 180]
drawBotMid = [308, 329, 180]
drawBotTask = [210, 328, 180]

drawForward = [drawBotMid, drawBotTask]
drawBackward = [drawBotMid, drawBotStart]

moveBotStart = [263, 420, 90]
moveBotTask = [263, 145, 90]

flipBotStart = [166, 203, 0]
flipBotTask = [210, 115, 270]

dealBotPlayer = [354, 133, 180]
dealBotDealer = [139, 140, 360]

# initail configuration for cubes
dealBot.configHorizontal(10)

# methods for moving each robot and handling errors

# motorType: 00 - constant, 01 - accelerate, 02 de accelerate, 03 accelerate then de accelerate
# movementType: 00 - move and rotate, 01 - not backwards, 02 - rotate after

def Move_DrawBot(locations, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		drawBot.moveToMulti(len(locations), locations, motorType, maxSpeed, movementType)

		while(len(drawBot.getMotorStatus()) != 3):
			pass

		exitCode = drawBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		# did not reach high enough on card
		elif exitCode == 1:
			drawBot.setMotor(-20, -20, .2)
			sleep(.2)
			drawBot.setMotor(150, 150, 1)
			sleep(1)
			break

		elif exitCode == 2:
			drawBot.setMotor(-20, -20, .5)
			sleep(.5)
			break
		else:
			print("Error: ", exitCode)
			break

def Move_MoveBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		moveBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(moveBot.getMotorStatus()) != 3):
			pass

		exitCode = moveBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			moveBot.setMotor(40, 40, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break

def Move_FlipBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		flipBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(flipBot.getMotorStatus()) != 3):
			pass

		exitCode = flipBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			flipBot.setMotor(20, 20, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break

def Move_DealBot(location, motorType: str = "03", maxSpeed: int = 80, movementType: str = "00"):
	finish = False
	while(finish == False):
		dealBot.moveTo(location, motorType, maxSpeed, movementType)

		while(len(dealBot.getMotorStatus()) != 3):
			pass

		exitCode = dealBot.getMotorStatus()[2]

		if exitCode == 0:
			finish = True

		elif exitCode == 2:
			dealBot.setMotor(20, 20, 1)
			sleep(1)
		else:
			print("Error: ", exitCode)
			break


# initialize all robots to starting posistions on board
drawBot.moveTo(drawBotStart)

Move_MoveBot(moveBotStart)

Move_FlipBot(flipBotStart)

Move_DealBot(dealBotDealer)

# movements for dealing card, initial deal of 3 cards, 2 to player one to dealer
for i in range(3):
	Move_DrawBot(drawForward, "01", 100, "00")
	Move_DrawBot(drawBackward, "00", 40, "00")

	#moveBot and flipBot Movement
	Move_MoveBot(moveBotTask, "03", 100)

	Move_FlipBot(flipBotTask)

	Move_FlipBot(flipBotStart)

	Move_MoveBot(moveBotStart)

	#dealCard every other
	Move_DealBot(dealBotPlayer if (i%2 == 0) else dealBotDealer, "03", 80, "02")

print("Hit or Stand? (double tap robot to hit) (tilt robot to stand)")
while True:

	# if cube is tilted(stand) break the loop
	# 1 is horezontal, 3 is double tap
	response = dealBot.getMotion()

	if response[3] == 1:
		dealBot.setSoundEffect(1)
		# dealBot to dealer side
		Move_DealBot(dealBotDealer)

		Move_DrawBot(drawForward, "01", 100, "00")

		Move_DrawBot(drawBackward, "00", 40, "00")


		#moveBot and flipBot Movement
		Move_MoveBot(moveBotTask, "03", 100)

		Move_FlipBot(flipBotTask)

		Move_FlipBot(flipBotStart)


		Move_MoveBot(moveBotStart)


		Move_DealBot(dealBotPlayer)

		print("Hit or Stand? (double tap robot to hit) (tilt robot to stand)")

	elif response[1] == 0:
		dealBot.setSoundEffect(2)
		sleep(.5)
		break

dealBot.motionReset()

dealerTotal = 0
while dealerTotal < 17:
	# dealBot to player side
	Move_DealBot(dealBotPlayer)

	Move_DrawBot(drawForward, "01", 100, "00")

	Move_DrawBot(drawBackward, "00", 40, "00")


	#moveBot and flipBot Movement
	Move_MoveBot(moveBotTask, "03", 100)


	Move_FlipBot(flipBotTask)

	Move_FlipBot(flipBotStart)

	Move_MoveBot(moveBotStart)


	Move_DealBot(dealBotDealer)
	dealerTotal += int(input("Dealers card: "))




releaseCubes(cubes)