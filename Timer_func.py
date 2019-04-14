import time

def Timer(Seconds):
    t=0
    while t<=Seconds:
        print(t)
        time.sleep(1)
        t+=1

Timer(10)