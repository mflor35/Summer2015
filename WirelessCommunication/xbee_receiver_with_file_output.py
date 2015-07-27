# -*- coding: utf-8 -*-
"""
radios_with_file_output - Xbee RECEIVER

Kapil Sinha
07/06/15

Receives the packets from the xbee transmitter and writes the raw dictionary results to tweetawatt_data.txt.
"""

from xbee import XBee
import serial
tweetawatt = open('Noisy_Zeros4.txt', 'w')
#Change serial port to COM1,COM2... when running this script on a Windows machine.
ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(ser)
while True:
    try:
        response = xbee.wait_read_frame()
        response = dict(response)
        tweetawatt.write(str(response)+"\n")
    except KeyboardInterrupt:
        break
ser.close()
