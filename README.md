# Smart GRID: Summer Internship 2015
As a result of increasing use of renewable energy sources for power generation, the overall quality of electrical services has degraded. We propose a method that uses frequency as an indication of the current state of the grid and quality of power, and regulates it by deferring load consumption. We thus designed and are in the process of implementing an embedded system in a micro-grid testbed that regulates power frequency through control of the deferrable loads. Frequency measurements from a microcontroller’s counting hardware feature are transmitted wirelessly to a single board computer for further processing. An algorithm running from a single board computer accesses this information and determines when to turn on/off or change the threshold temperature the various deferrable loads, while accounting for certain aspects unique to each load. Considering these aspects allows the micro-grid testbed to potentially stabilize frequency and improve the quality of the power delivered.

## Master Plan (Preliminary) - update the files used by the master plan
### Method 1: Tweet-a-Watt & Single-Board-Computer
### Provides little precision in frequency reading (1 decimal place)

[__*Tweet-a-watt*__](https://learn.adafruit.com/tweet-a-watt/) transmits current and voltage readings.

__(A)__ Base XBee configured according to __WirelessCommunication/xbee_receiver_config.xml__ to automatically send current and voltage info.

__(B)__ Base XBee uses __xbee_receiver_with_file_output.py__ to read and save the readings to a file.

__(C)__ Tweet-a-Watt transmitter XBee configured according to [https://learn.adafruit.com/tweet-a-watt/make-it-configure]
2. Calculate frequency of power grid on Single-Board-Computer, determine state of loads, and visualize duty cycle
	a. Use the __CalcFrequency/aghazadeh_algo.py__ algorithm to calculate frequency using voltage (more precise than frequency from Kill-a-Watt)
	b. Use the __DataAnalysis/state_detector.py__ to determine whether the load is on or off
	c. Use the __DataAnalysis/state_analysis.py__ to determine how long the on/off state lasts in the load
	d. Send the state_analysis.py results to a monitor (serial cable?)  and graph the duty cycle using __DataAnalysis/graph_stateanalysis.py__
3. MAIN MASTER_CONTROL: Decide how to alter power consumption in each load and account for several variables:
	a. Refrigerator: Change temperature on thermostat - Duty Cycle (32.3%), etc.
	b. Water Heater: Change temperature on thermostat - Duty Cycle, etc.
	c. Car Battery?: Turn on/off? - Duty Cycle, etc.
4. Transmit directions to XBees controlling the various aspects of the loads
	a. Use __WirelessCommunication/xbee_transmitter.py__ to transmit the directions from the base XBee to the XBees on the loads
	b. We have not finished the actual controller of the loads - ask Carlo and Andres for more details

###(Superior) Method 2: Texas Instruments Meter & Single-Board-Computer
####Provides lots of precision in frequency reading (4 decimal places)
#####I just copied and pasted the same format from the above. I think you wanted the SBC to make the decision before the XBee sends the info back.
1. Frequency meter measures frequency and attached XBee transmits frequency (+ current? + voltage?) data to the base XBee
		a. Base XBee configured according to WirelessCommunication/xbee_receiver_config.xml to automatically send current and voltage info.
		b. Base XBee uses xbee_receiver_with_file_output.py to read and save the readings to a file
		c. Transmitter XBee configured according to https://learn.adafruit.com/tweet-a-watt/make-it-configure
2. Determine state of loads, and visualize duty cycle
	a. Use the __DataAnalysis/state_detector.py__ to determine whether the load is on or off
	b. Use the __DataAnalysis/state_analysis.py__ to determine how long the on/off state lasts in the load
	c. Send the state_analysis.py results to a monitor (serial cable?)  and graph the duty cycle using __DataAnalysis/graph_stateanalysis.py
__
3. MAIN MASTER_CONTROL: Decide how to alter power consumption in each load and account for several variables:
		a. Refrigerator: Change temperature on thermostat - Duty Cycle (32.3%), etc.
		b. Water Heater: Change temperature on thermostat - Duty Cycle, etc.
		c. Car Battery?: Turn on/off? - Duty Cycle, etc.
4. Transmit directions to XBees controlling the various aspects of the loads
		a. Use __WirelessCommunication/xbee_transmitter.py__ to transmit the directions from the base XBee to the XBees on the loads
		b. We have not finished the actual controller of the loads - ask Carlo and Andres for more details
