import ast
from pylab import *
from time import sleep
def normalizeData(voltage,current):
    #Normalize the curve to zero
    #from Adafruit design https://learn.adafruit.com/tweet-a-watt/design-listen
    MAINSVPP = 170 * 2 # +-170V is what 120Vrms ends up being
    VREF = 498
    CURRENTNORM = 15.5

    max_v = 1023
    min_v = 0
    for v in voltage:
        if(v < min_v):
            min_v = v
        if(v > max_v):
            max_v = v
    # Average of the max and min of reading per sample
    avg_voltage = (min_v + max_v) / 2

    # Calculate  the peak to peak measurement
    vpp = max_v - min_v
    for index in range(len(voltage)):
        voltage[index] -= avg_voltage
        voltage[index] = (voltage[index] * MAINSVPP) / vpp
    # Normalize current reading to amperes
    for index in range(len(current)):
        current[index] -= VREF
        current[index] /= CURRENTNORM
    return voltage,current

def main():

    filepath = raw_input("Enter name of data file or path where it is located: ")
    data = open(filepath)
    ion()
    for reading in data:
        reading = reading.strip()
        adc0 = []
        adc4 = []
        cla()
        try:
            reading = ast.literal_eval(reading)
            for sample in reading['samples']:
               # voltage.append(sample['adc-0'])
               # current.append(sample['adc-4'])
                adc0.append(sample['adc-0'])
                adc4.append(sample['adc-4'])
            #print 'adc0:',adc0
            #print 'adc4:',adc4
            print
            voltage,current = normalizeData(adc0,adc4)
            print "V:",voltage
            print "C:",current
            print
            plot(voltage,'r',current,'b')
            draw()

            sleep(.3)
        except KeyboardInterrupt:
            break
main()
