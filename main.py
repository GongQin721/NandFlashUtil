# main.py -- put your code here!
import pyb
from flashcommands import reset, readId2, readId
pyb.LED(4).on()

reset()
result = readId2()
print(['0x%02x' % x for x in result])
result = readId()
print(['0x%02x' % x for x in result])

