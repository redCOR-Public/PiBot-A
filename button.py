#!/usr/bin/python
# ========================================================
# Python script for controlling a push button switch
# Version 1.2 for PiBot-A - Thomas Schoch - www.retas.de
# ========================================================

from time import sleep
from os import system
from sys import exit

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)  

# use button at GPIO 25 (P1 header pin 22)
gpio = 25

# main loop
while True:

    # setup GPIO "gpio" as input with pull-up
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

    # waiting for interrupt from button press
    GPIO.wait_for_edge(gpio, GPIO.FALLING)  

    # waiting for button release
    sec = 0
    while (GPIO.input(gpio) == GPIO.LOW):

        # delay for debouncing
        sleep(0.2)
        sec += 0.2

        # pressed longer than 2 seconds? Shutdown!
        if (sec > 2):
            GPIO.cleanup()
            system("/home/pi/robot/robot.sh shutdown")
            exit(0)

    # button released: toggle state of robot
    system("/home/pi/robot/robot.sh toggle")
    # reset interrupt

    GPIO.cleanup()
