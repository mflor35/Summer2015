# Calibrating Sensors (tweet-a-watt)

In order to normalize sensor data we need to eliminate the ADC-4 bias. This value is specific to each sensor.

## Get Noisy Zeros.
1. Plug in the sensor and let it run for a couple minutes.

2. Run the script called __xbee_reciever_with_file_outpu.py__ provide an output file name and make note of it, you'll need it for the calibrations python script. Let the script run for about 5 minutes. Use ``` Ctrl-c ``` to stop the script.

3. Run the calibration script in __DataAnalysis/Calibrate_Sensor.py__ and give it the file you got a from the previous script.

4. Take note of the SensorID (XBee address) and the value provided.
