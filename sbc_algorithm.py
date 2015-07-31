'''This is a basic algorithm for the single-board-computer. The actual code is somewhat faulty (unless it says THIS WORKS :) but the ideas are there. I hope.'''
from time import sleep
from datetime import datetime, timedelta, time
from xbee import XBee #from the Python XBee library
import serial
def Party(how_much):
'''***Call this function directly at the end of the main function for it to sleep***
Receives the how_much variable (which can only be 'hard') and sleeps for that duration
Arguments:
	how_much = only value is 'hard' because that's how we roll
'''
	if how_much == 'hard':
		sleep(2)

def getFreq():
'''~~~THIS IS INCOMPLETE~~~
***Call this function directly to get the frequency value***
Returns the frequency from the frequency meter.
No Arguments
'''
	#do some stuff:
	f1=0
	f2=0
	f3=0
	f4=0
	f5=0
	frequency = (f1 + f2 + f3 + f4 +f5)/5
	return frequency

def xbeeReceive(outputfile, METER_ADDRESS):
'''***Call this function directly to add on to the rawdata file and get the last value***
Receives data from the xbee in its raw format and returns the last response (converted into a dictionary).
Arguments:
	outputfile = output file that the program saves the information to (may be unnecessary since the response is returned
	METER_ADDRESS = XBee address so that we can refer to the different XBees and loads
'''

	#Change serial port to COM1,COM2... when running this script on a Windows machine.
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	xbee = XBee(ser)
	response = xbee.wait_read_frame()
	response = dict(response)
	outputfile.append(str(response)+"\n")
	ser.close()
	return response

def stateDetector (rawdata, METER_ADDRESS):
'''***DO NOT call this function directly. It is used in other functions (stateAnalysis)***
Receives the raw data (the last measurement dictionary) and returns whether the load is ON or OFF
Arguments:
	rawdata = the last raw data measurement converted into a dictionary (unless you uncomment the eval part) - you can pass the xbeeReceive function's result into this argument
	METER_ADDRESS = XBee address so that we can refer to the different XBees and loads
'''
#THIS WORKS :)
#rawdata should contain only the last measurement (one dictionary)
	DELTA_OFF = 15
	DELTA_ON  = 30
	#d = eval(rawdata) #raw data is python dictionaries written out as strings, this converts to a dictionary
	if rawdata['source_addr'] == METER_ADDRESS:
		time = rawdata['timestamp']
		samples = [x['adc-4'] for x in rawdata['samples']]
		delta = max(samples) - min(samples)
		if delta < DELTA_OFF:
			last_time_on = time
			return ('OFF', time)
		elif delta > DELTA_ON:
			last_time_off = time
			return ('ON', time)
		else:
		print s, 'UNSURE', ', ', delta
			return ('UNSURE', time)

def stateAnalysis(rawdata, METER_ADDRESS, last_statechange_stateandtime, last_on_time=datetime(2015, 2, 15, 1, 23, 45), amounttime_on = 0, time_state_list=[]):
'''***DO NOT call this function directly. It is used by other functions (do_stateAnalysis)***
Takes in the rawdata and uses stateDetector to return [time_state_list, last_statechange_stateandtime, last_on_time, amounttime_on], which is used by the do_stateAnalysis.
Arguments:
	rawdata, METER_ADDRESS = used for stateDetector
	last_statechange_stateandtime = [ON/OFF, time] for the last time the state changed from ON to OFF or OFF to ON
	last_on_time = last time the state changed from OFF to ON
	amounttime_on = how long the state has been ON
	time_state_list = [last_on_time, amounttime_on, amounttime_cycle]
		last_on_time, amounttime_on = see above
		amounttime_cycle = amount of time the state was OFF and ON (per cycle)
'''
#THIS WORKS :)
#Arguments: rawdata and METER_ADDRESS are for stateDetector, last_statechange_stateandtime and last_on_time and amounttime_on are for stateAnalysis, and time_state_list is optional (exclude for the first time it is run so that the function has some default values but include it every other time)
	last_statechange_time = last_statechange_stateandtime[1]
	if type(last_statechange_time) == str:
		last_statechange_time = datetime.strptime(last_statechange_time, "%Y-%m-%d %H:%M:%S")
	current_state = stateDetector(rawdata, METER_ADDRESS)[0]
        current_time = datetime.strptime(stateDetector(rawdata, METER_ADDRESS)[1], "%Y-%m-%d %H:%M:%S")
	previous_state = last_statechange_stateandtime[0]
	if current_state != previous_state:
                if current_state=='ON':
                        amounttime_cycle = int(float(str((current_time-last_on_time).total_seconds()))) #amount of time in cycle-
                        time_state_list.append((last_on_time,amounttime_on,amounttime_cycle))
			print("time_state_list = " + str(time_state_list))
                        last_statechange_stateandtime = (current_state, current_time)
			last_on_time = current_time			
			amounttime_on = 0
                if current_state=='OFF':
			amounttime_on = int(float(str((current_time-last_statechange_time).total_seconds()))) #amount of time ON in cycle
			last_statechange_stateandtime = (current_state, current_time)
	return [time_state_list, last_statechange_stateandtime, last_on_time, amounttime_on]
