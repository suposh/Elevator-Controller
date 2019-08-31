import micropython
import machine
import time
import _thread
import math

# exec(open('/main.py').read().globals())

MotionQueue    = []
InterruptFloorNew =  -1
InterruptFloorOld =  -1
ChangeDetected =  0
LOCK=0
LOCKTIME = 20 # in MILISECONDs

def callback(Object):
	"""
	Object argument is a string from whcih pin no. is extracted and converted to integer and this integer sets flag ChangeDetected and saves pin no. in variable InterruptFloorNew.
	"""
	pin = str(Object)
	pin = pin.split('(')
	pin = pin[1].split(')')
	pin = int(pin[0])
	# print('Scheduler Started ..From callback')
	global InterruptFloorNew
	global ChangeDetected
	global InterruptFloorOld
	global MotionQueue
	#micropython.schedule(ISR, pin)
	InterruptFloorNew = pin

	if len(MotionQueue) == 0:
		ChangeDetected = 1

	elif InterruptFloorNew == InterruptFloorOld :
		ChangeDetected = 0

	else:
		ChangeDetected = 1
		# InterruptFloorOld = InterruptFloorNew

def popMotionQueue():
	"""
	Once cabin reaches the floor which generated the call, that floor is poped out of list MotionQueue.
	"""
	global MotionQueue
	global LOCK
	global InterruptFloorOld

	if len(MotionQueue) > 0:
		LOCK = 1
		MotionQueue.reverse()
		MotionQueue.pop()
		MotionQueue.reverse()
		LOCK = 0

# def stat(a, b):
# 	"""
# 	This function is for debugging
# 	"""
# 	print("Motion Queue {}".format(a))
# 	print("InterruptFloorNew {}".format(b))

class PINMap:
	"""
	The callback function provides the pin number which generated the interrupt.
	This class stores relationship map between pin(s) belonging to respective floors.
	"""
	floor = -2

	def __init__(self, Data, numberoffloor):
		"""
		It creates the map from list of list of pins. All pins of a particular floor are contained in a list, and there are multiple such lists,which form a bigger list of all individual floors.
		pinmap = [[all pins of floor 0],[all pins of floor 1],[all pins of floor 2]]
		"""

		self.Floornum = Data
		self.PinDescStr = []
		i = 0
		while i <= len(Data) - 1 :
			self.PinDescStr.append(str(Data[i]))
			i+=1

	def findFloorFromPin(self,pin):
		"""
		This function finds the floor through the pin which is gien as an argument.
		This function iterates through a list of pins for every floor. When a match for a certain pin is found the floor no. is retuned.
		Magic in short.
		"""
		i = 0
		while i <= len(self.Floornum) - 1 :
			floor = self.PinDescStr[i].find(str(pin)+',')
			if floor > 0:
				print("Floor found for pin {} is {}".format(pin, i))
				return i
			elif i == len(self.Floornum) - 1:
				print("No match found for this pin.")
			i+=1
 # [ FLOOR(34, 12, 32, 26), FLOOR(25, 14, 33, 13), FLOOR(36, 39, 27, 35) ]



