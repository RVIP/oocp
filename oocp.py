# Scan the OOCP Keyboard and send OSC events


import CCore
# import RPi.GPIO as GPIO  
import FakeRPiGPIO as GPIO
import time  

# outputs: 1
# inputs 
scanList = [
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

# current state of each key
prev = [0]*len(scanList)

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

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  

def sendKey(keyname, state):
    # send the osc message [keyname, state], where 1 is PRESSED 
    if state:
        val = 1
    else:
        val = 0
    osc.send("/oocp", [keyname, val])

def test(keymap):
    # return the current state of a pin pair
    outPin = pinMap[keymap[0]]
    inPin  = pinMap[keymap[1]]
    GPIO.setup(outPin, GPIO.OUT)
    GPIO.setup(inPin, GPIO.IN)
    cur = GPIO.input(inPin)
    print "pin %s = %s" % (inPin, cur)
    return cur

def debounce(index, cur, k):
    # place to insert debouncing, currently, result is instantaneous
    if(prev[index]!=cur):
        prev[index]=cur
        sendKey(k[2], cur)

def scan(scanList):
    # itterate through the list 
    index = 0
    for k in scanList:
        cur = test(k)
        debounce(index,cur,k)
        index += 1

scan(scanList)
