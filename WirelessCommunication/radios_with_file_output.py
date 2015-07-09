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
from time import sleep
voltage_output = open('C:/Users/Vikesh/Desktop/voltage_output.txt', 'w')
voltage_output.close()
frequency_output = open('C:/Users/Vikesh/Desktop/frequency_output.txt', 'w')
frequency_output.close()
ser = serial.Serial('COM7', 9600)
xbee = XBee(ser)
i = 0 #counter for the response (assuming odd is voltage and even is frequency)
while True:
    try:
        sleep(2)
        voltage_output = open('C:/Desktop/voltage_output.txt', 'a')
        frequency_output = open('C:/Desktop/frequency_output.txt', 'a')
        response = xbee.wait_read_frame()
        i+=1
        if i%2==1: # If odd line (voltage measurement)
            voltage_output.write(str(response))
        else: #If even line (frequency measurement)
            frequency_output.write(str(response))
        voltage_output.close()
        frequency_output.close()
    except KeyboardInterrupt:
        break
ser.close()