from machine import Timer , Pin
z=Pin(4,Pin.OUT)
y=Pin(2,Pin.IN)
z.value(1)
while True:
  if y.value()==1:
    Timer(11)
    z.value(0)
  else:
    Timer(5)
    z.value(1)
  
