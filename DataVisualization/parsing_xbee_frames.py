import json
readings = open("original_frequency_output.txt", 'r')
stringReadings = readings.read()
print type(stringReadings)
listReadings = stringReadings.split('}')
print len(listReadings)
for reading in listReadings:
    reading = json.loads(reading)
print reading