#Return: updated time_state_list - so that you can append to it, last_statechange_stateandtime = (state, time), last_on_time - to calculate amount time on, amounttime_on - save it so that you can append it to the time_state_list when current_state == 'ON'

def do_stateAnalysis(rawdata, METER_ADDRESS, last_statechange_stateandtime=('ON','2015-02-15 1:23:45'), last_on_time=datetime(2015, 2, 15, 1, 23, 45), amounttime_on=0, time_state_list=[]): 
'''***Call this function directly - it implements the stateAnalysis function***
Takes in portions of the stateAnalysis function and implements it to return and update the time_state_list for when the state changes. It deletes the first time_state_list and adds values to the list as placeholders. These are deleted later though. You can clean it up if you want but it does work.
Arguments:
	rawdata, METER_ADDRESS = used by stateDetector
	last_statechange_stateandtime, last_on_time, amounttime_on, time_state_list = used by stateAnalysis - these have default values for the first time the time_state_list is appended to since we don't have the information for it. The default values are not used after and the first time_state_list value is deleted.
'''
#THIS WORKS :)
#this starts the stateAnalysis function so that the defaults are used the first time.
	if time_state_list == []:
		stateAnalysis_output = stateAnalysis(rawdata, METER_ADDRESS, last_statechange_stateandtime)
		if len(stateAnalysis_output[0]) > 0: #if time_state_list has an entry		
			time_state_list.append(' ') #keep a placeholder until more data comes
		last_statechange_stateandtime = stateAnalysis_output[1]
		last_on_time = stateAnalysis_output[2]
		amounttime_on = stateAnalysis_output[3]
	else:
		if len(time_state_list) == 2 and time_state_list[0] == ' ':
			time_state_list.pop(0) #remove the placeholder from the list		
		stateAnalysis_output = stateAnalysis(rawdata, METER_ADDRESS, last_statechange_stateandtime, last_on_time, amounttime_on, time_state_list)
		last_statechange_stateandtime = stateAnalysis_output[1]		
		last_on_time = stateAnalysis_output[2]
		amounttime_on = stateAnalysis_output[3]
	return [time_state_list, last_statechange_stateandtime, last_on_time, amounttime_on]

def isRefrigerator_Normal_DutyCycle():
'''***DO NOT call this function directly. It is used in other functions (maintainRefrigerator_DutyCycle)***
Returns whether the refrigerator is on its duty cycle. If true, it is on its normal cycle. If false, it is on its peak duty cycle. This is solely based on time of day (11:00-13:00 = peak duty cycle)
No Arguments
'''
	if time(11,00) <= datetime.now().time() <= time(13,00): #if between 11 am and 1 pm
		return False #not Normal Duty Cycle - peak cycle
	return True

def maintainRefrigerator_DutyCycle(time_state_list):
'''~~~THIS IS INCOMPLETE~~~
***Call this function directly to keep the refrigerator in its normal duty cycle when you don't have to change it.***
Takes in the time_state_list and keeps just the amounttime_on for the last entry in the list. It then determines if the refrigerator should be ON or OFF based on how long it has already been on
Arguments:
	time_state_list = takes from the results of the do_stateAnalysis and access the amounttime_on for the last entry
'''
#feed in the results of state_analysis.py but for the last state change (list of three elements)
	if datetime.now() - strptime(time_state_list[:-1][1], "%Y-%m-%d %H:%M:%S") >= 373 and isRefrigerator_Normal_DutyCycle==True: #if last time off is greater than 373 seconds and it is the normal duty cycle
		#Turn off the refrigerator for 794 seconds	
		pass
	if datetime.now() - strptime(time_state_list[:-1][1], "%Y-%m-%d %H:%M:%S") >= 414 and isRefrigerator_Normal_DutyCycle==False: #if last time off is greater than 414 seconds and it is the peak duty cycle
		#Turn off the refrigerator for 753 seconds
		pass

