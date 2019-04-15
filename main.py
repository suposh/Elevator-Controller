import micropython
import machine
import time
import _thread

# exec(open('/main.py').read().globals())

MotionQueue    = []
InterruptFloorNew =  -1
InterruptFloorOld =  -1
ChangeDetected =  0
LOCKING=0

def callback(Object):
			pin = str(Object)
			pin = pin.split('(')
			pin = pin[1].split(')')
			pin = int(pin[0])
			# print('Scheduler Started ..From callback')
			global InterruptFloorNew
			global ChangeDetected
			global InterruptFloorOld
			#micropython.schedule(ISR, pin)
			InterruptFloorNew = pin

			if InterruptFloorNew == InterruptFloorOld :
				ChangeDetected = 0
			else:
				ChangeDetected = 1
				# InterruptFloorOld = InterruptFloorNew
def popMotionQueue():
	global MotionQueue
	global LOCK
	global InterruptFloorOld


	LOCK = 1
	MotionQueue.reverse()
	MotionQueue.pop()
	MotionQueue.reverse()

	LOCK = 0

def pinObjDecode(Object):
			pin = str(Object)
		  	pin = pin.split('(')
		  	pin = pin[1].split(')')
		  	pin = int(pin[0])
			return pin

def stat(a, b):
			print("Motion Queue {}".format(a))
			print("InterruptFloorNew {}".format(b))

class PINMap:
	floor = -2

	def __init__(self, Data, numberoffloor):

		self.Floornum = Data
		self.PinDescStr = []
		i = 0
		while i <= len(Data) - 1 :
			self.PinDescStr.append(str(Data[i]))
			i+=1

	def findFloorFromPin(self,pin):
		i = 0
		while i <= len(self.Floornum) - 1 :
			floor = self.PinDescStr[i].find(str(pin)+',')
			if floor > 0:
				print("Floor found for pin {} is {}".format(pin, i))
				return i
			i+=1
 # FLOOR(27, 12, 35, 14, 26), FLOOR(25, 33, 32, 13, 34), FLOOR(2, 4, 5, 18, 19)



