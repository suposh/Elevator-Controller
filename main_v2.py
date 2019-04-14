import machine
import time
class Motor:
  def __init__(self,dirOne,dirTwo,Enable):
    self.start=machine.Pin(Enable,machine.Pin.OUT)
    self.open=machine.Pin(dirOne,machine.Pin.OUT)
    self.close=machine.Pin(dirTwo,machine.Pin.OUT)
  def Open(self):
    self.close.value(0)
    self.open.value(1)
  def Close(self):
    self.open.value(0)
    self.close.value(1)
  def Pwm(self,motorTime):
    t=time.ticks_ms()
    while time.ticks_ms()-t=motorTime:
      pwm1= machine.PWM(self.start, freq=5000, duty=6500)
    pwm1.deinit()
def doorAction(motor):
    motor.Open()
    motor.Pwm(3000)
    time.sleep(4000)
    motor.Close()
    motor.Pwm(3000)
            #level[0] motor level[1] motor  level[2] motor  #cabinmotion
motorArray=[Motor(36,39,23),Motor(36,39,22),Motor(36,39,21),Motor(3,17,16)]

cabinLoc=0 #cabin location
# while Level[z].liftLocation.value()!=1:
# while MotionQueue=
floorButton=MotionQueue[0]
MotionQueue.reverse()
MotionQueue.pop()
MotionQueue.reverse()

# Level[floorButton].floorCall.value(1)
# Level[z].liftLocation.value()
if floorButton>cabinLoc:
    while(Level[floorButton].liftLocation.value()!=1):
        motorArray[3].Open() #Open = up
        motorArray[3].Pwm(5000)
    doorAction(motorArray[floorButton])
    cabinLoc=floorButton
elif floorButton<cabinLoc:
    while(Level[floorButton].liftLocation.value()!=1):
        motorArray[3].Close() #Close = down
        motorArray[3].Pwm(5000)
        doorAction(motorArray[floorButton])
    cabinLoc=floorButton
else:
    doorAction(motorArray[floorButton])
    cabinLoc=floorButton
