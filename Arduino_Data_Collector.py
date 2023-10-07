'''
Python Script to print the serial output of an Arduino
'''

import serial
import pandas as pd
import os


port = 'COM3'
baudrate = 9600

save_folder_path = os.path.expanduser("~") + "/Downloads/"


default_sample_count = 10

# *********** Variables ***********

headers = None
dataframe = None

delimiters = [';', '|', ':', ',']


def test_connection(port: str, baudrate: int) -> serial.Serial:
    '''
    Function to test the connection to the microcontroller (MCU).

    Parameters:
        port: port to connect to MCU (str).
        baudrate: baudrate of MCU (int).

    Returns:
        Serial object
    '''

    # baudrate = int(baudrate)
    try:
        ser = serial.Serial(port=port, baudrate=baudrate)
    except serial.SerialException as err:
        err = str(err).split(':')[0]
        print(f"Error: {err}, check the port and/or baudrate!\n")
        exit(1)

    return ser


def get_collection_params() -> tuple:
    '''
    Function to get the user parameters for collecting data.

        Parameters:
            None

        Returns tuple of:
            headers_printed: bool, does MCU print headers.
            max_count: int, how many samples to collect.
            path: str, path to save data as.
    '''

    # Asking user if column headers are printed from controller:
    text = 'Are the column headers printed from the controller? (Default - yes).'
    text += '\nIf they are not, default headers will be generated: '
    user = input(text).lower()
    if user in ['yes', 'y', '']:
        headers_printed = True
    print()

    # Asking user how many data samples to collect:
    while True:
        text = f'How samples to collect? (default {default_sample_count}): '
        try:
            # checking if user enter an integer.
            user = input(text)
            if user == '':
                user = default_sample_count
            max_count = int(user)
            break
        except ValueError:
            print('You must enter an integer, try again.\n')

    # Asking user for a filename to save data as:
    print("\nData is saved as a CSV file only.")
    filename = input('Enter a filename to save the data: ')
    if not filename:
        filename = 'Arduino_data'
    path = os.path.join(save_folder_path, f'{filename}.csv')

    return headers_printed, max_count, path


def main():
    count = 0  # data collected count
    headers_printed, max_count, path = get_collection_params()
    print()
    ser = test_connection(port=port, baudrate=baudrate)

    try:
        '''
        Try block to read MCU's Serial output

        execptions:
            serial.SerialException: issues connect to MCU.
            KeyboardInterrupt: uses clicks ctrl-c.

        '''

        while count < max_count + 1:

            # reading data from the MCU.
            raw_data = ser.readline().decode().strip()

            # Changing delimiters and splitting data into columns.
            for delimiter in delimiters:
                raw_data = raw_data.replace(delimiter, ' ')
            raw_data = raw_data.split()

            print(f'Count {count:>3}/{max_count}: {raw_data}')

            if count == 0:
                if headers_printed:
                    headers = raw_data
                else:
                    headers = [f'Col{num}' for num in range(len(raw_data))]
                dataframe = pd.DataFrame(columns=headers)
                count = 1
            else:
                tmp_data = pd.DataFrame(raw_data).T
                tmp_data.columns = headers
                dataframe = pd.concat(
                    [dataframe, tmp_data],
                    ignore_index=True
                )
                count += 1

    except serial.SerialException:
        print('-> Arduino was disconnected.')

    except KeyboardInterrupt:  # user interrupt process.
        ser.close()
        print("-> User stopped Program.")

    # showing sample of data collected.
    print("\nSample of collected data:\n")
    print(dataframe.head())

    # getting user info to save file
    print(f'\nData saved as "{path}"\n')
    dataframe.to_csv(path, index=False)


if __name__ == "__main__":

    main()
