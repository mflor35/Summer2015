import ast
import matplotlib.pyplot as plt
data = open('frequency_output.txt')
voltage = []
current = []
number_samples = []

line = ast.literal_eval(data.readline())
"""
for sample in line['samples']:
    voltage.append(sample['adc-0'])
    current.append(sample['adc-4'])
"""
x = 0
for line in data:
    line = line.strip()
    try:
        line = ast.literal_eval(line)
        for sample in line['samples']:
            voltage.append(sample['adc-0'])
            current.append(sample['adc-4'])
            x += 1
            number_samples.append(x)
    except:
        pass

plt.ylabel("current",fontsize=14)
plt.scatter(number_samples,current)
plt.show()
