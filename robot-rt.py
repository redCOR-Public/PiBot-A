#!/usr/bin/env python

from __future__ import print_function
from pololu_drv8835_rpi import motors, MAX_SPEED
from time import sleep
import signal, sys
def sigterm_handler(signal, frame):
    motors.setSpeeds(0, 0)
    sys.exit(0)
 
signal.signal(signal.SIGTERM, sigterm_handler)

try:
    while True:
        motors.setSpeeds(0, 0)
    
        print ("left forward")
        motors.setSpeeds(MAX_SPEED, 0)
        sleep (2)
    
        print ("left backward")
        motors.setSpeeds(-MAX_SPEED, 0)
        sleep (2)
    
        print ("right forward")
        motors.setSpeeds(0, MAX_SPEED)
        sleep (2)
    
        print ("right backward")
        motors.setSpeeds(0, -MAX_SPEED)
        sleep (2)

finally:
    motors.setSpeeds(0, 0)
