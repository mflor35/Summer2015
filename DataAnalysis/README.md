Data Analysis of 
Basics on how to use this file:
## Files to use:
 1. state_detector.py = takes in rawdata2.txt (not given - use any raw data) and returns whether the load is on or off based on amplitude of the current wave. The file prints the data and so needs to be redirected into the file fridgestate2.csv. Output is in the form of timestamp, ON/OFF, delta (max-min)
 2. state_analysis.py = takes in fridgestate2.csv and returns only the times where the state changes from ON to OFF or OFF to ON. The file prints the data and so needs to be redirected into the file state_analysis.txt. Output is in the form of [timestamp of state change, amount of time ON in cycle, amount of time between ON cycles]. The averages of the second and third part of the list (which is commented out) can be divided to give the duty cycle as a decimal.
 3. graph_state_analysis.py = takes in state_analysis.txt file and graphs the data. This is specifically for the data collected from 07/16/2015 to 07/21/2015 but can be modified for future graphs. 

## Extra information/files:
__graph_data.py__ takes in rawdata.txt (can be replaced with any raw data file) and normalizes the voltage and current data based on the method used at https://learn.adafruit.com/tweet-a-watt/design-listen (link given in file as well) and graphs the result.

__graph_frequency_voltage.py__ takes in frequency and voltage data and graphs it. This is a preliminary code experimenting with graphing with time. It will not be used for its code but can be helpful in dealing with time for graphs

__graphing_data_visualization.py__ = takes in sunlight, power, and energy information to create several graphs. This also was designed as an experiment with graphing and though will not be used as a program for the project, it contains useful code that helps in graphing (especially formatting).

