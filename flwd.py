from __future__ import print_function
import os
import sys
import random
import time
import signal

import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import AlphaNum4

# My python files:
import words


def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    os.system('echo gpio | sudo tee /sys/class/leds/led1/trigger')
    os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness')

f = open('output.log', 'w')


# declare a callback to be called on ctrl-c to clean up hardware and leave display blank
def signal_handler(signal, frame):
        print('\nCleaning up GPIO and exiting.')
        f.close()
        display.clear()
        display.write_display()
        GPIO.cleanup();
        os.system('echo 1 | sudo tee /sys/class/leds/led1/brightness')
        sys.exit(0)


def get_offensive_word():
    word = "okok"
    while not word.endswith("*"):
        word = random.choice(words.words)
    return word


def get_clean_word():
    word = "*"
    while word.endswith("*"):
        word = random.choice(words.words)
    return word


def get_random_word():
    word = random.choice(words.words)
    return word


def get_word_based_on_offense_level(offense_level):
    function_chooser = {
        0: get_clean_word(),    # totally clean
        1: get_clean_word(),    # TODO - biased toward clean
        2: get_random_word(),   # equally random
        3: get_random_word(),   # TODO - biased toward dirty
        4: get_offensive_word() # only dirty
    }
    get_word = function_chooser.get(offense_level, lambda:get_clean_word())
    return get_word


def display_word(word):
    display.print_str(word)
    display.write_display()
    print(word)
    f.write(word+'\n')
    time.sleep(0.8)


def display_startup_message():
    for start_word in words.startup_message:
        display_word(start_word)
        time.sleep(0.7)


# app starts here
#---------------------------


offense_level = 2
word = "init"

#initialize the ctrl-c callback
signal.signal(signal.SIGINT, signal_handler)

# assign stderr to capture any errors
sys.stderr = open('stderr.txt', 'w')

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Init the display. Must be called once before using the display.
display.begin()
display.clear()

setup_GPIO()

random.seed()

if len(sys.argv) == 1:
    display_startup_message()

# Main Loop:
#------------
while True:
    word = get_word_based_on_offense_level(offense_level)
    display_word(word)


