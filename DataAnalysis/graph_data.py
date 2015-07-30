#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from xbee import XBee
import serial
import numpy as np
#COUNTER = 0
"""
normalizeData takes in analog readings of the  current(adc-4) and the volatage(adc-0).
It also takes in the sensorAddr(source_addr) simply to keep track where is the data comming from

@voltage:  a list of 19 analog readings [672, 801, 864, 860, 755, 607, 419, 242, 143, 108, 143, 253, 433, 623, 760, 848, 871, 811]
@current:  a list of 19 analog readings [492, 492, 510, 491, 492, 491, 491, 491, 492, 480, 492, 492, 492, 492, 492, 492, 497, 492]
"""
__authors__ = ["Miguel Flores Silverio (miguelflores6182@stuent.hartnell.edu)"]
__author__ = ', '.join(__authors__)
__copyright__ = """Copyright © 2015 The Regents of the University of California
All Rights Reserved"""
__credits__ = ["Zachary Graham", "Kapil Sinha", "Miguel Flores Silverio", "Andres Aranda"]
__status__ = "prototype"
__license__ = """Copyright © 2015, The Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
     * Neither the name of Center for Sustainable Energy and Power Systems nor
       the names of its contributors may be used to endorse or promote products
       derived from this software without specific prior written permission.
     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""

def getSensorReading(serialPort):
    """
    Read data from sensor.

    serial_port: A string with the port number where the xbee reciever is connected
    for windows system is something like 'COM3','COM4'.. etc
    for Linux/Unix systems should be something lik '/dev/ttyUSB0', '/dev/ttyUSB1' ...etc

    """
    ser = serial.Serial(serialPort,9600) # Serial port to which the reciever is connected
    xbee = XBee(ser)                         # Xbee object
    response = xbee.wait_read_frame() # get reading
    response['timestamp'] = datetime.now()
    ser.close()
    return response

def updateGraph(current,voltage,graph):
    """Updates the currenta and voltage values in the specified graph.

    current: List of already normalized current values.
    [-0.375, 0.0625, 0.375, 0.625, 0.75, 0.625, 0.3125, 0.0, -0.4375, -0.625, -0.75, -0.625, -0.375, 0.0, 0.375, 0.625, 0.75, 0.625, 0.3125]

    voltage: List of already normalize voltage values.
    [-92, -1, 78, 137, 163, 144, 81, 1, -87, -142, -164, -142, -83, 3, 84, 144, 164, 136, 76]

    graph: Intance of a matplotlib figure object (graph = plt.figure())

    """
    graphVoltage = graph.add_subplot(111) # Add a plot and a subplot to our figure. In this case our main plot is the voltage graph
    graphCurrent = graphVoltage.twinx()   # Add the Current graph as a subplot
    graphVoltage.plot(voltage,'r')        # Plot the voltage values (red line)
    graphCurrent.plot(current,'b')        # Plot the current values (blue line)
    vLegend = mpatches.Patch(color='red',label='Voltage')  # Create volatage patch for plot legend
    cLegend = mpatches.Patch(color='blue',label='Current') # Create current patch for plot legend
    graphVoltage.set_xlabel("Sample")     # X axis label
    graphVoltage.set_ylabel("Voltage")    # y axis label for the voltage data (This is displayed on the right of the graph)
    graphCurrent.set_ylabel("Current")    # y axis labe for current data (This is displayed on the left of the graph)
    graphCurrent.set_ylim(-1.2,1.2)       # set y axis limits for current values
    graph.legend([vLegend,cLegend],["Voltage","Current"]) # Add the legend patches to the graph/figure
    graph.canvas.draw()                   # Show the graph
    graphCurrent.cla()                    # Clear the voltage data.
    graphVoltage.cla()                    # Clear the current data.

def createGraph(sensorID):
    """
    Creates a graph for the specified sensor

    sensorID: XBee address
    """
    plt.ion()
    graph = plt.figure()
    graph.suptitle(sensorID,fontsize=12,fontweight='bold')
    return graph,sensorID

def getAnalogData(reading):
    """
    Parse the reading to just get the analog values and return them.

    reading: A json string that can be evaluated into a dictionary.

    """
    # make sure it is a python dictionary. if it is not break the program
    adc0 = []                     # List of all adc-0 analog value in the packet (Analog voltage readings)
    adc4 = []                     # List of all adc-4 analog value in the packet (Analog current readings)
    sensorAddr = reading['source_addr'].encode('hex') # Which sensor is the packet coming from
    for sample in reading['samples']: # iterate through each of the anlog samples and put them in their correpoding list
        adc0.append(sample['adc-0'])  # add all adc-0 values to adc0 list
        adc4.append(sample['adc-4'])  # add all adc-4 values to adc4 list

    return adc0,adc4,sensorAddr
def normalizeData(voltage,current,sensorVREF):
    """
    Turn all the analog data into proper voltage and current values.
    voltage: The list of analog voltage values from the sensor
    current: The list of analog current values from the sensor
    sensorVREF: ADC-4 bias to normalize the curve to zero. varies per sensor.

    """
    # Normalize the curve to zero
    # From and more at Adafruit design https://learn.adafruit.com/tweet-a-watt/design-listen
    MAINSVPP = 164 * 2 # +-164V
    VREF = sensorVREF  # Varies per sesnsor
    CURRENTNORM = 15.5 # Normalizing constant that converts the analog reading to Amperes
    min_v = 1024       # XBee ADC is 10 bits, so max value is 1023
    max_v = 0
    # Find the smallest voltage and the biggest voltage in the list of samples taken
    for v in voltage:
        if(min_v > v):
            min_v = v
        if(max_v < v):
            max_v = v
    # Average of the biggest  and smallest voltage samples
    avg_voltage = (min_v + max_v) / 2
    # Calculate  the peak to peak measurement
    vpp = max_v - min_v
    for index in range(len(voltage)):
        # Remove 'dc-bias', which is the average reading
        try:
            voltage[index] -= avg_voltage
            voltage[index] = (voltage[index] * MAINSVPP) / vpp
            # Normalize current reading to amperes
        except:
            pass
    for index in range(len(current)):
        try:
            current[index] -= VREF
            current[index] /= CURRENTNORM
        except:
            pass
    return voltage,current
def liveData():
    """
    Get live data from the sensor
    """
    listGraphs = []
    sensorsConnected = []# List of all the graph (Keeps track of all the graphs being displayed)
    calibratedSensors = []
    calibrationInfo = []
    while True:
        try:
            reading = getSensorReading('/dev/ttyUSB0')
            adc0, adc4, id = getAnalogData(reading)
            sensorInfo = [id,reading['timestamp'],[]]
            if sensorInfo[0] not in sensorsConnected:
                print "Adding sensor: " + sensorInfo[0]
                sensorsConnected.append(sensorInfo[0])
                calibrationInfo.append(sensorInfo)
                graph,graphID = createGraph(sensorInfo[0]) # Create a graph for all the sensor that do have a graph yet
                listGraphs.append((graph,sensorInfo[0]))
            if sensorInfo[0] not in calibratedSensors:
                for sensor in calibrationInfo:
                    if(sensor[0] == sensorInfo[0]):
                        elapsedTime = int((datetime.now() - sensor[1]).total_seconds())
                        if(elapsedTime <= 60):
                            print "Time current - added: ", elapsedTime
                            print "Calibrating..."
                            sensor[2] += adc4
                        else:
                            calibratedSensors.append(sensorInfo[0])
            else:
                print id + " Sensor already calibrated"
                for sensor in calibrationInfo:
                    sensor[2] = int(np.mean(sensor[2]))
                    if(id == sensor[0]):
                        voltage, current = normalizeData(adc0[2:],adc4[2:],sensor[2]) # turn analog data into actual voltage and current. discard first 2 analog readings from adc-0 and adc-4\
                        # Debuggin porpuses
                        print
                        print "Sensor ID:", id
                        print "Voltage"
                        print "Min:",min(voltage)
                        print "Max:",max(voltage)
                        print "Current"
                        print "Min:",min(current)
                        print "Max:",max(current)
                for graph in listGraphs:
                    if(graph[1] == id):
                        updateGraph(current,voltage,graph[0])
        except KeyboardInterrupt:
            break
def main():

    liveData() # Graphing data live
if __name__ == '__main__':
    main()
