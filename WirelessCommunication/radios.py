from xbee import XBee
import serial

ser = serial.Serial('/dev/ttyUSB1', 9600)
xbee = XBee(ser)
while True:
    try:
        response = xbee.wait_read_frame()
        print response
    except KeyboardInterrupt:
        break

ser.close()
