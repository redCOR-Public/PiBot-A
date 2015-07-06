#!/usr/bin/python
# ========================================================
# Python script for PiBot-A: obstacle avoidance
# Version 1.0 - by Thomas Schoch - www.retas.de
# ========================================================

from __future__ import print_function #+# NUR WENN PRINT!
from pololu_drv8835_rpi import motors, MAX_SPEED
from time import sleep
import RPi.GPIO as GPIO

# Signal handler for SIGTERM
import signal, sys
def sigterm_handler(signal, frame):
    motors.setSpeeds(0, 0)
    sys.exit(0) 
signal.signal(signal.SIGTERM, sigterm_handler)

# GPIO pins of sensors
GPIO.setmode(GPIO.BCM)
GPIO_right  = 21
GPIO_middle = 26
GPIO_left   = 20

# Configure sensors as input
GPIO.setup(GPIO_right, GPIO.IN)
GPIO.setup(GPIO_middle, GPIO.IN)
GPIO.setup(GPIO_left, GPIO.IN)

try:
    # Start moving forward
    motors.setSpeeds(MAX_SPEED, MAX_SPEED)

    while True: # Main loop

        # Read sensor input (positive logic)
        INPUT_right  = not GPIO.input(GPIO_right)
        INPUT_middle = not GPIO.input(GPIO_middle)
        INPUT_left   = not GPIO.input(GPIO_left)

        # Set motor speeds dependent on sensor input
        if INPUT_left and INPUT_right:
            # Obstacle immediately ahead: move a bit bwrd,
            # turn left a little bit and then proceed fwrd
            motors.setSpeeds(-200, -200)
            sleep (1)
            motors.setSpeeds(-200, 200)
            sleep (0.3)
            motors.setSpeeds(MAX_SPEED, MAX_SPEED)

        elif INPUT_middle: # turn left
            motors.setSpeeds(100, MAX_SPEED)

        elif INPUT_left: # turn right
            motors.setSpeeds(MAX_SPEED, 200)

        elif INPUT_right: # turn left
            motors.setSpeeds(200, MAX_SPEED)
        else:
            # No sensor input: drive forward
            motors.setSpeeds(MAX_SPEED, MAX_SPEED)

        # Repeat this loop every 0.1 seconds
        sleep (0.1)

finally:
    # Stop motors in case of <Ctrl-C> or SIGTERM:
    motors.setSpeeds(0, 0)
