import machine
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
  def Pwm(self):
    t=time.ticks_ms()
    while time.ticks_ms()-t=3000:
      pwm1= machine.PWM(self.start, freq=5000, duty=6500)
  def doorAction(self):
    motorArray[floorButton].Open()
    motorArray[floorButton].Pwm()
    time.sleep(10000)
    motorArray[floorButton].Close()

motorArray=[Motor(36,39,23),Motor(36,39,22),Motor(36,39,21),Motor(3,17,16)]

z=0
# while Level[z].liftLocation.value()!=1:

floorButton=MotionQueue[0]
MotionQueue.reverse()
MotionQueue.pop()
MotionQueue.reverse()

# Level[floorButton].floorCall.value(1)
# Level[z].liftLocation.value()
if floorButton>z:
    while(Level[floorButton].liftLocation.value()!=1):
        motorArray[3].Open() #open = up
        motorArray[3].Pwm()
    motorArray[floorButton].doorAction()
    z=floorButton
elif floorButton<z:
    while(Level[floorButton].liftLocation.value()!=1):
        motorArray[3].Close() #close = down
        motorArray[3].Pwm()
    motorArray[floorButton].doorAction()
    z=floorButton
else:
    motorArray[floorButton].doorAction()
    z=floorButton
