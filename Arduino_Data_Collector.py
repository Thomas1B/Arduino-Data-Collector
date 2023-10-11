'''
Python Script to print the serial output of an Arduino
'''

import serial
import serial.tools.list_ports
import pandas as pd
import os
import time


PORT = None
BAUDRATE = None

save_folder_path = os.path.expanduser("~") + "/Downloads/"


default_sample_count = 20

# *********** Variables ***********

delimiters = [';', '|', ':', ',']

# *********** Function ***********


def get_available_ports() -> list[str]:
    '''
    Function to show all available serial ports

        Parameters:
            None

        Returns:
            List of available serial ports.
    '''

    # Get a list of all available serial ports
    available_ports = serial.tools.list_ports.comports()

    available_ports = [port.device for port in available_ports]

    return available_ports


def get_port_and_baudrate(ports: list) -> tuple[str, int]:
    '''
    Function to show user available ports, get user response and baudrate.

        Parameters:
            ports: list of available serial ports

        Returns:
            port (str): port controller is connected to.
            baudrate (int): baudrate controller is using.

    '''
    port = None
    baudrate = None

    # making a string to show optins
    options = 'Available Serial Ports:\n'
    options += '\n'.join(
        [f'-> {i:>2}: {port}' for i, port in enumerate(ports, 1)]
    )
    options += f'\n-> {"q":>2}: Quit Program\nWhich port would you like to connect: '

    # loop to make user enters an appropriate input when picking a serial port
    while True:
        user = input(options).lower()
        if user in ['q', 'quit']:
            exit("User quit program.")
        else:
            try:
                user = int(user)
                if user > 0 and user < len(ports)+1:
                    port = ports[user-1]
                    break
                else:
                    print("That option is not available, try again.\n")

            except Exception as err:
                print(f"You must enter an integer, try again.\n")

    # loop to make user enters an appropriate input when entering a baudrate
    while True:
        user = input("Enter the baudrate (default 9600): ")
        if user == '':
            baudrate = 9600
            break
        else:
            try:
                baudrate = int(user)
            except Exception:
                print('Baudrate must be an integer, try again.\n')

    return port, baudrate


def test_connection(port: str, baudrate: int, close=True) -> serial.Serial:
    '''
    Function to test the connection to the controller (MCU).

        Parameters:
            port (str): port MCU is connected to.
            baudrate (int): baudrate MCU is using.
            close (bool: default True): close connection to MCU after test.

        Returns:
            Serial object of MCU.
    '''

    text = f'\nTesting connection to port "{port}" with baudrate of {baudrate}: '
    print(text, end='')

    # try block to test connection to MCU
    try:
        ser = serial.Serial(port=port, baudrate=baudrate)
        print("Connection Succesful!\n")
        if close:
            ser.close()

    except serial.SerialException as err:
        err = str(err).split(':')[0]
        print("Connection Failed!")
        exit(f"Error: {err}, check the port and/or baudrate!\n")

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
    print("Getting Collection Parameters:")

    # Asking user if column headers are printed from controller:
    text = 'Are the column headers printed from the controller? (y/n).'
    text += '\nIf they are not, default headers will be generated: '
    user = input(text).lower()

    headers_printed = False
    if user in ['yes', 'y',]:
        headers_printed = True
    print()

    # Asking user how many data samples to collect:
    while True:
        text = f'How samples to collect? (default {default_sample_count}): '
        try:
            # checking if user entered an integer.
            user = input(text)
            if user == '':
                user = default_sample_count
            max_count = int(user)
            break
        except ValueError:
            print('You must enter an integer, try again.\n')

    # Asking user for a filename to save data as:
    print("\nGetting Saving Information:")
    print("Data is saved as a CSV file only into the systems downloads folder.")
    text = 'Enter a filename to save the data or "skip" not to save, leaving blank will default to "Arduino_data (#).csv".'
    print(text)

    filename = input('User: ')
    if filename == "":
        filename = 'Arduino_data'
        print('-> Using default naming scheme.')
    elif '.csv' in filename:
        filename = filename.split('.')[0]

    if filename.lower() == 'skip':
        path = None
    else:
        path = os.path.join(save_folder_path, f'{filename}.csv')

        # loop to check if filename already exists, if so modify the name
        base, ext = os.path.splitext(path)
        count = 1
        while os.path.exists(path):
            path = f'{base} ({count}){ext}'
            count += 1

    return headers_printed, max_count, path


def save_data(data: pd.DataFrame, path: str):
    '''
    Function to save the collected data

        Parameters:
            data: dataframe of collected data
            path: path to save the data.

        Returns:
            none
    '''
    if path:  # User wants to save data.
        data.to_csv(path, index=False, sep=' ')
        print(f'Data saved as "{path}".')

    else:  # User skipped data saving.
        print('\nSaving data was skipped.')


def format_runtime(runtime: float):
    '''
    Function to convert the runtime into a string.

        Parameters:
            runtime (float): runtime of program in seconds.

        return:
            str hours:minutes:seconds:milliseconds.
    '''

    # divmod example: 3, 2 = divmod(17, 5)

    # calculating hours, minutes, and seconds.
    minutes, seconds = divmod(runtime, 60)
    hours, minutes = divmod(minutes, 60)
    millis = (runtime - int(runtime)) * 1000

    millis = round(millis)

    # making string.
    text = f'{int(hours)}:{int(minutes)}:{int(seconds)}:{millis}'
    return text


# *********** Main Program ***********


def main():

    triggerd = None

    if not PORT and not BAUDRATE:
        available_ports = get_available_ports()
        port, baudrate = get_port_and_baudrate(available_ports)
    else:
        port = PORT
        baudrate = BAUDRATE

    ser = test_connection(port=port, baudrate=baudrate, close=True)
    headers_printed, max_count, path = get_collection_params()

    ser.open()

    # try-block to collect data
    count = 0  # data collected count

    try:
        '''
        Try block to read MCU's Serial output

        execptions:
            serial.SerialException: issues connect to MCU.
            KeyboardInterrupt: uses clicks ctrl-c.

        '''

        # collecting data
        print('\nStarting Data Collection:')
        start_time = time.time()
        while count < max_count + 1:

            # reading data from the MCU.
            raw_data = ser.readline().decode().strip()

            # Changing delimiters
            for delimiter in delimiters:
                raw_data = raw_data.replace(delimiter, ' ')
            raw_data = raw_data.split()  # splitting data

            # print statement to show data as it collected.
            if max_count >= 1000:
                print(f'Count {count:>3}/{max_count}: {raw_data}')
            else:
                print(f'Count {count:>2}/{max_count}: {raw_data}')

            # Adding data to dataframe:
            if count == 0:
                # checking if headers are included in data
                if headers_printed:
                    headers = raw_data
                else:
                    # creating default headers
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
        triggerd = '-> Arduino was disconnected.'

    except KeyboardInterrupt:  # user interrupt process.
        ser.close()
        triggerd = "-> User stopped Program."

    runtime = time.time() - start_time
    runtime = format_runtime(runtime)

    # showing sample of data collected.
    print("\nSample of collected data:")
    print(dataframe.head())

    save_data(data=dataframe, path=path)

    print("\nCollection Parameters:")
    if triggerd:
        print(f'Job Status: {triggerd}')
    else:
        print(f'Job Status: Succesful.')
    text = f'Serial Port: {port}, Baudrate: {baudrate}.\n'
    text += f'Sample Count: {count-1}/{max_count}, Runtime: {runtime}\n'
    text += f'Saved Filename: "{os.path.split(path)[-1]}"\n'
    print(text)


if __name__ == "__main__":

    main()
