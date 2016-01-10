import RPi.GPIO
import signal
import os
import time
import sys

#import from RPi GPIO

def signal_handler(signal, frame):
        RPi.GPIO.output(RED, False)   # Turns off the Red LED
        RPi.GPIO.output(YELLOW, False)  # Turns off the Yellow LED
        RPi.GPIO.output(GREEN, False)  # Turns off the Green LED
        print('\nCleaning up GPIO and exiting.')
        RPi.GPIO.cleanup();
        os.system('echo 1 | sudo tee /sys/class/leds/led1/brightness')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

sys.stderr = open('stderr_traffic.txt', 'w')
# assigning stderr above captures annoying (but ignorable) errors

os.system('echo gpio | sudo tee /sys/class/leds/led1/trigger')
os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness')

RPi.GPIO.setmode(RPi.GPIO.BCM)

RED = 9
YELLOW = 10
GREEN = 11

RPi.GPIO.setup(RED, RPi.GPIO.OUT)  # Red LED pin set as output
RPi.GPIO.setup(YELLOW, RPi.GPIO.OUT) # Yellow LED pin set as output
RPi.GPIO.setup(GREEN, RPi.GPIO.OUT) # Green LED pin set as output
#RPi.GPIO.setup(12, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP) # Switch as input

while True:

    RPi.GPIO.output(GREEN, True)  # Turns on the Green LED
    RPi.GPIO.output(YELLOW, False) 
    RPi.GPIO.output(RED, False) # Turns off the Red LED
    time.sleep(2)


    RPi.GPIO.output(YELLOW, True) # Turns on the Yellow LED
    RPi.GPIO.output(GREEN, False)
    time.sleep(1)



    RPi.GPIO.output(YELLOW, False) 
    RPi.GPIO.output(RED, True)
    time.sleep(2)


    RPi.GPIO.output(RED, False)
