import math

#frequency = 59

def frange(start,end,step):
    while(start < end):
        yield start
        start += step

max_voltage = 100

frequency = float(raw_input("Enter value of frequency(in Hz)"))
number_of_samples = 250
delta_time = 1.0 / (24.0*60.0)

n = 0
voltage = []
Times = []
for time in frange(delta_time,number_of_samples*delta_time,delta_time):
    voltage.append(max_voltage * math.sin(2 * math.pi * frequency * time) + max_voltage * math.sin(6 * math.pi * frequency * time))
    Times.append(time)
# Finding zero crossoings
print "Generated volatages"
for v in voltage:
    print v
zero_crossings = []
for j in range(number_of_samples):
    x  = voltage[j] * voltage[j-1]
    if(x < 0):
        zero_crossings.append(j)
i = zero_crossings[0]
a = abs((voltage[i] * delta_time) / (voltage[i] - voltage[i - 1])) #Correction Factor 1

i = zero_crossings[1]
b = abs((voltage[i - 1] * delta_time) / (voltage[i] - voltage[i - 1]))

p = zero_crossings[1] - zero_crossings[0]

f1 = 1 / (2 * ((p - 1) * delta_time + a + b))
print("This feq is calculated using only one half cycle. " + str(f1))

# Second part of the sub-algorithm
alpha = 0
beta = 0
for j in range(1,6):
    i = zero_crossings[j]
    a = abs((voltage[i] * delta_time) / (voltage[i] - voltage[i - 1]))
    beta = beta + b

p = zero_crossings[6] - zero_crossings[0] # This is the number of samples between 6 zero crossings
T2 = ((p - 6) * delta_time) + alpha + beta # Interval between 6 zero cross overs
f2 = 3 / T2
print "This is the frequency calculted using six half cycles",str(f2)

i = zero_crossings[0]
a  = abs((voltage[i] * delta_time) / (voltage[i] - voltage[i - 1])) #correction factor 1
i = zero_crossings[6]
b = abs((voltage[i-1]* delta_time) / (voltage[i] - voltage[i - 1]))

p = zero_crossings[6] - zero_crossings[0]
f3 =  3 / ((p - 1) * delta_time + a + b);

print "This is an alternative way of calculating frequency using six half cycles", f3

if abs(f2 - f1) < 0.01:
    f0 = f2
else:
    f0 = f1

print "After checking with the criterion, we get the frequency to be", f0

i = int(raw_input("Enter at wich sample you want to the frequency to be calculated by second algo"))
Fr = []
for j in range(4):
    if(voltage[i - 1] == 0):
        i = i - 1

    omega_delta_t = math.acos(abs((voltage[i] + voltage[i - 2]) / (2 * voltage[i - 1])))
    Fr.append(omega_delta_t / (2 * math.pi * delta_time))
    print str(Fr[j])
    i = i - 1

print "The frequency using the second sub algorithm is: ", Fr[0]
