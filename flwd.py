import random
import time
import RPi.GPIO
import words
import signal

def signal_handler(signal, frame):
        print('\nCleaning up GPIO and exiting.')
        RPi.GPIO.cleanup();
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#from Adafruit_LED_Backpack import AlphaNum4
import sys

sys.stderr = open('stderr.txt', 'w')
# assigning stderr above captures these annoying (but ignorable) errors:
#flwd.py:43: RuntimeWarning: A physical pull up resistor is fitted on this channel!
#  RPi.GPIO.setup(12 RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)

## Create display instance on default I2C address (0x70) and bus number.
#display = AlphaNum4.AlphaNum4()

## Alternatively, create a display with a specific I2C address and/or bus.
## display = AlphaNum4.AlphaNum4(address=0x74, busnum=1)

## Init the display. Must be called once before using the display.
#display.begin()

offense_level = 0
cleaner_button = 0
dirtier_button = 0 
word = "init"

def update_offense_level_from_switch(word, offense_level):

    if RPi.GPIO.input(12) == RPi.GPIO.LOW:
        if offense_level <= 4:    
            offense_level += 1
        word = "   " + str(offense_level)
    return word

def setup_GPIO():
    RPi.GPIO.setmode(RPi.GPIO.BCM)
    RPi.GPIO.setup(12, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)
    RPi.GPIO.setup(4, RPi.GPIO.OUT)

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
#    display.clear()
#    display.print_str(word)
#    display.write_display()
    print(word)

def display_startup_message():
    for start_word in words.startup_message:
        RPi.GPIO.output(4, RPi.GPIO.HIGH)
        display_word(start_word)
        time.sleep(0.4)
        RPi.GPIO.output(4, RPi.GPIO.LOW)
        time.sleep(0.4)

setup_GPIO()

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

    RPi.GPIO.output(4, RPi.GPIO.HIGH)
    time.sleep(0.5)
    RPi.GPIO.output(4, RPi.GPIO.LOW)
    time.sleep(0.5)


