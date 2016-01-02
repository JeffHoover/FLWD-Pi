import RPi.GPIO
import time
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(2, RPi.GPIO.OUT)

while True:
    RPi.GPIO.output(2, RPi.GPIO.HIGH)
    time.sleep(1)
    RPi.GPIO.output(2, RPi.GPIO.LOW)
    time.sleep(1)
