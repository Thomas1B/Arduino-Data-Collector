'''
Python program to connect to an arduino, read in data and save it to a CSV File.
DataFrame are set up as columns.

'''

from Program_Files.Arduino_Data_Collector import main

if __name__ == "__main__":

    '''
    Program Parameters:
        port: port arduino is connected to.
        baudrate: baudrate that arduino is set to.
        num_of_samples: number of samples to be taken.

    '''

    port = 'COM3'
    baudrate = 9600
    num_of_samples = 100

    main(port, baudrate, num_of_samples)