class FLOOR:
	global MotionQueue
	global ChangeDetected
	global InterruptFloorNew
	global InterruptFloorOld

	def __init__(self, openR, closeR, cabinB, lift_FloorR):


			# self.levelNum     =     floorNum
			self.openReed     =     machine.Pin(openR,  machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.closeReed    =     machine.Pin(closeR, machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.cabinCall    =     machine.Pin(cabinB, machine.Pin.IN, machine.Pin.PULL_DOWN)
			# self.floorCall    =     machine.Pin(floorB, machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.liftLocation =     machine.Pin(lift_FloorR, machine.Pin.IN, machine.Pin.PULL_DOWN)
			# self.pinMap       =     [floorNum, openR, closeR, cabinB, floorB, lift_FloorR]
			# self.openReed.value()
			# self.closeReed.value()

			# self.liftLocation.value()
	def InitiateInterrupt(self):
			self.cabinCall.irq(trigger = machine.Pin.IRQ_RISING, handler=callback)
			# self.floorCall.irq(trigger = machine.Pin.IRQ_RISING, handler=callback)

class Motor:
  def __init__(self,dirOne,dirTwo,Enable):
	self.start = machine.Pin(Enable,machine.Pin.OUT)
	self.open  = machine.Pin(dirOne,machine.Pin.OUT)
	self.close = machine.Pin(dirTwo,machine.Pin.OUT)

  def Open(self):
	self.close.value(0)
	self.open.value(1)
	return 0

  def Close(self):
	self.open.value(0)
	self.close.value(1)
	return 1

  def liftPwm(self, motorTime, doorDuty, floo):
	global Level
	print("Lift Pwm Start")
	pwm2 = machine.PWM(self.start, freq=4000, duty=doorDuty)
	#
	t = time.ticks_ms()
	deltaT = time.ticks_diff(time.ticks_ms(), t)
	timeCond = floo.liftLocation.value() == 0
	while (timeCond):
		print("Lift Timer:{}".format(deltaT))
		time.sleep_ms(400)
		deltaT = time.ticks_diff(time.ticks_ms(), t)
		timeCond = deltaT <= motorTime or floo.liftLocation.value() == 0
		pass

	print("Lift Pwm End")

	return pwm2.deinit()
  def doorPwm(self, motorTime, doorDuty,floorNumb):
	global Level
	print("Door Pwm Start")
	self.Open()
	t = time.ticks_ms()
	pwm1 = machine.PWM(self.start, freq = 4000, duty=doorDuty)
	while Level[floorNumb].openReed.value() == 0 or time.ticks_diff(time.ticks_ms(), t) < motorTime:
		print("Door Open Timer:{}".format(t))
		# print("Oppen Read Value {}".format(Level[floorNumb].openReed.value()))
		time.sleep_ms(400)
		pass
	pwm1.deinit()
	self.start.value(0)

	time.sleep_ms(3000)

	self.Close()
	t = time.ticks_ms()
	pwm3 = machine.PWM(self.start, freq = 4000, duty=doorDuty)
	while Level[floorNumb].closeReed.value() == 0 or time.ticks_diff(time.ticks_ms(), t) < motorTime:
		# print("Close Read Value {}".format(Level[floorNumb].closeReed.value()))
		time.sleep_ms(400)
		print("Door Close Timer:{}".format(t))
		pass
	pwm3.deinit()
	print("Lift Pwm Start")

# def doorAction(motor,floor):
# 	motor.Open()
# 	#motor.Pwm(Pwn timer, Duty)
# 	motor.doorPwm(3000, 435, Level[floor].liftLocation)
# 	time.sleep(4000)
# 	motor.Close()
# 	motor.doorPwm(3000, 435 Level[floor].liftLocation)


def addToMotionQueue(floorToAdd):
	global MotionQueue
	global LOCKING

	if LOCKING == 0:
		LOCKING = 1
		MotionQueue.append(floorToAdd)
		LOCKING = 0

	elif LOCKING == 1:
		while LOCKING == 1:
			time.sleep_ms(4)
		LOCKING = 1
		MotionQueue.append(floorToAdd)
		LOCKING = 0




def updateMotionQueueViaInterrupt():
	global MotionQueue
	global ChangeDetected
	global InterruptFloorNew
	global InterruptFloorOld

	while True:

		if ChangeDetected == True :				#		<------
			# time.sleep_ms(400)
			state = machine.disable_irq()
			Floor = IOMap.findFloorFromPin(InterruptFloorNew)

			if len(MotionQueue) == 0:
				# print("len(MotionQueue) == 0")
				# MotionQueue.clear()
				addToMotionQueue(Floor)
				InterruptFloorOld = InterruptFloorNew
				ChangeDetected = 0
				machine.enable_irq(state)


			elif MotionQueue[len(MotionQueue)-1] != Floor :
				# print("MotionQueue[len(MotionQueue)-1] != Floor :")
				addToMotionQueue(Floor)
				InterruptFloorOld = InterruptFloorNew
				ChangeDetected = 0
				machine.enable_irq(state)

			else:
				# print("I dont know . Whats going on.")
				InterruptFloorOld = InterruptFloorNew
				ChangeDetected = 0
				machine.enable_irq(state)
				# just ignore the interrupt

			print(MotionQueue)

		else:
			pass
			# Goto Ground floor

#level[0] motor, level[1] motor,  level[2] motor,  #cabinmotion
MotorArray = [Motor(2,4,16),Motor(2,4,21),Motor(2,4,23),Motor(2,4,22)]

#(self, openR, closeR, cabinB, lift_FloorR)
Level = [ FLOOR(27, 12, 32, 26), FLOOR(25, 14, 33, 13), FLOOR(36, 39, 34, 35) ]

L= [[27, 12, 32, 26],[25, 14, 33, 13],[36, 39, 34, 35]]
IOMap=PINMap(L, 3)

cabinLoc = 0 										#cabin location

Level[0].InitiateInterrupt()
Level[1].InitiateInterrupt()
Level[2].InitiateInterrupt()

_thread.start_new_thread(updateMotionQueueViaInterrupt, ())
while True:
	if len(MotionQueue) > 0:
		print(MotionQueue)
		floorButton = MotionQueue[0]

		if floorButton > cabinLoc:
			# while(Level[floorButton].liftLocation.value() != 1):
			print('going up')
			MotorArray[3].Open() 				#Open = up
			MotorArray[3].liftPwm(4000, 500, Level[floorButton])
			MotorArray[floorButton].doorPwm(3000, 250, floorButton)
			cabinLoc = floorButton

		elif floorButton < cabinLoc:
			# while(Level[floorButton].liftLocation.value() != 1):
			MotorArray[3].Close() 				#Close = down
			MotorArray[3].liftPwm(5000, 500, Level[floorButton])
			MotorArray[floorButton].doorPwm(5000, 250, floorButton)
			cabinLoc = floorButton

		else:
			MotorArray[floorButton].doorPwm(5000, 250, floorButton)
			cabinLoc = floorButton

#CHECK LOCKING AND MODIFY MotionQueue

		if LOCKING == 0:
			popMotionQueue()
			print(MotionQueue)
		elif LOCKING == 1:
			while LOCKING == 1:
				time.sleep_ms(4)
			popMotionQueue()
			print(MotionQueue)
