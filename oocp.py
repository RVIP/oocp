# Scan the OOCP Keyboard and send OSC events


import CCore
import RPi.GPIO as GPIO  
import time  

# outputs: 1
# inputs 
keyList = [
#    [ 1, 1,"A"],
#    [ 1, 1,"D"],
    [ 1, 3,"Down"],
    [ 1, 4,"Not"],
    [ 1, 5,"Delete"],
    [ 1, 6,"Up"],
    [ 1,10,"Left"],
    [ 1,11,"Insert"],
    [ 2, 7,"Right"],
    [ 2,12,"0"],
    [ 2,14,"8",],
    [ 3, 7,"Text"],
    [ 3,12,"6"],
    [ 4, 7,"Row",],
    [ 4, 9,"Cont"],
    [ 4, 9,"List"],
    [ 4,12,"1"],
    [ 4,14,"9"],
    [ 5, 7,"Format"],
    [ 5,12,"4"],
    [ 5,14,"C"],
    [ 5,14,"E",],
    [ 6, 7,"Mode"],
    [ 6,12,"5"],
    [ 7,11,"Blank"],
    [ 7,13,"Stop"],
    [10,12,"7"],
    [10,14,"F"],
    [11,14,"B"],
    [12,11,"3"],
    [12,13,"2"]
    ]

# map keyboard pins to GPIO pins {keyboard:GPIO, ...}
def pinMap = {1:11}

def sendKey(keyname, state):
    # send the osc message [keyname, state], where 1 is PRESSED 
    osc.send("/oocp", [keyname, state])

def test(keymap):
    outPin = pinMap[keymap[0]]
    inPin  = pinMap[keymap[1]]
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.setup(inPin, GPIO.IN)
    print GPIO.input(inPin)

# initialization 
osc = CCore.CCore(pubsub="osc-udp:") # use default bidirectional multicast

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  

# set up GPIO output channel  
GPIO.setup(11, GPIO.OUT)  

GPIO.cleanup()   

# blinking function  
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  
        return  
