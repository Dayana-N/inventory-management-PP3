'''
Main code for the program for terminal of 80 characters wide and 24 rows high
'''
import re
import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console
from rich.table import Table


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
job_data = SHEET.worksheet('job')
engineer_data = SHEET.worksheet('engineer')


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
    stock_serial = ''
    while True:
        console.print('Please enter the serial number of stock you wish to',
                      'add. For example: SN-1234', justify='center',
                      style='cyan')
        serial_input = input()
        pattern = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
        if re.match(pattern, serial_input) and 4 <= len(serial_input) <= 20:
            stock_serial = serial_input
            break
        else:
            console.print(
                '''
                The input can contain alphanumeric values and dash
                The input must be between 4 and 20 characters
                ''', justify='center', style='red'
            )

    return stock_serial


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
                'Please enter the name of the site. For example: Circle K',
                justify='center', style='cyan')
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


def stock_input():
    '''
    Calls the input validating functions,
    creates an object and adds it to spreadsheet
    '''
    stock_name = stock_name_input()
    stock_serial = stock_serial_input()
    stock_location = stock_location_input()
    location_name = stock_loc_name_input(stock_location)
    return stock_name, stock_serial, stock_location, location_name


def add_stock(entry):
    '''
    Check if the serial number exist on the system,
    if not adds it to spreadsheet and handles potential errors
    '''
    serial_num = entry.serial
    find_serial = None
    try:
        for worksheet in SHEET.worksheets():
            find_serial = worksheet.find(serial_num)
            break
    except gspread.exceptions.WorksheetNotFound:
        console.print('Worksheet not found. Please try again.',
                      justify='center', style='red')
        main_menu()

    if find_serial is not None:
        try:
            current_sheet = SHEET.worksheet(entry.location)
            current_sheet.append_row([entry.s_name, entry.serial,
                                      entry.location, entry.loc_name])
            console.print(entry.s_name, entry.serial, entry.location,
                          entry.loc_name, 'added successfully.',
                          justify='center', style='green')
        except gspread.exceptions.WorksheetNotFound:
            console.print('Worksheet not found. Please try again.',
                          justify='center', style='red')
            main_menu()
        except gspread.exceptions.APIError:
            console.print('An Error occurred. Please try again.',
                          justify='center', style='red')
            main_menu()
    else:
        console.print('This serial number already exist on the system',
                      justify='center', style='red')


def view_stock():
    '''
    Displays the stock in a table format
    '''
    index = 0
    table = Table(title='List of all stock')
    table.add_column('№', justify='left', style='cyan')
    table.add_column('Item Name', justify='left', style='cyan')
    table.add_column('Serial No', justify='left', style='cyan')
    table.add_column('Location', justify='left', style='cyan')
    table.add_column('Name', justify='left', style='cyan')

    for worksheet in SHEET.worksheets():
        worksheet_data = worksheet.get_all_values()
        for row in worksheet_data[1:]:
            index += 1
            table.add_row(str(index), *row)

    console.print(table, justify='center')


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print('PRESS C TO ADD STOCK, PRESS V TO VIEW STOCK, PRESS S',
                      'TO SEARCH OR Q TO QUIT\n', justify='center', style='cyan')
        user_input = input()
        if user_input.lower() == 'c':
            user_input = stock_input()
            entry = CreateStock(*user_input)

            add_stock(entry)
        elif user_input.lower() == 'v':
            view_stock()
        elif user_input.lower() == 's':
            pass
        elif user_input.lower() == 'q':
            quit()
        else:
            console.print('Invalid input. Please select one of the available ',
                          'options (C,V,S,Q)', justify='center', style='red')


main_menu()
