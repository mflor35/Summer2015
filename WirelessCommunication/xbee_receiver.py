'''Reads input from xbees - not used anymore and replaced by xbees_with_file_output'''

from xbee import XBee
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(ser)
while True:
    try:
        response = xbee.wait_read_frame()
        print response
    except KeyboardInterrupt:
        break

ser.close()
