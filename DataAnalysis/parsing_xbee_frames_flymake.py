import json
readings = file("original_frequency_output.txt")
listReadings = []
for line in readings:
    tempreading = ""
    for char in line:
        if char != '}':
            tempreading += char
        else:
            tempreading += '}'
            listReadings.append(tempreading)
            tempreading = ""

for reading in listReadings:
    reading = json.loads(reading)
