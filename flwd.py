from __future__ import print_function
import os
import sys
import random
import time
import signal

import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import AlphaNum4

import words

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SWITCH_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    os.system('echo gpio | sudo tee /sys/class/leds/led1/trigger')
    os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness')


# declare a callback to be called on ctrl-c to clean up hardware and leave display blank
def signal_handler(signal, frame):
        print('\nCleaning up GPIO and exiting.')
        display.clear()
        display.write_display()
        GPIO.cleanup();
        os.system('echo 1 | sudo tee /sys/class/leds/led1/brightness')
        sys.exit(0)

def get_clean_word():
    word = "*"
    while word.endswith("*"):
        word = random.choice(words.words)
    return word

def display_word(word):
    display.print_str(word)
    display.write_display()
    print(word)
    time.sleep(0.8 + random.random())

def display_startup_message():
    for start_word in words.startup_message:
        display_word(start_word)
        time.sleep(0.8)

word = "init"

#initialize the ctrl-c callback
signal.signal(signal.SIGINT, signal_handler)

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Init the display. Must be called once before using the display.
display.begin()
display.clear()

setup_GPIO()

random.seed()

# If any command-line argument, skip the startup message
if len(sys.argv) == 1:
    display_startup_message()

# Main Loop:
#------------
while True:
    display_word(get_clean_word())

