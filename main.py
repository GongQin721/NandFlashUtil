# main.py -- put your code here!
import pyb
from flashcommands import reset, readId2, readId, readStatus, readUniqueID, readStatusEnhanced
pyb.LED(4).on()

reset()
#result = readId2()
#print(['0x%02x' % x for x in result])
result = readId()
print(['0x%02x' % x for x in result])

result = readStatus()
print('status:')
print(['0x%02x' % x for x in result])

result = readUniqueID()
print('unique id:')
print(['0x%02x' % x for x in result])

result = readStatusEnhanced(0)
print('status of page 0')
print(['0x%02x' % x for x in result])

#result = readPage(0)
#print('contents of page 0')
#print(['0x%02x' % x for x in result])

