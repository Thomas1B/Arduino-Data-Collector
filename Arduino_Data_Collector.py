'''
Python program to connect to an arduino, read in data and save it to a CSV File.
DataFrame are set up as columns.

This program expects the first line of data to be the column headers.
Example from arduino: Serial.print("Time Temperature Pressure")

'''

import serial
import pandas as pd
import progressbar
import os


def main() -> None:
    '''
    Main Function to run the program
    '''

    text = 'Welcome to the Arduino Serial Reader!\n'
    text += 'Note: Data is saved as a csv file.\n'
    print(text)

    ser, num_of_samples, headers = get_collection_params()

    # asking user if they want to print data as it's collected.
    text = 'Would you like to print the data as it is collected?\n'
    text += '1 - Yes, 2 - No: '
    print_sample = None
    while True:
        print_sample = input(text)
        if print_sample == '1':
            print_sample = True
            break
        elif print_sample == '2':
            print_sample = False
            break

    # getting saving parameters
    save_name = get_saving_params()
    print()  # for spacing

    while True:
        start = input("Press Enter to start or another key to quit: ")

        if start == '':
            if print_sample:
                print('---> starting...\n')
            break
        else:
            exit()

    print()
    data = collect_data(num_of_samples,
                        ser=ser,
                        print_sample=print_sample,
                        headers=headers
                        )

    # Saving data
    try:
        data.to_csv(save_name, index=False)
    except Exception as err:
        print("Error occurred while saving.")
        if err:
            print("\nError:")
            print(err, '\n')
        exit()
    print(f'\nSaved as "{save_name}".\n')


def get_collection_params() -> tuple:
    '''
    Function to get the parameters for collecting data.

        Returns: 
            (port, baudrate, num_of_samples, header)

    '''
    user_print = '---> {}\n'  # string to print

    port, baudrate, num_of_samples = None, None, None
    ser = None

    # getting the port from user
    while True:
        port = input("Enter the port: ")
        if port:
            break
        else:
            text = 'You must enter a port!\n'
            print(text)
    print(user_print.format(port))

    # getting baudrate from user
    while True:
        baudrate = input("Enter the baudrate, (default 9600): ")

        if baudrate.isdigit():
            baudrate = int(baudrate)
            break
        elif baudrate == '':
            baudrate = 9600
            break
        else:
            text = 'Baudrate must be a integer!\n'
            print(text)
    print(user_print.format(baudrate))

    print('Connecting to the Arduino ', end='')
    try:
        # try block for connecting to arduino.
        ser = serial.Serial(port, baudrate)
        print('was successful!\n')
    except serial.SerialException:
        print("failed! Device cannot be found, make sure you selected the correct port.\n")
        quit()

    # getting number of samples from user
    while True:
        num_of_samples = input(
            "Enter the number of sample to collect (default 100): ")

        if num_of_samples.isdigit():
            num_of_samples = int(num_of_samples)
            break
        elif num_of_samples == '':
            num_of_samples = 100
            break
        else:
            text = 'Number of samples must be an integer.\n'
            print(text)
    print(user_print.format(num_of_samples))

    # asking user if headers are printed from the arduino
    header = input("Are headers printed from the arduino? (deflaut yes): ")
    if header:
        header = True
    elif header in ['n', 'no']:
        header = False
    else:
        header = True
        print(user_print.format('yes'))

    return ser, num_of_samples, header


def get_saving_params() -> str:
    '''
    Function to get parameters for saving the data to a csv file.

        Returns:
            filepath for saving the csv file.
    '''

    text = '\nData is saved as CSV file automatically.'
    print(text)

    # Asking user for filename for saving.
    text = 'Enter a filename for the data file, or leave blank for the default name: '
    user = input(text)
    if user:
        if '.csv' in user:
            user = user.strip('.csv')
    else:
        print('\t-> using default filename.\n')
        user = 'default'
    path = f'{user}.csv'

    # asking user if they want to overwrite the file, (only if custom name is given and path already exists).
    overwrite = False
    if os.path.exists(path) and user != 'default':
        text = 'That filename is already used. Would you like to overwrite? (y/n): '
        overwrite = input(text)
        if overwrite.lower() in ['y' or 'yes']:
            overwrite = True
        else:
            overwrite = False

    if not overwrite:
        # used for default and custom names.
        try:
            # if the filename exists already, modifying it
            if os.path.exists(path):
                name, ext = os.path.splitext(path)
                count = 1
                while os.path.exists(path):
                    path = f'{name} ({count}){ext}'
                    count += 1
                print(f'Data will be saved as "{path}"')
        except:
            pass

    return path


def collect_data(num_of_samples: int, ser, print_sample=False, headers=True) -> pd.DataFrame:
    '''
    Function to read in data from the arduino.

        Parameters:
            num_of_samples: number of samples to take.
            ser: Serial object.
            print_sample: print sample as collected.

        Returns:
            DataFrame, with each kind of data as a column, (Ex: time, voltage, temperature, etc)

    '''
    data = None     # temporary data. DO NOT DELETE

    # if statement for styling prints
    if print_sample:
        print("\nData collection started\n")

    # showing a progess bar
    bar = None
    if not print_sample:
        widgets = [progressbar.Timer(format='Runtime: %(elapsed)s'), ' | ',
                   progressbar.Percentage(), ' | ',
                   progressbar.Counter(
                       format='Sample {}/{:0d}'.format('%(value)d', num_of_samples)), ' ',
                   progressbar.GranularBar(),
                   ' ', progressbar.CurrentTime(), ' '
                   ]
        bar = progressbar.ProgressBar(max_value=num_of_samples,
                                      widgets=widgets).start()

    # declaring column headers for dataframe
    data_in = ser.readline().decode().strip()
    if headers:
        column_names = data_in.split()
    else:
        column_names = [
            f'Col {i}' for i in range(len(data_in.split()))]
        data = pd.DataFrame(columns=column_names)
        if print_sample:
            print(', '.join(column_names))

    # loop to collect data
    for count in range(1, num_of_samples+1):
        # num_of_samples + 1 to account for reading column names.

        # reading data line
        line = read_data(ser=ser, column_names=column_names)

        # adding line to dataframe
        data = pd.concat([data, line], ignore_index=True)

        if print_sample:
            text = ', '.join(
                pd.Series(line.values[0]).to_numpy().astype(str)
            )
            print(text)
        else:
            bar.update(count)

    if print_sample:
        print("\nData collection finished\n")

    return data


def read_data(ser: serial.Serial, column_names: list = []) -> pd.DataFrame:
    '''
    Function to read one line of data from the arduino.

        Parameters:
            ser: Serial object.
            column_names: (optional) names for each column

        Returns:
            DataFrame
    '''

    # reading a sample then decoding and stripping
    data_in = ser.readline().decode().strip()

    # converting a sample into floats and create a dataframe.
    data = pd.DataFrame(data_in.split(), dtype=float).T
    if column_names:
        data.columns = column_names

    return data


if __name__ == "__main__":

    main()
