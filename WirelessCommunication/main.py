import XBee
import math
from time import sleep
def frange(start,end,step):
    while(start < end):
        yield start
        start += step
def voltageGenerator():
    sample_frequency = 4000.0
    delta_time = 1.0 / sample_frequency
    nominal_frequency = 60 #Nominal Frequency
    #testing_frequency = 59
    max_voltage = 120 #Amplitude of the test signal
    number_of_samples = 10000
    x = []
    for t in frange(delta_time,number_of_samples * delta_time,delta_time):
        x.append(max_voltage * math.sin(2 * math.pi * nominal_frequency * t))
    return x
xbee = XBee.XBee("/dev/ttyUSB0")  # Your serial port name here
for voltage in voltageGenerator():
    sleep(2)
    voltage = "%.5f"%voltage
    sent = xbee.SendStr(voltage)
