'''
Main code for the program for terminal of 80 characters wide and 24 rows high
'''

import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console
import re


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pp3-inventory-management')

console = Console()
warehouse_data = SHEET.worksheet('warehouse')


class CreateStock():
    '''
    Creates object with for new stock
    by taking stock name, serial number, location and location name
    '''

    def __init__(self, s_name, serial, location, loc_name):
        self.s_name = s_name
        self.serial = serial
        self.location = location
        self.loc_name = loc_name


def stock_name_input():
    '''
    Validates the user input for stock name. Only letters,
    numbers and empty spaces allowed, not only empty space on it's own
    '''
    while True:
        console.print('Please enter the name of stock you wish to add',
                      'For example: Clover Station',
                      justify='center', style='cyan')
        stock_name = input()
        pattern = r"^(?!.*\s\s)(?=.*[a-zA-Z0-9])[a-zA-Z0-9\s]*[a-zA-Z0-9]$"
        if re.match(pattern, stock_name) and 4 <= len(stock_name) <= 20:
            return stock_name
        else:
            console.print(
                '''
                Spaces to be entered, but no more than one at a time.
                The input must end with an alphanumeric character.
                The input cannot contain two consecutive space characters.
                The input cannot consist only of space characters.
                The input must be between 4 and 20 characters
                ''', justify='center', style='red'
            )


def stock_serial_input():
    '''
    Validates the user input for serial number. Only letters,
    numbers and dash allowed
    '''
    while True:
        console.print('Please enter the serial number of stock you wish to',
                      'add. For example: SN-1234', justify='center',
                      style='cyan')
        stock_serial = input()
        pattern = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
        if re.match(pattern, stock_serial) and 4 <= len(stock_serial) <= 20:
            return stock_serial
        else:
            console.print(
                '''
                The input can contain alphanumeric values and dash
                The input must be between 4 and 20 characters
                ''', justify='center', style='red'
            )


def stock_location_input():
    '''
    Validates user input for stock location
    '''

    while True:
        console.print('''Please select stock location,
        Press W for warehouse
        Press J for job/site
        Press E to assign to engineer''', justify='center', style='cyan')
        stock_loc_input = input()
        stock_location = ''

        if stock_loc_input.lower() == 'w':
            stock_location = 'warehouse'
            break
        elif stock_loc_input.lower() == 'j':
            stock_location = 'job'
            break
        elif stock_loc_input.lower() == 'e':
            stock_location = 'engineer'
            break
        else:
            console.print(
                'Invalid input. Please select one of the following options',
                justify='center', style='red')

    return stock_location


def stock_loc_name_input(location):
    '''
    Checks the location and asks the user to enter,
    location name based on the result
    '''
    loc_name = ''
    if location == 'warehouse':
        while True:
            console.print('''
            Please Enter:
            G to add to good stock,
            B to add to bad stock''', justify='center', style='cyan')
            loc_name_input = input()
            if loc_name_input.lower() == 'g':
                loc_name = 'good'
                break
            elif loc_name_input.lower() == 'b':
                loc_name = 'bad'
                break
            else:
                console.print('Invalid input. Please select one of the following options',
                              justify='center', style='red')
    elif location == 'job':
        while True:
            console.print(
                'Please enter the name of the site. For example: Circle K')
            loc_name_input = input()
            pattern = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"
            if re.match(pattern, loc_name_input) and 4 <= len(loc_name_input) <= 20:
                loc_name = loc_name_input
                break
            else:
                console.print('''
                The input can contain alphanumeric values and space
                The input must be between 4 and 20 characters
                ''', justify='center', style='red')
    elif location == 'engineer':
        while True:
            console.print(
                'Please enter the name of engineer. For example: John Smyth')
            loc_name_input = input()
            pattern = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"
            if re.match(pattern, loc_name_input) and 4 <= len(loc_name_input) <= 20:
                loc_name = loc_name_input
                break
            else:
                console.print('''
                The input can contain alphanumeric values and space
                The input must be between 4 and 20 characters
                ''', justify='center', style='red')

    return loc_name


def check_database():
    '''
    Calls the input validating functions and then checks if the serial number,
    exist in the system
    '''
    stock_name_input()
    stock_serial_input()
    location_input = stock_location_input()
    stock_loc_name_input(location_input)


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print('PRESS C TO ADD STOCK, PRESS V TO VIEW STOCK, PRESS S',
                      'TO SEARCH OR Q TO QUIT\n', justify='center', style='cyan')
        user_input = input()
        if user_input.lower() == 'c':
            check_database()
        elif user_input.lower() == 'v':
            pass
        elif user_input.lower() == 's':
            pass
        elif user_input.lower() == 'q':
            quit()
        else:
            console.print('Invalid input. Please select one of the available ',
                          'options (C,V,S,Q)', justify='center', style='red')


main_menu()
