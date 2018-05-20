import time
import pyb

#  X4 - pin 29 IO:0
#  X5 - pin 30 IO:1
#  X6 - pin 31 IO:2
#  X7 - pin 32 IO:3
#  X8 - pin 41 IO:4
#  Y9 - pin 42 IO:5
# Y10 - pin 43 IO:6
# Y11 - pin 44 IO:7
#  Y5 - pin 19 WP#
#  Y6 - pin 18 WE#
#  Y7 - pin 17 ALE
#  Y8 - pin 16 CLE
#  X9 - pin 9  CE#
# X10 - pin 8  RE#

# X11 - pin 7  R/B#  ready - busy
READY = pyb.Pin('X11', pyb.Pin.IN, pyb.Pin.PULL_UP)

def reset():
    """ command of xFF after waiting for R/B# 
     """
    command(0xff)

def command(cmd):
    """ place command on IO[0:7] assert CLE deassert ALE assert CE#  """

    while isBusy():
        time.sleep(1)



def isBusy():
    return not READY.value()