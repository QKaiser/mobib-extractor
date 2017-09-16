#!/usr/bin/env python

from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.Exceptions import NoCardException
import sys

# select first smartcard reader by default
r=readers()
if not len(r):
    print "[!] No reader connected."
    sys.exit(-1)
else:
    print "[+] Connecting to %s" % r[0]

try:
    connection = r[0].createConnection()
    connection.connect()
except NoCardException as e:
    print "[!] Insert a card in the reader, dummy."
    sys.exit(-1)



# select ICC
s = "80 A4 08 00 04 3F 00 00 02"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
if sw2 == 0x19:
    s = "80 B2 01 04 1D"
    read_1record = toBytes(s) #intermediate if 0X612A
    data,sw1,sw2 = connection.transmit(read_1record)
    print "ICC: %s" % (toHexString(data))
else:
    print ("Error in ICC select")


# select holder
s = "80 A4 08 00 04 3F 00 3F 1C"
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "RAPDU: %s %02x %02x" % (toHexString(data), sw1,sw2)
if sw2 == 0x19:
    s = "80 B2 01 04 1D"
    read_1record = toBytes(s)
    data,sw1,sw2 = connection.transmit(read_1record)
    print "Holder 1: %s" % (toHexString(data))
    s = "80 B2 02 04 1D"
    read_2record = toBytes(s)
    data,sw1,sw2 = connection.transmit(read_2record)
    print "Holder 2: %s" % (toHexString(data))
else:
    print ("Error in ICC select")

s = "00 A4 04 00 0E 31 54 49 43 2E 49 43 41 D0 56 00 01 91 01"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "RAPDU: %s %02x %02x" % (toHexString(data), sw1,sw2)
if sw2 == 0x2a:
    s = "00 C0 00 00 2A"
    read_1record = toBytes(s) #intermediate if 0X612A
    print "CAPDU: %s" % s
    data,sw1,sw2 = connection.transmit(read_1record)
    print ("UNKNOWN: %s" % (toHexString(data)))
else:
    print ("Error in ICC select")

s = "00 B2 01 3C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN1: %s" % (toHexString(data))

s = "00 B2 02 3C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN2: %s" % (toHexString(data))

s = "00 B2 01 CC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Counter: %s" % (toHexString(data))


s = "00 B2 01 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra1: %s" % (toHexString(data))
s = "00 B2 02 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra2: %s" % (toHexString(data))
s = "00 B2 03 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra3: %s" % (toHexString(data))
s = "00 B2 04 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra4: %s" % (toHexString(data))
s = "00 B2 05 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra5: %s" % (toHexString(data))
s = "00 B2 06 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra6: %s" % (toHexString(data))
s = "00 B2 07 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra7: %s" % (toHexString(data))
s = "00 B2 08 4C 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Contra8: %s" % (toHexString(data))

# EvLog1
s = "00 B2 01 BC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "EvLog1:  %s" % (toHexString(data))

# EvLog2
s = "00 B2 02 BC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
#print "EvLog2:  %s" % (toHexString(data))

# EvLog3
s = "00 B2 03 BC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "EvLog3:  %s" % (toHexString(data))

s = "00 B2 04 BC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "EvLog4?: %s" % (toHexString(data))

s = "00 B2 01 EC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN1: %s" % (toHexString(data))
s = "00 B2 02 EC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN2: %s" % (toHexString(data))
s = "00 B2 03 EC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN3: %s" % (toHexString(data))
s = "00 B2 04 EC 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN4: %s" % (toHexString(data))

s = "00 B2 01 B4 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "UNKNOWN1: %s" % (toHexString(data))

s = "00 B2 01 F4 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "ConList:  %s" % (toHexString(data))
s = "00 A4 04 00 0B A0 00 00 02 91 D0 56 00 01 90 01"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "RAPDU: %s %02x %02x" % (toHexString(data), sw1,sw2)

if sw1 == 0x90 and sw2 == 0x00:
    s = "00 C0 00 00 00"
    read_1record = toBytes(s) #intermediate if 0X9000
    print "CAPDU: %s" % s
    data,sw1,sw2 = connection.transmit(read_1record)
    print ("RAPDU:     %s %02x %02x" % (toHexString(data), sw1, sw2))
    if sw1 == 0x6c and sw2 == 0x27:
        s = "00 C0 00 00 27" #intermediate if 0X6C27 RAPDU
        read_2record = toBytes(s)
        print "CAPDU: %s" % s
        data,sw1,sw2=connection.transmit(read_2record)
        print ("UNKNOWN:     %s" % (toHexString(data)))
    else:
        print("Error in 0X6C27 read")
else:
    print ("Error in 0X900 read")


s = "00 B2 01 E4 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Holder1: %s" % (toHexString(data))
s = "00 B2 02 E4 1D"
print("CAPDU: %s"%s)
select_command = toBytes(s)
data,sw1,sw2 = connection.transmit(select_command)
print "Holder2: %s" % (toHexString(data))
