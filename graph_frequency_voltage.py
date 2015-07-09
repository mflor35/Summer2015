# -*- coding: utf-8 -*-
"""
graph_frequency_voltage - graph frequency and voltage over time

Kapil Sinha
07/07/15

This graphs the voltage and frequency data over time. It will be used with
radios_with_file_output.
"""

from pylab import *
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from time import sleep

def get_datetime(current_time): #gives list of date&times for x axis
    xdatelist = []
    i = 0
    original_time = current_time - 0:00:30.000000
    while i<6: # 5 values on x-axis
        xdatelist.append(original_time + (i*7.5))
        i+=1
    return xdatelist #return the range of dates needed
def generate_xValues(): #provides x values (replaced with time) - for 1 hour
    i = 0
    xValues = []
    while i<3600:
        xValues.append(i/3600)
        i+=2
    return xValues
###########Rename file locations
yValues_voltage = open('C:/Users/Vikesh/Desktop/voltage_output.txt', 'r')
yValues_frequency = open('C:/Users/Vikesh/Desktop/frequency_output.txt', 'r')
pdf1 = PdfPages('C:/Users/Vikesh/Desktop/voltage_graphs.pdf')
pdf2 = PdfPages('C:/Users/Vikesh/Desktop/frequency_graphs.pdf')
#The following statements should remain constant for the whole program. I will
#perhaps need to place the xdatelist portion in the loop later on.
a = 0; b = 60; j = 0 #Each graph will have the data for one minute.
xlist = generate_xValues()
yTitle_voltage = "Voltage"
yTitle_frequency = "Frequency"
xTitle = "Date and Time" # x-axis title    
while True: ####This is probably wrong. The loop somehow has to work with that
################radios_with_file_output
    sleep(60) '''Now the voltage graphs'''
    ylist_voltage = yValues_voltage.readlines() #convert raw data into lists
    plt.xlabel(xTitle, fontsize=12)
    x = xlist[a:b] #get the relevant list of dates
    current_time = datetime.datetime.now()
    xdate = get_datetime(current_time) #gets dates for the x-axis
    plt.xticks([0,.5,1,1.5,2], xdate) #replaces number x-axis values with date
    plt.ylabel(yTitle_voltage, fontsize=12)
    y = ylist_voltage[a:b]
    plt.suptitle(str(current_time - 0:00:30.000000) + " to " + str(current_time), fontsize=15)
    plt.xlim([0,60])
    plt.ylim([0,150]) # May be different
    plt.subplots_adjust(left=0.15, right=0.9, top=.9, bottom=0.18) #adjust margins
    scatter(x,y)
    pdf1.savefig()
    plt.cla() #clear graph (so that you can make a new one)
            '''Now the frequency graphs'''
    ylist_frequency = yValues_frequency.readlines()    
    plt.xlabel(xTitle, fontsize=12)
    x = xlist[a:b] #get the relevant list of dates
    current_time = datetime.datetime.now()
    xdate = get_datetime(current_time) #gets dates for the x-axis
    plt.xticks([0,.5,1,1.5,2], xdate) #replaces number x-axis values with date
    plt.ylabel(yTitle_frequency, fontsize=12)
    y = ylist_frequency[a:b]
    plt.suptitle(str(current_time - 0:00:30.000000) + " to " + str(current_time), fontsize=15)
    plt.xlim([0,60])
    plt.ylim([50,70]) # May be different
    plt.subplots_adjust(left=0.15, right=0.9, top=.9, bottom=0.18) #adjust margins
    scatter(x,y)
    pdf2.savefig()
    plt.cla() #clear graph (so that you can make a new one)
    a+=60; b+=60; j+=1
pdf1.close()
pdf2.close()
xdateValues.close()
yValues.close()