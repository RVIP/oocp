# Scan the OOCP Keyboard and send OSC events

import CCore
import RPi.GPIO as GPIO  
# import FakeRPiGPIO as GPIO
import time  

# outputs: 1
# inputs 
scanList = [
    [ 1, 13, "NoCare"],
    [ 1, 3,"Down"],
    [ 1, 4,"Not"],
    [ 1, 5,"Delete"],
    [ 1, 6,"Up"],
    [ 1,10,"Left"],
    [ 1,11,"Insert"],
    [ 13, 14,"A"],
    [ 2, 1,"End"],
    [ 2, 7,"Right"],
    [ 2, 9,"Select"],
    [ 2,12,"0"],
    [ 2,14,"8",],
    [ 3, 7,"Text"],
    [ 3,12,"6"],
    [ 3,14,"E",],
    [ 4, 7,"Run",],
    [ 4, 9,"Cont"],
    [ 4,12,"1"],
    [ 4,14,"9"],
    [ 5, 7,"Format"],
    [ 5,12,"4"],
    [ 5,14,"C"],
    [ 6, 14,"D"],
    [ 6, 7,"Mode"],
    [ 6,12,"5"],
    [ 7,10,"List"],
    [ 7,11,"Blank"],
    [ 7,13,"Stop"],
    [10,12,"7"],
    [10,14,"F"],
    [11,14,"B"],
    [12,11,"3"],
    [12,13,"2"]
    ]

# current state of each key
prev = [1]*len(scanList)

# symbolic names to board pin#s
GPIO0=3     # sda
GPIO1=5     # scl
GPIO4=7     # cpclk0
GPIO14=8    # txd
GPIO15=10   # rxd
GPIO17=11
GPIO18=12   # pcm_clk
GPIO21=13
GPIO22=15	# pcm_dout
GPIO23=16
GPIO24=18
GPIO10=19   # mosi
GPIO9=21    # miso
GPIO25=22
GPIO11=23   # sclk
GPIO8=24    # ce0
GPIO7=26    # ce1

# mapped to pins 1-8 of oocp
MOSI=GPIO10
MISO=GPIO9
SCLK=GPIO11
CS0=GPIO8
CS1=GPIO7
SDA=GPIO0
SCL=GPIO1
TXD=GPIO14

# mapped to pins 9-16 of oocp
# GPIO17, GPIO18, GPIO21, GPIO22, GPIO23, GPIO24, GPIO25, GPIO4

pinMap = {1:MOSI, 2:MISO, 3:SCLK, 4:CS0, 5:CS1, 6:SDA, 7:SCL, 8:TXD,
          9:GPIO17, 10:GPIO18, 11:GPIO21, 12:GPIO22, 13:GPIO23, 14:GPIO24, 15:GPIO25, 16:GPIO4}

# initialization 
osc = CCore.CCore(pubsub="osc-udp:") # use default bidirectional multicast

# use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  

def sendKey(keyname, state):
    # send the osc message [keyname, state], where 1 is PRESSED 
    print "key = %s %s" % (keyname, state)
    if state:
        val = 0
    else:
        val = 1
    osc.send("/oocp", [keyname, val])

def settle():
    time.sleep(0.001)

def waitFor1(pin, count):
    while count:
        if GPIO.input(pin):
            return True
        count -= 1
    return False

def stay0(pin, count):
    while count:
        if GPIO.input(pin):
            return False
        count -= 1
    return True

def test(keymap):
    # return the current state of a pin pair
    # Note: Output pins set to 1, when read will FLOAT!
    # There for, we use this cunning plan!
    # We will set out output pin to 1, we will wait some number of
    # cycles for a 1 to appear, if it doesn't we will record NO CHANGE
    # for that button.
    # We then set our output pin to 0 and wait for N consecutive reads
    # of 0, if we get them, we'll call that PRESS, if we don't a RELEASE
    # All this to avoid pull up resistors
    outPin = pinMap[keymap[0]]
    inPin  = pinMap[keymap[1]]
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.setup(inPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.output(outPin,1)
    if(not waitFor1(inPin, 50)):
        return -1	# no confidence
    GPIO.output(outPin,0)
    settle()
    if(stay0(inPin, 300)):
        cur = 0
    else:
        cur = 1
    GPIO.setup(outPin, GPIO.IN)	# leave pins in INPUT mode to protect board
    # print "pin %s/%s = %s" % (keymap[0],inPin, cur)
    return cur

MAX=10
RELEASE=5
PRESS=0

def debounce(index, cur, k):
    # if 1 add to prev (up to MAX)
    # if now at RELEASE, trigger RELEASE, set prev to MAX
    # if previous not 0, and cur = 0, subtract 1, if now 0 - trigger PRESS
    # if(cur && prev[index]<MAX):
    #     prev[index]+= 1
    # raw:
    if(prev[index]!=cur):
        prev[index]=cur
        sendKey(k[2], cur)

def scan(scanList):
    # itterate through the list 
    index = 0
    for k in scanList:
        # print k
        cur = test(k)
        if cur >= 0:	# -1 for no confidence
            debounce(index,cur,k)
        index += 1

def tmp():
    while True:
        scan([[1,9,"HEY"]])
        time.sleep(0.05)

def loop(sl):
    while True:
        scan(sl)
        # print "."


loop(scanList)


    
