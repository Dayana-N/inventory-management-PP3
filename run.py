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

    return stock_serial.upper()


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
                console.print('Invalid input. Please select one of the',
                              'following options', justify='center',
                              style='red')
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
    except gspread.exceptions.WorksheetNotFound:
        console.print('Worksheet not found. Please try again.',
                      justify='center', style='red')
        main_menu()

    if find_serial is None:
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


def view_stock_menu():
    '''
    Asks the user if they would like to see all stock,
    engineer stock, warehouse or stock on site
    '''
    console.print('''Please press
    A to view all stock
    W to view warehouse stock
    J to view job/site stock
    E to view engineer stock
    Q to go back to main menu''', justify='center', style='cyan')
    user_input = input()

    while True:
        if user_input.lower() == 'a':
            view_stock()
            break
        elif user_input.lower() == 'w':
            view_stock('warehouse')
            break
        elif user_input.lower() == 'j':
            view_stock('job')
            break
        elif user_input.lower() == 'e':
            view_stock('engineer')
            break
        elif user_input.lower() == 'q':
            main_menu()
        else:
            console.print('Invalid input. Please try again',
                          justify='center', style='red')

    while True:
        console.print('Press B to go back or Q to quit',
                      justify='center', style='cyan')
        user_input = input()
        if user_input.lower() == 'b':
            view_stock_menu()
            break
        elif user_input.lower() == 'q':
            main_menu()
        else:
            console.print('Invalid input. Please try again',
                          justify='center', style='red')


def view_stock(worksheet_name=None):
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

    if worksheet_name is not None:
        try:
            current_worksheet = SHEET.worksheet(worksheet_name)
            worksheet_data = current_worksheet.get_all_values()
            for row in worksheet_data[1:]:
                index += 1
                table.add_row(str(index), *row)
        except gspread.exceptions.WorksheetNotFound:
            console.print('Worksheet not found. Please try again.',
                          justify='center', style='red')
            main_menu()
        except gspread.exceptions.APIError:
            console.print('An Error occurred. Please try again.',
                          justify='center', style='red')
            main_menu()
    else:
        try:
            for worksheet in SHEET.worksheets():
                worksheet_data = worksheet.get_all_values()
                for row in worksheet_data[1:]:
                    index += 1
                    table.add_row(str(index), *row)
        except gspread.exceptions.WorksheetNotFound:
            console.print('Worksheet not found. Please try again.',
                          justify='center', style='red')
            main_menu()
        except gspread.exceptions.APIError:
            console.print('An Error occurred. Please try again.',
                          justify='center', style='red')
            main_menu()

    console.print(table, justify='center')


def delete_entry(result, worksheet):
    '''
    Delete current stock
    '''
    while True:

        console.print('You are about to delete this serial number from the system',
                      'Do you wish to continue?', 'Press Y for YES or N for NO',
                      justify='center', style='red')
        user_input = input()

        if user_input.lower() == 'y':
            current_row = result.row
            result_row_values = worksheet.row_values(result.row)
            worksheet.delete_rows(current_row)
            console.print('Serial number deleted successfully', ','.join(result_row_values),
                          justify='center', style='green')

            while True:
                console.print('Press S to search or M to go back to main menu',
                              justify='center', style='cyan')
                user_answer = input()
                if user_answer.lower() == 's':
                    validate_search_data()
                elif user_answer.lower() == 'm':
                    main_menu()
                else:
                    console.print('Invalid Input. Try again',
                                  justify='center', style='red')

        elif user_input.lower() == 'n':
            console.print('Redirecting to main menu',
                          justify='center', style='cyan')
            main_menu()
        else:
            console.print('Invalid Input. Try again',
                          justify='center', style='red')


