# just put some end points so we can develop w/o a Raspberry Pi
# usage:
# import FAKE.Rpi.GPIO as GPIO
#

pinsOut = [0]*17
pinsIn = [0]*17

# defs
OUT = "out"
IN = "in"
HIGH = 1
LOW = 0
BOARD = "board pin numbering mode"

import random

def setup(pin, mode):
    print "GPIO pin = %s   mode = %s" % (pin, mode)

def setmode(boardmode):
    print "Pin Mode = %s" % (boardmode)

def input(pin):
    if pin == 5:	# pin 5 is flakey!
        pinsIn[5] = bool(random.getrandbits(1))
    return pinsIn[pin]

def output(pin,val):
    pinsOut[pin]=val