def getTemp(METER_ADDRESS):
'''~~~THIS IS INCOMPLETE~~~
***DO NOT call this function. It is used in another function (changeTemp).***
Returns the temperature of the load
Arguments:
	METER_ADDRESS = XBee address so that we can refer to the different XBees and loads
'''
#gets the temperature (water heater esp.) Should use the temperature sensor and code that Andres and Carlo made
	#if METER_ADDRESS == water heater METER_ADDRESS:
	#gets the temperature
	#return temperature (Celsius)
	pass

def changeTemp(METER_ADDRESS): #temperature argument is the temperature that the load will be changed to
'''~~~THIS IS INCOMPLETE~~~
***Call this function directly to get and change the temperature.***
Changes the temperature of the load based on the temperature.
Arguments:
	METER_ADDRES = XBee address so that we can refer to the different XBees and loads
'''
	#temperature = getTemp(METER_ADDRESS)
	#if METER_ADDRESS == water heater METER_ADDRESS:
	#change temperature of the water heater to the temperature in the argument
	pass

def main():
	delta = .01 #eh
	caution = .025 #caution needed 
	danger = .05 #you're screwed
	f_nom = 60 #nominal frequency - 60 Hz
	METER_ADDRESS = '\x00\x01'
	rawdata_file = open('rawdata.txt', 'w')
	rawdata_file.close()
	while True:
		with open('Summer2015_mine/DataAnalysis/rawdata.txt"', 'a') as rawdata_file:
			xbeeReceive(rawdata_file)
		rawdata_file = open('Summer2015_mine/DataAnalysis/rawdata.txt', 'r')
		rawdata_file.seek(0,2)
		rawdata = eval(rawdata_file.readline())
		frequency = getFreq()
		if frequency > f_nom + delta: #freq > 60.1
			#advance water heater usage:
			#turn on water heater for 5 min
			#sleep(300)
			pass
		elif frequency < f_nom - delta: #freq < 59.9
			#defer water heater usage
			#lower temperature of water heater --> .1 Hz = 2 degrees Celsius	
			pass
			if frequency < f_nom - caution: #freq < 59.75
				#shed low priority loads
				pass
				if frequency < f_nom - danger:
					#shed medium priority loads
					pass
		if time_state_list == []:
			do_stateAnalysis_output = do_stateAnalysis(d, METER_ADDRESS, last_statechange_stateandtime)
			time_state_list = do_stateAnalysis_output[0]
			last_statechange_stateandtime = do_stateAnalysis_output[1]
			last_on_time = do_stateAnalysis_output[2]
			amounttime_on = do_stateAnalysis_output[3]
		else:
			do_stateAnalysis_output = do_stateAnalysis(d, METER_ADDRESS, last_statechange_stateandtime, last_on_time, amounttime_on, time_state_list)
			last_statechange_stateandtime = do_stateAnalysis_output[1]
			last_on_time = do_stateAnalysis_output[2]
			amounttime_on = do_stateAnalysis_output[3]	
		Party('hard')
main()
''' Extra Info/Notes
minimum time
refrigerator = on/off
	1. Minimum time to be off and on
	JUSTIN HELP:
		how much can we change the duty cycle?
		20 degrees C per Hz - how much on/off
water heater = temperature-based
Refrigerator: 3 min off delay or 5 min enforced off

Might need a getTemp function for water heaters and refrigerators?
Disturbance reserve - 0.1 to 0.5 Hz
59.9 - 59.5 Hz Reconnect at 59.95 
Normal reserve: 59.9 - 60.1 Hz or 59.8 - 60.2 Hz #maybe let's go with the first one
Refrigerator within +- 2 Celsius setpoint change --> how do we do this by an on/off switch?

Water Heater Duty Cycle: (water heater - delay 5 min after turn off and turn on) - turn on only when freq > 60
5 AM - 11 AM: 27%-40%
11 AM - 5 PM: 10%-30%
5 PM - 11 PM: 4%-21%
11 PM - 5 AM: 1%-13%
'''
