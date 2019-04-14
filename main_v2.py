import machine
import time

LOCK = 0

def popMotionQueue():
    global MotionQueue
	global LOCK

    LOCK = 1
    MotionQueue.reverse()
    MotionQueue.pop()
    MotionQueue.reverse()
    LOCK = 0


class Motor:
  def __init__(self,dirOne,dirTwo,Enable):
    self.start = machine.Pin(Enable,machine.Pin.OUT)
    self.open  = machine.Pin(dirOne,machine.Pin.OUT)
    self.close = machine.Pin(dirTwo,machine.Pin.OUT)

  def Open(self):
    self.close.value(0)
    self.open.value(1)

  def Close(self):
    self.open.value(0)
    self.close.value(1)

  def Pwm(self,motorTime):
    t = time.ticks_ms()
    pwm1 = machine.PWM(self.start, freq=5000, duty=6500)
    while time.ticks_ms() - t < motorTime:
        pass
    pwm1.deinit()

def doorAction(motor):
    motor.Open()
    motor.Pwm(3000)
    time.sleep(4000)
    motor.Close()
    motor.Pwm(3000)

#level[0] motor, level[1] motor,  level[2] motor,  #cabinmotion
MotorArray = [Motor(36,39,23),Motor(36,39,22),Motor(36,39,21),Motor(3,17,16)]

while len(MotionQueue) > 0:

    cabinLoc = 0 #cabin location

    floorButton = MotionQueue[0]


    if floorButton > cabinLoc:
        while(Level[floorButton].liftLocation.value() != 1):
            MotorArray[3].Open() #Open = up
            MotorArray[3].Pwm(5000)
        doorAction(MotorArray[floorButton])
        cabinLoc = floorButton

    elif floorButton < cabinLoc:
        while(Level[floorButton].liftLocation.value() != 1):
            MotorArray[3].Close() #Close = down
            MotorArray[3].Pwm(5000)
            doorAction(MotorArray[floorButton])
        cabinLoc = floorButton

    else:
        doorAction(MotorArray[floorButton])
        cabinLoc = floorButton

#CHECK LOCK AND MODIFY MotionQueue

    if LOCK == 0:
        popMotionQueue()
    elif LOCK == 1:
        while LOCK == 1:
            pass
        popMotionQueue()
