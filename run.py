'''
Main code for the program for terminal of 80 characters wide and 24 rows high
'''

import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console


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


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print('PRESS C TO ADD STOCK, PRESS V TO VIEW STOCK, PRESS S',
                      'TO SEARCH OR Q TO QUIT', justify='center', style='cyan')
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
