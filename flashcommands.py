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
#  Y9->X12 - pin 42 IO:5
IO5 = pyb.Pin('X12', pyb.Pin.OUT_PP)
# Y10 - pin 43 IO:6
IO6 = pyb.Pin('Y4', pyb.Pin.OUT_PP)
# Y11 - pin 44 IO:7
IO7 = pyb.Pin('Y11', pyb.Pin.OUT_PP)

#  Y5 - pin 19 WP# Output

#  Y6 - pin 18 WE# Output
WE_ = pyb.Pin('Y6', pyb.Pin.OUT_PP)

#  Y7 - pin 17 ALE Output
ALE = pyb.Pin('Y7', pyb.Pin.OUT_PP)

#  Y8 - pin 16 CLE Output
CLE = pyb.Pin('Y8', pyb.Pin.OUT_PP)

#  X9 - pin 9  CE# Output
CE_ = pyb.Pin('X9', pyb.Pin.OUT_PP)

# X10 - pin 8  RE#
RE_ = pyb.Pin('X10', pyb.Pin.OUT_PP)

# X11 - pin 7  R/B#  ready - busy
READY = pyb.Pin('X11', pyb.Pin.IN, pyb.Pin.PULL_UP)

def switchIOPinsToInput():
    # switch to input mode
    IO0 = pyb.Pin('X4', pyb.Pin.IN)
    IO1 = pyb.Pin('X5', pyb.Pin.IN)
    IO2 = pyb.Pin('X6', pyb.Pin.IN)
    IO3 = pyb.Pin('X7', pyb.Pin.IN)
    IO4 = pyb.Pin('X8', pyb.Pin.IN)
    IO5 = pyb.Pin('X12', pyb.Pin.IN)
    IO6 = pyb.Pin('Y4', pyb.Pin.IN)
    IO7 = pyb.Pin('Y11', pyb.Pin.IN)

def switchIOPinsToOutput():
    # put it back to output mode
    IO0 = pyb.Pin('X4', pyb.Pin.OUT_PP)
    IO1 = pyb.Pin('X5', pyb.Pin.OUT_PP)
    IO2 = pyb.Pin('X6', pyb.Pin.OUT_PP)
    IO3 = pyb.Pin('X7', pyb.Pin.OUT_PP)
    IO4 = pyb.Pin('X8', pyb.Pin.OUT_PP)
    IO5 = pyb.Pin('X12', pyb.Pin.OUT_PP)
    IO6 = pyb.Pin('Y4', pyb.Pin.OUT_PP)
    IO7 = pyb.Pin('Y11', pyb.Pin.OUT_PP)

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
    RE_.high()
    WE_.low()
    switchIOPinsToOutput()
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

def sendAddress(addr):
    CE_.low()
    CLE.low()
    ALE.high()
    WE_.low()
    switchIOPinsToOutput()
    IO0.value(addr & 0b00000001)
    IO1.value(addr & 0b00000010)
    IO2.value(addr & 0b00000100)
    IO3.value(addr & 0b00001000)
    IO4.value(addr & 0b00010000)
    IO5.value(addr & 0b00100000)
    IO6.value(addr & 0b01000000)
    IO7.value(addr & 0b10000000)
    WE_.high()
    ALE.low()

    time.sleep_us(1) # tWB=100ns
    while isBusy():
        time.sleep_us(10)

def sendPageAddress(addr):
    """ page addresses are 3 bytes long """
    CE_.low()
    CLE.low()
    ALE.high()
    switchIOPinsToOutput()
    remainingBytes = 3
    while( remainingBytes > 0):
        WE_.low()
        time.sleep_us(1)
        IO0.value(addr & 0b00000001)
        IO1.value(addr & 0b00000010)
        IO2.value(addr & 0b00000100)
        IO3.value(addr & 0b00001000)
        IO4.value(addr & 0b00010000)
        IO5.value(addr & 0b00100000)
        IO6.value(addr & 0b01000000)
        IO7.value(addr & 0b10000000)
        WE_.high()
        time.sleep_us(1)
        remainingBytes -= 1
        addr = addr >> 8
        
    WE_.high()
    ALE.low()

    time.sleep_us(1) # tWB=100ns
    while isBusy():
        time.sleep_us(10)


def readBytes(count):
    """ assume CE_ is already asserted and ready is high """
    result = []
    switchIOPinsToInput()

    for i in range(0, count):
        RE_.low()
        time.sleep_us(5)
        RE_.high()
        result.append(IO0.value() + (IO1.value() << 1) + (IO2.value() << 2) + (IO3.value() << 3) +
                      (IO4.value() << 4) + (IO5.value() << 5) + (IO6.value() << 6) + (IO7.value() << 7))
        time.sleep_us(30)

    CE_.high()
    return result

def isBusy():
    return not READY.value()

def readId():
    sendCommand(0x90)
    sendAddress(0x00)
    return readBytes(4)

def readId2():
    sendCommand(0x90)
    sendAddress(0x20)
    return readBytes(4)

def readStatus():
    sendCommand(0x70)
    return readBytes(1)

def readUniqueID():
    sendCommand(0xED)
    sendAddress(0x00)
    return readBytes(32)

def readStatusEnhanced(pageNum):
    sendCommand(0x78)
    sendPageAddress(pageNum)
    return readBytes(1)