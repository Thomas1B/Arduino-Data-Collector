# Arduino Data Collector
Python program to connect to an arduino, read in data and save it to a CSV File.

This program uses **pandas** and **progressbar2** libaries.
- pandas: https://pandas.pydata.org/
- progressbar2: https://pypi.org/project/progressbar2/

DataFrame are set up as columns.

## Program Requirements
This program expects the first line of data to be the column headers.<br>
Example from arduino: `Serial.print("Time Temperature Pressure")`

Data is printed from the arduino as such:
```c
Serial.print(time)
Serial.print(" ")
Serial.print(temperature)
Serial.print(" ")
Serial.print(pressure)
Serial.println()
```

## Program Parameters
```
'''
Program Parameters:
    port: port arduino is connected to.
    baudrate: baudrate that arduino is set to.
    num_of_samples: number of samples to be taken.
'''

port = 'COM5'
baudrate = 9600
num_of_samples = 50
```
<hr>

### To run program: 
```Bash
python Arduino-Data-Collector.py
```