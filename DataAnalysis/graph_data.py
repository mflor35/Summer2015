import ast
import matplotlib.pyplot as plt
from time import sleep
"""
normalizeData takes in analog readings of the  current(adc-4) and the volatage(adc-0).
It also takes in the sensorAddr(source_addr) simply to keep track where is the data comming from

@voltage:  a list of 19 analog readings [672, 801, 864, 860, 755, 607, 419, 242, 143, 108, 143, 253, 433, 623, 760, 848, 871, 811]
@current:  a list of 19 analog readings [492, 492, 510, 491, 492, 491, 491, 491, 492, 480, 492, 492, 492, 492, 492, 492, 497, 492]

"""
def normalizeData(voltage,current):
    # Normalize the curve to zero
    # From and more at Adafruit design https://learn.adafruit.com/tweet-a-watt/design-listen

    MAINSVPP = 164 * 2 # +-164V
    VREF = 498         # Hardcoded 'DC bias' value its about 492
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
        voltage[index] -= avg_voltage

        voltage[index] = (voltage[index] * MAINSVPP) / vpp

    # Normalize current reading to amperes
    for index in range(len(current)):
        current[index] -= VREF
        current[index] /= CURRENTNORM
    return voltage,current
def main():
    #filepath = raw_input("Enter name of data file or path where it is located: ")
    data = open("data_sample/rawdata1.txt")
    plt.ion()
    fig,ax1 = plt.subplots()
    ax2 = plt.twinx()
    for reading in data:
        reading = reading.strip()
        adc0 = []
        adc4 = []
        ax1.cla()
        ax2.cla()
        try:
            reading = ast.literal_eval(reading)
            sensorAddr = reading['source_addr']
            for sample in reading['samples']:
                adc0.append(sample['adc-0'])
                adc4.append(sample['adc-4'])
            voltage,current = normalizeData(adc0,adc4)
            print voltage
            ax1.plot(voltage,'r')
            ax1.set_xlabel("Sample #")
            ax1.set_ylabel("Voltage")
            ax2.plot(current,'b')
            ax2.set_ylabel("Current")
            sleep(1)
            plt.draw()
        except KeyboardInterrupt:
            break
main()
