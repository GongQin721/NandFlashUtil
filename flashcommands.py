import time
import pyb

#  X4 - pin 29 IO:0
IO0 = pyb.Pin('X4', pyb.Pin.OUT_PP)
#  X5 - pin 30 IO:1
IO1 = pyb.Pin('X5', pyb.Pin.OUT_PP)
#  X6 - pin 31 IO:2
IO2 = pyb.Pin('X6', pyb.Pin.OUT_PP)
#  X7 - pin 32 IO:3
IO3 = pyb.Pin('X7', pyb.Pin.OUT_PP)
#  X8 - pin 41 IO:4
IO4 = pyb.Pin('X8', pyb.Pin.OUT_PP)
#  Y9 - pin 42 IO:5
IO5 = pyb.Pin('Y9', pyb.Pin.OUT_PP)
# Y10 - pin 43 IO:6
IO6 = pyb.Pin('Y10', pyb.Pin.OUT_PP)
# Y11 - pin 44 IO:7
IO7 = pyb.Pin('Y11', pyb.Pin.OUT_PP)

#  Y5 - pin 19 WP# Output

#  Y6 - pin 18 WE# Output
WE_ = pyb.Pin('Y6', pyb.Pin.OUT_PP)

#  Y7 - pin 17 ALE Output

#  Y8 - pin 16 CLE Output
CLE = pyb.Pin('Y8', pyb.Pin.OUT_PP)

#  X9 - pin 9  CE# Output
CE_ = pyb.Pin('X9', pyb.Pin.OUT_PP)

# X10 - pin 8  RE#

# X11 - pin 7  R/B#  ready - busy
READY = pyb.Pin('X11', pyb.Pin.IN, pyb.Pin.PULL_UP)

def reset():
    """ command of xFF after waiting for R/B# 
     """
    sendCommand(0xff)
    while isBusy():
        time.sleep(1)
    print('Ready again after reset.')

def sendCommand(cmd):
    """ place lower 8 bits of cmd on IO[0:7] assert CLE deassert ALE assert CE#  """

    while isBusy():
        time.sleep(1)
    print('ready before sending command')
    CE_.low()
    CLE.high()

    WE_.low()
    IO0.value(cmd & 0b00000001)
    IO1.value(cmd & 0b00000010)
    IO2.value(cmd & 0b00000100)
    IO3.value(cmd & 0b00001000)
    IO4.value(cmd & 0b00010000)
    IO5.value(cmd & 0b00100000)
    IO6.value(cmd & 0b01000000)
    IO7.value(cmd & 0b10000000)
    WE_.high()
    time.sleep_us(1) # tWB=100ns
    CLE.low()
    CE_.high()



def isBusy():
    return not READY.value()