def edit_entry(result, worksheet):
    '''
    Edit entry
    '''
    new_loc = stock_location_input()
    new_loc_name = stock_loc_name_input(new_loc)

    worksheet.update_cell(result.row, (result.col+1), new_loc)
    worksheet.update_cell(result.row, (result.col+2), new_loc_name)
    new_entry = worksheet.row_values(result.row)
    print(new_entry)
    if new_loc != worksheet.title:
        try:
            current_sheet = SHEET.worksheet(new_loc)
            current_sheet.append_row(new_entry)

            old_row = result.row
            worksheet.delete_rows(old_row)
            console.print(','.join(new_entry), 'updated successfully.',
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
        console.print(','.join(new_entry), 'updated successfully.',
                      justify='center', style='green')


def search_again_menu(result, worksheet):
    '''
    Search menu options
    '''
    while True:
        console.print('''Please Press:
        S to search again
        E to edit stock location
        D to delete
        Q for main menu''',
                      justify='center', style='cyan')
        user_input = input()
        if user_input.lower() == 's':
            validate_search_data()
        elif user_input.lower() == 'e':
            edit_entry(result, worksheet)

            console.print('Press S to search or M to go back to main menu',
                          justify='center', style='cyan')
            user_answer = input()
            if user_answer.lower() == 's':
                validate_search_data()
            elif user_answer.lower() == 'm':
                main_menu()
            else:
                console.print('Invalid Input. Try again',
                              justify='center', style='red')

        elif user_input.lower() == 'd':
            delete_entry(result, worksheet)

            console.print('Press S to search or M to go back to main menu',
                          justify='center', style='cyan')
            user_answer = input()
            if user_answer.lower() == 's':
                validate_search_data()
            elif user_answer.lower() == 'm':
                main_menu()
            else:
                console.print('Invalid Input. Try again',
                              justify='center', style='red')

        elif user_input.lower() == 'q':
            main_menu()
        else:
            console.print('Invalid Input. Try again',
                          justify='center', style='red')


def search_data(result, worksheet):
    '''
    Search data and displays it in a table
    '''
    result_row_data = worksheet.row_values(result.row)
    table = Table(title='Result')
    table.add_column('Item Name', justify='left', style='cyan')
    table.add_column('Serial No', justify='left', style='cyan')
    table.add_column('Location', justify='left', style='cyan')
    table.add_column('Name', justify='left', style='cyan')
    table.add_row(*result_row_data)
    console.print(table, justify='center')

    search_again_menu(result, worksheet)


def validate_search_data():
    '''
    Allows the user to search by serial number
    '''
    while True:
        console.print('Please enter the serial number you wish to search:',
                      justify='center', style='cyan')
        user_input = input()
        pattern = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
        if re.match(pattern, user_input) and 4 <= len(user_input) <= 20:
            result_found = False
            try:
                for worksheet in SHEET.worksheets():
                    result = worksheet.find(user_input.upper())
                    if result:
                        search_data(result, worksheet)
                        result_found = True
                if not result_found:
                    console.print('No results found',
                                  justify='center', style='red')
                    main_menu()
            except gspread.exceptions.WorksheetNotFound:
                console.print('Worksheet not found. Please try again.',
                              justify='center', style='red')
                main_menu()
            except gspread.exceptions.APIError:
                console.print('An Error occurred. Please try again.',
                              justify='center', style='red')
                main_menu()
        else:
            console.print(
                '''
                The input can contain alphanumeric values and dash
                The input must be between 4 and 20 characters
                ''', justify='center', style='red'
            )


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print('PRESS C TO ADD STOCK, PRESS V TO VIEW STOCK, PRESS S',
                      'TO SEARCH OR Q TO QUIT\n', justify='center',
                      style='cyan')
        user_input = input()
        if user_input.lower() == 'c':
            user_input = stock_input()
            entry = CreateStock(*user_input)

            add_stock(entry)
        elif user_input.lower() == 'v':
            view_stock_menu()
        elif user_input.lower() == 's':
            validate_search_data()
        elif user_input.lower() == 'q':
            quit()
        else:
            console.print('Invalid input. Please select one of the available ',
                          'options (C,V,S,Q)', justify='center', style='red')


main_menu()
