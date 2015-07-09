import XBee
from time import sleep
if __name__ == "__main__":

    xbee = XBee.XBee("/dev/ttyUSB0")  # Your serial port name here

    # A simple string message
    sent = xbee.SendStr("Test 2")
    sleep(0.25)
    Msg = xbee.Receive()
    if Msg:
        content = Msg[7:-1].decode('ascii')
        print("Msg: " + content)
