""" Transmits packets using xbees """
import XBee
command = raw_input("Enter Command: ")
xbee = XBee.XBee("/dev/ttyUSB0")  # Your serial port name here
sent = xbee.SendStr(command)
