'''
This program takes the output from the state_analysis.py file and creates a graph of all 5 days with several different colors.
'''
import matplotlib.pyplot as plt
datafile = open('state_analysis.txt', 'r')
data_list = eval(datafile.readline())
x_numbers = []
x_date = []
y_timeon = []
y_timecycle = []
for tup in data_list:
	x_date.append(tup[0])
	y_timeon.append(tup[1])
	y_timecycle.append(tup[2])
y_dutycycle = []
sum_dutycycle = 0
i = 0
while i<len(y_timeon):
	y_dutycycle.append(float(y_timeon[i])/float(y_timecycle[i]))
	sum_dutycycle+=y_dutycycle[i]
	i+=1
print "The average duty cycle is " + str(sum_dutycycle/(i+1))
n = 0
for element in x_date:
	x_numbers.append(n)
	n+=1
''''''
''''''
#Day 1: [0:38]          38
#Day 2: [38:114]        76
#Day 3: [114:189]       75
#Day 4: [189:263]       74
#Day 5: [263:294]       31

xdate = []
ticklist = []
plt.xlabel('Date', fontsize=15)
i = 1
while i<15:
	xdate.append(x_date[20*i])
	ticklist.append(20*i)
	i+=1
plt.xticks(ticklist, xdate)
plt.suptitle('4-Day Refrigerator  Duty Cycle Graph', fontsize = 20)
plt.scatter(x_numbers[0:38], y_dutycycle[0:38], c = 'b')
plt.scatter(x_numbers[38:114], y_dutycycle[38:114], c = 'g')
plt.scatter(x_numbers[114:189], y_dutycycle[114:189], c = 'r')
plt.scatter(x_numbers[189:263], y_dutycycle[189:263], c = 'c')
plt.scatter(x_numbers[263:294], y_dutycycle[263:294], c = 'm')
plt.show()

