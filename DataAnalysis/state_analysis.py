import csv
import datetime
datafile = open('fridgestate2.csv', 'r')
reader = csv.reader(datafile)
time_state_list = []
amounttime_on = str(0)
previous_state = 'OFF'
previous_statechange_time = datetime.datetime.strptime(reader.next()[0], "%Y-%m-%d %H:%M:%S")
for line in reader:
	current_state = line[1].strip()
	current_time = datetime.datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
	if current_state != previous_state:
                if current_state=='ON':
                        amounttime_cycle = int(float(str((current_time-previous_statechange_time).total_seconds()))) #amount of time in cycle
                        time_state_list.append((str(previous_statechange_time),amounttime_on,amounttime_cycle))
                        previous_statechange_time = current_time
                if current_state=='OFF':
                        amounttime_on = int(float(str((current_time-previous_statechange_time).total_seconds()))) #amount of time ON in cycle
	previous_state = current_state
time_state_list.pop(0) #remove the first entry
print time_state_list
'''sum_amounttime_on = 0
sum_amounttime_cycle = 0
n = 0
for tup in time_state_list:
	sum_amounttime_on += tup[1]
	sum_amounttime_cycle += tup[2]
	n +=1
print "Average time on is " + str(sum_amounttime_on/n)
print "Average time per cycle is " + str(sum_amounttime_cycle/n)'''
datafile.close()
