import matplotlib.pyplot as plt
from time import sleep
import matplotlib.patches as mpatches
from xbee import XBee
from xbee.base import TimeoutException
import serial
from datetime import datetime

TIMEOUT=2
MEASUREMENT_PERIOD=5
DATAFILE="waterHeaterTemp.csv"

def getSensorReading(xbee):
    """
    Read data from sensor.
    TODO: SerialPort is an object

    serial_port: A string with the port number where the xbee reciever is connected
    for windows system is something like 'COM3','COM4'.. etc
    for Linux/Unix systems should be something lik '/dev/ttyUSB0', '/dev/ttyUSB1' ...etc

    """
    response = xbee.wait_read_frame(timeout=1)   # get reading
    response['timestamp'] = datetime.now()
    return response

def updateGraph(temp,graph):
    """Updates the currenta and voltage values in the specified graph.
    graph: Intance of a matplotlib figure object (graph = plt.figure())

    """
    graph.plot(temp,'r')                                       # Plot the voltage values (red line)
    tLegend = mpatches.Patch(color='red',label='Temperature')  # Create volatage patch for plot legend
    graph.set_xlabel("Time")                                   # X axis label
    graph.set_ylabel("Temperature")                            # y axis label for the voltage data (This is displayed on the right of the graph)
    graph.legend([tLegend],["Temperature"])                    # Add the legend patches to the graph/figure
    graph.canvas.draw()                                        # Show the graph
    graph.cla()                                                # Clear the current data.

def format(msg):
    """
    Formats a byte or bytearray object into a more human readable string
    where each bytes is represented by two ascii characters and a space

    Input:
    msg: A bytes or bytearray object

    Output:
    A string representation
        """
    return " ".join("{:02x}".format(b) for b in msg)

def Escape(msg):
    """
    Escapes reserved characters before an XBee message is sent.
    Inputs:
    msg: A bytes or bytearray object containing an original message to be sent to an XBee

    Outputs:A bytearray object prepared to be sent to an XBee in API mode
    """
    escaped = bytearray()
    reserved = bytearray(b"\x7E\x7D\x11\x13")

    escaped.append(msg[0])
    for m in msg[1:]:
        if m in reserved:
            escaped.append(0x7D)
            escaped.append(m ^ 0x20)
        else:
            escaped.append(m)

    return escaped
def Send(serialPort, msg, addr=0xFFFF, options=0x01, frameid=0x00):
    """
    Inputs:
    msg: A message, in bytes or bytearray format, to be sent to an XBee
    addr: The 16 bit address of the destination XBee (default broadcast)
    options: Optional byte to specify transmission options (default 0x01: disable ACK)
    frameod: Optional frameid, only used if transmit status is desired
    Returns: Number of bytes sent
    """
    if not msg:
        return 0
    hexs = '7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}'.format(
        len(msg) + 5,           # LSB (length)
        frameid,
        (addr & 0xFF00) >> 8,   # Destination address high byte
        addr & 0xFF,            # Destination address low byte
        options
    )
    frame = bytearray.fromhex(hexs)
    #  Append message content
    frame.extend(msg)
    # Calculate checksum byte
    frame.append(0xFF - (sum(frame[3:]) & 0xFF))
    # Escape any bytes containing reserved characters
    frame = Escape(frame)
    print("Tx: " + format(frame))

    return serialPort.write(frame)

def turnWaterHeaterON():
    pass

def menu():

    print"================"
    print"Commands for water heater:"
    print"1.- ON"
    print"2.- OFF"
    print"3.- Status"
    print"4.- Set temperature offset"
    print"5.- Collect Temperature Data"
    print"0.- Exit"

def main():
    ser = serial.Serial('/dev/ttyUSB0',9600)
    Send(ser, 'Status!')
    xbee = XBee(ser)             # Xbee object
    reading = getSensorReading(xbee)
    print reading
    ser.timeout=TIMEOUT
    menu()
    choice = int(raw_input("Enter a option: "))
    while choice != 0:
        if(choice == 5):
            #open data file for writing
            with open(DATAFILE, 'w', buffering=1) as df:
                try:
                    while True:
                        ser.flush()
                        Send(ser,"Temp!")
                        while True:
                            try:
                                reading = getSensorReading(xbee)
                            except TimeoutException:
                                print "Timeout Occured"
                                Send(ser, "Temp!")
                            else:
                                break
                        print reading['rf_data']
                        #write to file
                        r=reading['rf_data'].replace("TEMPERATURE: ", "")
                        r=float(r.replace(" C\r\n",""))
                        df.write("{ts}, {temp}\n".format(ts=str(reading['timestamp']), temp=r))
                        sleep(MEASUREMENT_PERIOD)
                except KeyboardInterrupt:
                    reading=""
        elif(choice == 1 ):
            Send(ser,"ON!")
            reading = getSensorReading(xbee)
        elif(choice == 2):
            Send(ser,"OFF!")
            reading = getSensorReading(xbee)
        elif(choice == 3):
            Send(ser,"Status!")
            reading = getSensorReading(xbee)
        elif(choice == 4):
            offset = int(raw_input("Enter new temperature offset: "))
            Send(ser,"SetPoint: "+str(offset)+"!")
            reading = getSensorReading(xbee)
        print reading
        menu()
        choice = int(raw_input("Enter a option: "))

if __name__ == '__main__':
    main()
