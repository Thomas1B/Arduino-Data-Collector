'''
Python Script to print serial outputs from an arduino
'''

import serial
import serial.tools.list_ports
import pandas as pd
import os

# This variables can be set to skip the menu.
PORT = None
BAUDRATE = None


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
            print('-> using default.')
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
        print("Connection Succesful!")
        if close:
            ser.close()

    except serial.SerialException as err:
        err = str(err).split(':')[0]
        print("Connection Failed!")
        exit(f"Error: {err}, check the port and/or baudrate!\n")

    return ser


def get_serial_output(ser: serial.Serial) -> str:
    '''
    Function to get the serial output of the controller.

        Parameters:
            ser: Serial object of controller

        Returns:
            str
    '''

    return ser.readline().decode().strip()


def main():
    '''
    Main Function
    '''

    # checking if manual override is set
    if not PORT and not BAUDRATE:
        available_ports = get_available_ports()
        port, baudrate = get_port_and_baudrate(available_ports)
    else:
        port = PORT
        baudrate = BAUDRATE

    # testing connection with given port and baudrate
    ser = test_connection(port, baudrate)

    # Starting Serial outputs
    print('Starting Serial Prints:\n')
    ser.open()
    while (True):
        try:
            # getting
            output = get_serial_output(ser)
            print(output)

        except serial.SerialException:
            exit('\nMicrocontroller was disconnected.')

        except KeyboardInterrupt:
            exit('\nUser force quit Program.')


if __name__ == '__main__':
    main()
