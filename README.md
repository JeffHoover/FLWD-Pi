# FLWD-Pi

My inspiration:

- http://pbxbook.com/clocks/B7971_flw.html (has video of startup message)
- http://www.oocities.org/tokyo/8908/fourletterword/index.html
- http://pbxbook.com/clocks/pdf/FLW-UM-2.5.pdf

Video showing original segment-based hangman mode:
-----------
https://www.youtube.com/watch?v=1UGYAl4RTpc


My Zetalink Four Letter Word has been running nearly 24/7/365 for more than 10 years.
-----------


Adafruit Quad Alphanumeric Display - Red 0.54" Digits w/ I2C Backpack 
- https://www.adafruit.com/products/1911  ($10)
- http://www.amazon.com/dp/B00L2X4JEW/ref=cm_sw_r_tw_dp_c4ZIwb0SV9F0G (Ah, Amazon Prime)

- https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/overview
- https://forums.adafruit.com/viewtopic.php?f=50&t=83885&p=423018&hilit=backpack+alphanumeric+54#p423018
- https://learn.adafruit.com/adafruit-led-backpack/0-54-alphanumeric
- https://learn.adafruit.com/led-backpack-displays-on-raspberry-pi-and-beaglebone-black/usage
- https://learn.adafruit.com/adafruit-led-backpack/changing-i2c-address
- https://www.adafruit.com/datasheets/CID2379.pdf

Trello board for backlog:
-----------
https://trello.com/b/GAjtxf5i/flwd-pi

Things I added from the original:
-----------
- hardware pushbutton to change mode on the fly (was dip switches)
- portability - original is fragile and high-voltage
- command-line flag to skip startup message

Pi-related things I've had to learn for this project:
-----------
- Driving an LED
- Reading hardware switches
- displaying words on the adafruit
- Trapping ctrl-c to shut down GPIO politely as program ends.
- Python
- Breaking python into multiple files (via import)
- Dictionary mapping for functions - use this strategy to replace multiple if()s and the absence of a switch command.
- Make a python program launch on Pi power-up (via crontab)
- Python program command-line args
- ssh'ing into the Pi via wifi
- Transferring files between Mac and Pi (via rsync)
- Shell out to turn off system LED(s) then shell out to turn back on just before exiting

Other skills needed for someone to reproduce what I did:
------------
- basic breadboarding
- unix commands
- git



 
