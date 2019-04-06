import micropython
import machine
import time

MotionQueue    = []
InterruptFloorNew =  -1
InterruptFloorOld =  -1
ChangeDetected =  0

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
L= [[27, 12, 35, 14, 26],[25, 33, 32, 13, 34],[2, 4, 5, 18, 19]]
IOMap=PINMap(L, 3)


class FLOOR:
	global MotionQueue
	global InterruptFloorNew
	global InterruptFloorOld
	global ChangeDetected

	def __init__(self, openR, closeR, cabinB, floorB, lift_FloorR):


			# self.levelNum     =     floorNum
			self.openReed     =     machine.Pin(openR,  machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.closeReed    =     machine.Pin(closeR, machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.cabinCall    =     machine.Pin(cabinB, machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.floorCall    =     machine.Pin(floorB, machine.Pin.IN, machine.Pin.PULL_DOWN)
			self.liftLocation =     machine.Pin(lift_FloorR, machine.Pin.IN, machine.Pin.PULL_DOWN)
			# self.pinMap       =     [floorNum, openR, closeR, cabinB, floorB, lift_FloorR]
			# self.openReed.value()
			# self.closeReed.value()

			# self.liftLocation.value()
	def InitiateInterrupt(self):
			self.cabinCall.irq(trigger = machine.Pin.IRQ_RISING, handler=callback)
			self.floorCall.irq(trigger = machine.Pin.IRQ_RISING, handler=callback)




class Motion:
	def VerticalMotionControl( ):
		pass

	def DoorControl():
		pass


#(self, floorNum, openR, closeR, cabinB, floorB, lift_FloorR)

Level = [ FLOOR(27, 12, 35, 14, 26), FLOOR(25, 33, 32, 13, 34), FLOOR(2, 4, 5, 18, 19) ]




Level[0].InitiateInterrupt()
Level[1].InitiateInterrupt()
Level[2].InitiateInterrupt()

while True:

	if ChangeDetected == True :				#		<------
		# time.sleep_ms(400)
		state = machine.disable_irq()
		Floor = IOMap.findFloorFromPin(InterruptFloorNew)

		if len(MotionQueue) == 0:
			# print("len(MotionQueue) == 0")
			# MotionQueue.clear()
			MotionQueue.append(Floor)
			InterruptFloorOld = InterruptFloorNew
			ChangeDetected = 0
			machine.enable_irq(state)


		elif MotionQueue[len(MotionQueue)-1] != Floor :
			# print("MotionQueue[len(MotionQueue)-1] != Floor :")
			MotionQueue.append(Floor)
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
		# Goto Ground floor
		pass
