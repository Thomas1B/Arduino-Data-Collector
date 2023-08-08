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

<hr>

### To run program: 
```Bash
python Arduino_Data_Collector.py
```