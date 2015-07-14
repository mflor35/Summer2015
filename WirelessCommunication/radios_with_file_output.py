# -*- coding: utf-8 -*-
"""
radios_with_file_output - Xbee RECEIVER

Kapil Sinha
07/06/15

This receives the packets from the xbee transmitter.
It also saves the information received into a file. I will assume for now that
the transmitter file will transmit the voltage, followed by the frequency
"""

from xbee import XBee
import serial
from time import strftime
tweetawatt = open('tweetawatt_data.txt', 'w')
#Change serial port to COM1,COM2... when running this script on a Windows machine.
ser = serial.Serial('/dev/ttyUSB0', 9600)
xbee = XBee(ser)
i = 0 #counter for the response (assuming odd is voltage and even is frequency)
while True:
    try:
        response = xbee.wait_read_frame()
        response = dict(response)
        response["datestamp"] = strftime("%Y-%m-%d %H:%M:%S")
        tweetawatt.write(str(response)+"\n")
    except KeyboardInterrupt:
        break
ser.close()
