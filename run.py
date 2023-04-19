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
    numbers, dashes and empty spaces allowed, not only empty space on it's own
    '''
    while True:
        console.print('Please enter the name of stock you wish to add',
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
                ''', justify='center', style='red'
            )


def check_database():
    '''
    Calls the input validating functions and then checks if the serial number,
    exist in the system
    '''
    pass


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print('PRESS C TO ADD STOCK, PRESS V TO VIEW STOCK, PRESS S',
                      'TO SEARCH OR Q TO QUIT\n', justify='center', style='cyan')
        user_input = input()
        if user_input.lower() == 'c':
            pass
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
