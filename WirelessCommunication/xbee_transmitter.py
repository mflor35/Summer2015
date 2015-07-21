''' Transmits packets using xbees'''
import XBee
xbee = XBee.XBee("/dev/ttyUSB0")  # Your serial port name here
sent = xbee.SendStr(voltage)