class FLOOR:
	"""

	"""
	global MotionQueue
	global ChangeDetected
	global InterruptFloorNew
	global InterruptFloorOld

	def __init__(self, openR, closeR, cabinB, lift_FloorR):
		"""
		
		"""


			#self.levelNum     =     floorNum
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
		global speedTable
		print("Heap Size {}".format(gc.mem_free()))
		print("Lift Pwm Start")


		dutyPump = 0
		UnitTimeDiv = int(motorTime/10)
		t = time.ticks_ms()
		deltaT = time.ticks_diff(time.ticks_ms(), t)

		pwm1 = machine.PWM(self.start, freq=4000, duty=0)
		while not(deltaT >= motorTime or floo.liftLocation.value() == 1):
			if deltaT > dutyPump*UnitTimeDiv:
				doorDuty = int(speedTable[dutyPump])
				pwm1 = machine.PWM(self.start, freq=4000, duty=doorDuty)
				dutyPump += 1
				# print("Duty Pump: {}".format(dutyPump))
			# print("Lift Timer:{}".format(deltaT))
			# time.sleep_ms(100)
			deltaT = time.ticks_diff(time.ticks_ms(), t)
			# if deltaT <= motorTime or floo.liftLocation.value() == 1:
			# 	break
		print("Lift Timer:{}".format(deltaT))
		duty = 0
		print("Lift Pwm End")

		return pwm1.deinit()

	def doorPwm(self, motorTime, doorDuty,floorNumb):
		global Level
		print("Door Pwm Start")
		self.Open()
		# print("Heap Size 1 {}".format(gc.mem_free()))
		t = time.ticks_ms()
		deltaT = time.ticks_diff(time.ticks_ms(), t)
		pwm2 = machine.PWM(self.start, freq = 4000, duty=doorDuty)
		while not(deltaT >= motorTime or Level[floorNumb].openReed.value() == 1):
			# print("Oppen Read Value {}".format(Level[floorNumb].openReed.value()))
			time.sleep_ms(400)
			deltaT = time.ticks_diff(time.ticks_ms(), t)
			# print("Door Open Timer:{}".format(deltaT))
		# print("Heap Size 2 {}".format(gc.mem_free()))
		print("Door Open Time:{}".format(deltaT))
		pwm2.deinit()



		time.sleep(3)

		self.Close()
		# print("Heap Size 3 {}".format(gc.mem_free()))
		t = time.ticks_ms()
		deltaT = time.ticks_diff(time.ticks_ms(), t)
		pwm3 = machine.PWM(self.start, freq = 4000, duty=doorDuty)
		while not(deltaT >= motorTime or Level[floorNumb].closeReed.value() == 1):
			# print("Close Read Value {}".format(Level[floorNumb].closeReed.value()))
			time.sleep_ms(400)
			deltaT = time.ticks_diff(time.ticks_ms(), t)
			# print("Door Close Timer:{}".format(deltaT))

		# print("Heap Size 4 {}".format(gc.mem_free()))
		print("Door Close Time:{}".format(deltaT))
		pwm3.deinit()

def addToMotionQueue(floorToAdd):
	global MotionQueue
	global LOCK
	global LOCKTIME

	if LOCK == 0:
		LOCK = 1
		TempMotionQueue = MotionQueue.copy()
		TempMotionQueue.append(floorToAdd)
		MotionQueue = TempMotionQueue.copy()
		LOCK = 0

	elif LOCK == 1:
		while LOCK == 1:
			time.sleep_ms(LOCKTIME)
		LOCK = 1
		TempMotionQueue = MotionQueue.copy()
		TempMotionQueue.append(floorToAdd)
		MotionQueue = TempMotionQueue.copy()
		LOCK = 0




def updateMotionQueueViaInterrupt():
	global MotionQueue
	global ChangeDetected
	global InterruptFloorNew
	global InterruptFloorOld
	global IOMap

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
Level = [ FLOOR(34, 12, 32, 26), FLOOR(25, 14, 33, 13), FLOOR(36, 39, 27, 35) ]

L= [[34, 12, 32, 26],[25, 14, 33, 13],[36, 39, 27, 35]]
IOMap=PINMap(L, 3)

cabinLoc = 0 										#cabin location

Level[0].InitiateInterrupt()
Level[1].InitiateInterrupt()
Level[2].InitiateInterrupt()
TimeTable = [3000, 5000 ,7000]
speedTable = [20,150,180,350,450,449,349,179,149 ,20 ]
dutyForDoor = 800
_thread.start_new_thread(updateMotionQueueViaInterrupt, ())
while True:
	if len(MotionQueue) > 0:
		print(MotionQueue)
		floorButton = MotionQueue[0]
		travelTime = TimeTable[int(math.fabs(floorButton-cabinLoc))]
		if floorButton > cabinLoc:
			# while(Level[floorButton].liftLocation.value() != 1):
			print('going up')
			MotorArray[3].Open() 				#Open = up
			MotorArray[3].liftPwm(travelTime, 500, Level[floorButton])
			MotorArray[floorButton].doorPwm(3000, dutyForDoor, floorButton)
			cabinLoc = floorButton

		elif floorButton < cabinLoc:
			# while(Level[floorButton].liftLocation.value() != 1):
			MotorArray[3].Close() 				#Close = down
			MotorArray[3].liftPwm(travelTime, 500, Level[floorButton])
			MotorArray[floorButton].doorPwm(5000, dutyForDoor, floorButton)
			cabinLoc = floorButton

		else:
			MotorArray[floorButton].doorPwm(5000, dutyForDoor, floorButton)
			cabinLoc = floorButton

#CHECK LOCK AND MODIFY MotionQueue

		if LOCK == 0:
			popMotionQueue()
			print(MotionQueue)
		elif LOCK == 1:
			while LOCK == 1:
				time.sleep_ms(LOCKTIME)
			popMotionQueue()
			print(MotionQueue)
	gc.collect()
	time.sleep(1)
