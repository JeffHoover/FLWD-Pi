import os
import sys
import random
import time
import signal

import RPi.GPIO as GPIO
import picamera
from Adafruit_LED_Backpack import AlphaNum4
from twython import Twython

# My python files:
import words
import twitter_auth

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


def take_picture():
    camera.capture('image.jpg')
    photo = open('/home/pi/projects/FLWD-Pi/image.jpg', 'rb')
    return twitter.upload_media(media=photo)


def update_offense_level_from_switch(word, offense_level):
    if GPIO.input(SWITCH_GPIO_PIN) == GPIO.LOW:
        if offense_level <= 4:    
            offense_level += 1
        word = "   " + str(offense_level)
    return word


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


def display_word_no_tweet(word):
    display.print_str(word)
    display.write_display()
    print(word)
    time.sleep(1)


def display_word(word):
    display_word_no_tweet(word)
    response = take_picture()
    twitter.update_status(status = word, media_ids=[response['media_id']])


def display_startup_message():
    for start_word in words.startup_message:
        display_word_no_tweet(start_word)
        if GPIO.input(SWITCH_GPIO_PIN) == GPIO.LOW:
            return
        time.sleep(0.8)

# app starts here
#---------------------------


offense_level = 0
cleaner_button = 0
dirtier_button = 0 
word = "init"
SWITCH_GPIO_PIN = 12

#initialize the ctrl-c callback
signal.signal(signal.SIGINT, signal_handler)

camera = picamera.PiCamera()

twitter = Twython(twitter_auth.apiKey,twitter_auth.apiSecret,twitter_auth.accessToken,twitter_auth.accessTokenSecret)

# assign stderr to capture annoying (but ignorable) pull-up resistor errors:
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
    word = update_offense_level_from_switch(word, offense_level)
    if word.startswith(" "):
        new_offense_level = word[3:]
        offense_level = int(new_offense_level)
        if offense_level > 4:
            offense_level = 0
            word = "   0"

    display_word(word)


