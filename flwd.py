import picamera
import random
import time
import RPi.GPIO
import words
import signal
import os
from twython import Twython
import twitter_auth
import sys
from Adafruit_LED_Backpack import AlphaNum4

def signal_handler(signal, frame):
        print('\nCleaning up GPIO and exiting.')
        display.clear()
        display.write_display()
        RPi.GPIO.cleanup();
        os.system('echo 1 | sudo tee /sys/class/leds/led1/brightness')
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

camera = picamera.PiCamera()

api = Twython(twitter_auth.apiKey,twitter_auth.apiSecret,twitter_auth.accessToken,twitter_auth.accessTokenSecret)

sys.stderr = open('stderr.txt', 'w')
# assigning stderr above captures these annoying (but ignorable) errors:
#flwd.py:43: RuntimeWarning: A physical pull up resistor is fitted on this channel!
#  RPi.GPIO.setup(12 RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

## Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

## Init the display. Must be called once before using the display.
display.begin()
display.clear()

offense_level = 0
cleaner_button = 0
dirtier_button = 0 
word = "init"
SWITCH_GPIO_PIN = 12

def update_offense_level_from_switch(word, offense_level):

    if RPi.GPIO.input(SWITCH_GPIO_PIN) == RPi.GPIO.LOW:
        if offense_level <= 4:    
            offense_level += 1
        word = "   " + str(offense_level)
    return word

def setup_GPIO():
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setup(SWITCH_GPIO_PIN, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    os.system('echo gpio | sudo tee /sys/class/leds/led1/trigger')
    os.system('echo 0 | sudo tee /sys/class/leds/led1/brightness')

def print_throwing_away (word):
    print ("Throwing away: " + word)

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

    camera.capture('image.jpg')
    photo = open('/home/pi/projects/FLWD-Pi/image.jpg', 'rb')
    response = api.upload_media(media=photo)
    api.update_status(status = word, media_ids=[response['media_id']])

    time.sleep(1)

def display_startup_message():
    for start_word in words.startup_message:
        display_word(start_word)
        if RPi.GPIO.input(SWITCH_GPIO_PIN) == RPi.GPIO.LOW:
            return
        time.sleep(0.9)

setup_GPIO()

random.seed()

if len(sys.argv) == 1:
    display_startup_message()


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

