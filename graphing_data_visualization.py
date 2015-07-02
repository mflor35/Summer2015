# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:56:55 2015

@author: Kapil

This program is used for data visualization. I designed it to graph sunlight, power, and energy information generated from the solar panels at Hartnell, with the 48 datapoints on each graph (hourly for two days). It implements two files: xdatelist is a list generated from a file of the date and time (in the format mm/dd/yyyy t:tt) and ylist is a list generated from a file of the corresponding y values (power, energy, or insolation).

While several of the functions and formatting are used specifically for this purpose, this program also serves as a basic format for creating a scatterplot from two files and creating a PDF with all the graphs on separate pages.

This program will hopefully be useful for the latter step of real-time data visualization and will need to be adjusted for those circumstances (I broke up the data with another program and some crafty [sarcasm intended] handiwork of my own).
"""

from pylab import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def subtract_from_list(datalist, number):
    #reduces x values from generate_xValues() so that they are between 0 and 2
    new_datalist = []
    for item in datalist:
        item = float(item)-number
        new_datalist.append(item)
    return new_datalist
def get_datetime(xdatelist, day_start): #gives list of date&times for x axis
    n_xdatelist = []
    i = 0
    a = 2 * day_start
    while i<(len(xdatelist)/12):
        n_xdatelist.append(xdatelist[i*12])
        i+=1
    return n_xdatelist[a:a+5] #return the range of dates needed
def remove_year(xdate): #removes year from the date for the x-axis
    j = 0    
    k = 0
    new_xdatelist = []
    while k<len(xdate): #remove year
        a = xdate[k]
        if a[j] == " ":
            new_xdatelist.append(a[0:j-5]+a[j:])
            k+=1
            j = -1        
        j+=1
    return new_xdatelist
def remove_time(date): #removes time so that the date can be used for the title
    i = 0
    while i<len(date):
        if date[i] == " ":
            new_date = date[0:i]
        i+=1
    return new_date
def generate_xValues(): #provides x values (replaced with dates)
    i = 0
    xValues = []
    while i<2273:
        xValues.append(i/24.0)
        i+=1
    return xValues
###########DEPENDS ON ENERGY/POWER/SUNLIGHT(rename files and file locations)
yValues = open('C:\Desktop\sunlight_output_from_solar_panels\sunlight_output_Yvalues.txt', 'r')
xdateValues = open('C:\Desktop\sunlight_output_from_solar_panels\sunlight_output_Xvalues.txt', 'r')
pdf = PdfPages('C:\Desktop\sunlight_output_from_solar_panels\sunlight_graphs.pdf')

a = 0; b = 48; j = 0 
xlist = generate_xValues()
ylist = yValues.readlines() #convert raw data into lists
yTitle = ylist[0] # y-axis title
ylist.pop(0) #Remove title from the data list
xdatelist = xdateValues.readlines()
xdatelist.pop(0)
xTitle = "Date and Time" # x-axis title    
while b<len(ylist):
    plt.xlabel(xTitle, fontsize=12)
    x = xlist[a:b] #get the relevant list of dates
    xdate = get_datetime(xdatelist, a/24) #gets dates for the x-axis
    xdate_without_year = remove_year(xdate)
    x = subtract_from_list(x,2*j) #subtract number to keep x values 0<x<2
    plt.xticks([0,.5,1,1.5,2], xdate_without_year) #replaces number x-axis values with date
    plt.ylabel(yTitle, fontsize=12)
    y = ylist[a:b]
    plt.suptitle(str(remove_time(xdate[0])) + " to " + str(remove_time(xdate[2])), fontsize=15)
    plt.xlim([0,2])
    plt.ylim([0,900]) ###########DEPENDS ON ENERGY(500)/POWER(500)/SUNLIGHT(900)
    plt.subplots_adjust(left=0.15, right=0.9, top=.9, bottom=0.18) #adjust margins
    scatter(x,y)
    pdf.savefig()
    plt.cla() #clear graph (so that you can make a new one)
    a+=48; b+=48; j+=1
pdf.close()
xdateValues.close()
yValues.close()
