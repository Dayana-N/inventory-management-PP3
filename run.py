'''
Main code for the program for terminal of 80 characters wide and 24 rows high
'''
import sys
from time import sleep
import re
import gspread
from google.oauth2.service_account import Credentials
from rich.console import Console
from rich.table import Table
from app_text import BORDER, INSTRUCTIONS

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


def typewritter(text, time):
    '''
    Creates typewritter effect,
    borrowed from StackOverflow
    '''
    for char in text:
        sleep(time)
        sys.stdout.write(char)
        sys.stdout.flush()


class Stock():
    '''
    Creates object for new stock
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
    numbers and empty spaces allowed, not empty space on it's own
    '''
    while True:
        console.print('PLEASE ENTER THE NAME OF THE STOCK YOU WISH TO ADD',
                      'FOR EXAMPLE: Clover Station', justify='center')
        stock_name = input()
        pattern = r"^(?!.*\s\s)(?=.*[a-zA-Z0-9])[a-zA-Z0-9\s]*[a-zA-Z0-9]$"
        if re.match(pattern, stock_name) and 4 <= len(stock_name) <= 17:
            return stock_name
        else:
            console.print(
                '''
                Spaces to be entered, but no more than one at a time.
                The input must end with an alphanumeric character.
                The input cannot contain two consecutive space characters.
                The input cannot consist only of space characters.
                The input must be between 4 and 17 characters
                ''', justify='center', style='red'
            )


def stock_serial_input():
    '''
    Validates the user input for serial number. Only letters,
    numbers and dash allowed
    '''
    stock_serial = ''
    while True:
        console.print('PLEASE ENTER THE SERIAL NUMBER YOU WISH TO ADD',
                      'FOR EXAMPLE: SN-1234', justify='center')
        serial_input = input()
        pattern = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
        if re.match(pattern, serial_input) and 4 <= len(serial_input) <= 17:
            stock_serial = serial_input
            break
        else:
            console.print(
                '''
                The input can contain alphanumeric values and dash
                The input must be between 4 and 17 characters
                ''', justify='center', style='red'
            )

    return stock_serial.upper()


def stock_location_input():
    '''
    Validates user input for stock location
    '''

    while True:
        console.print(
            '''
        PLEASE SELECT STOCK LOCATION:
        PRESS W FOR WAREHOUSE
        PRESS J FOR JOB/SITE
        PRESS E TO ASSIGN TO ENGINEER
        ''', justify='center')
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
    Checks the location and asks the user to enter
    location name based on the result, validates the input
    '''
    loc_name = ''
    if location == 'warehouse':
        while True:
            console.print('''
            PLEASE ENTER:
            G TO ADD TO GOOD STOCK,
            B TO ADD TO BAD STOCK''', justify='center')
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
                'PLEASE ENTER THE NAME OF THE SITE. FOR EXAMPLE: Circle K',
                justify='center')
            loc_name_input = input()
            pattern = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"
            if re.match(pattern, loc_name_input) and \
                    4 <= len(loc_name_input) <= 17:
                loc_name = loc_name_input
                break
            else:
                console.print('''
                The input can contain alphanumeric values and space
                The input must be between 4 and 17 characters
                ''', justify='center', style='red')
    elif location == 'engineer':
        while True:
            console.print(
                'PLEASE ENTER THE NAME OF ENGINEER. FOR EXAMPLE: John Smyth')
            loc_name_input = input()
            pattern = r"^[a-zA-Z]+(?: [a-zA-Z]+)*$"
            if re.match(pattern, loc_name_input) and \
                    4 <= len(loc_name_input) <= 17:
                loc_name = loc_name_input
                break
            else:
                console.print('''
                The input can contain alphanumeric values and space
                The input must be between 4 and 17 characters
                ''', justify='center', style='red')

    return loc_name


def stock_input():
    '''
    Calls the input validating functions and
    returns their values
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
    # Loop through spreadsheets and search serial number
    serial_num = entry.serial
    find_serial = None
    try:
        for worksheet in SHEET.worksheets():
            search_result = worksheet.find(serial_num)
            if search_result is not None:
                find_serial = search_result
    except gspread.exceptions.WorksheetNotFound:
        console.print('Worksheet not found. Please try again.',
                      justify='center', style='red')
        main_menu()

    # If no serial is found add the new entry to the spreadsheet
    if find_serial is None:
        try:
            current_sheet = SHEET.worksheet(entry.location)
            current_sheet.append_row([entry.s_name, entry.serial,
                                      entry.location, entry.loc_name])
            console.print(entry.s_name, entry.serial, entry.location,
                          entry.loc_name, 'ADDED SUCCESSFULLY.\n',
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

    while True:
        console.print(
            '''
    PLEASE PRESS
    A TO VIEW ALL STOCK
    W TO VIEW WAREHOUSE STOCK
    J TO VIEW JOB/SITE STOCK
    E TO VIEW ENGINEER STOCK
    M FOR MAIN MENU
    ''', justify='center')
        user_input = input()
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
        elif user_input.lower() == 'm':
            main_menu()
        else:
            console.print('Invalid input. Please try again',
                          justify='center', style='red')

    while True:
        console.print('PRESS B TO GO BACK OR M FOR MAIN MENU',
                      justify='center')
        user_input = input()
        if user_input.lower() == 'b':
            view_stock_menu()
            break
        elif user_input.lower() == 'm':
            main_menu()
        else:
            console.print('Invalid input. Redirecting to view stock menu',
                          justify='center', style='red')
            view_stock_menu()


def view_stock(worksheet_name=None):
    '''
    Displays the stock in a table format
    '''
    index = 0
    table = Table(title='LIST OF STOCK')
    table.add_column('№', justify='left')
    table.add_column('Item Name', justify='left')
    table.add_column('Serial No', justify='left')
    table.add_column('Location', justify='left')
    table.add_column('Name', justify='left')

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


def search_or_back_menu():
    '''
    Displays the search or back to menu option
    '''
    while True:
        console.print('PRESS S TO SEARCH OR M FOR MAIN MENU',
                      justify='center')
        user_answer = input()
        if user_answer.lower() == 's':
            search_data()
        elif user_answer.lower() == 'm':
            main_menu()
        else:
            console.print('Invalid Input. Redirecting to main menu...',
                          justify='center', style='red')
            main_menu()


def delete_entry(result, worksheet):
    '''
    Ask the user if they want to delete the serial number,
    deletes the row from the spreadsheet
    '''
    while True:

        console.print(
            '''
            You are about to delete this serial number from
            the system. Do you wish to continue?
            Press Y for YES or N for NO
            ''', justify='center', style='bright_red')
        user_input = input()

        if user_input.lower() == 'y':
            current_row = result.row
            result_row_values = worksheet.row_values(result.row)
            worksheet.delete_rows(current_row)
            console.print('Serial number deleted successfully',
                          ','.join(result_row_values), justify='center',
                          style='green')
            search_or_back_menu()

        elif user_input.lower() == 'n':
            console.print('Redirecting to main menu...',
                          justify='center')
            main_menu()
        else:
            console.print('Invalid Input. Try again.',
                          justify='center', style='red')


def edit_entry(result, worksheet):
    '''
    Takes user's input for location and location name,
    updates the corresponding cells with the new data,
    checks if the location is matching the correct spreadsheet,
    if not adds the row to the new spreadsheet and deletes it from the old
    '''
    new_loc = stock_location_input()
    new_loc_name = stock_loc_name_input(new_loc)

    worksheet.update_cell(result.row, (result.col+1), new_loc)
    worksheet.update_cell(result.row, (result.col+2), new_loc_name)
    new_entry = worksheet.row_values(result.row)
    if new_loc != worksheet.title:
        try:
            current_sheet = SHEET.worksheet(new_loc)
            current_sheet.append_row(new_entry)
            old_row = result.row
            worksheet.delete_rows(old_row)
            console.print(','.join(new_entry), 'updated successfully.\n',
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
        console.print(','.join(new_entry), 'updated successfully.\n',
                      justify='center', style='green')


def search_again_menu(result, worksheet):
    '''
    Search menu options
    '''
    while True:
        console.print(
            '''
        PLEASE PRESS:
        S TO SEARCH AGAIN
        E TO EDIT STOCK LOCATION
        D TO DELETE
        M FOR MAIN MENU
        ''', justify='center')

        user_input = input()
        if user_input.lower() == 's':
            search_data()
        elif user_input.lower() == 'e':
            edit_entry(result, worksheet)
            search_or_back_menu()

        elif user_input.lower() == 'd':
            delete_entry(result, worksheet)

        elif user_input.lower() == 'm':
            main_menu()
        else:
            console.print('Invalid Input. Redirecting to main menu...',
                          justify='center', style='red')
            main_menu()


def display_data(result, worksheet):
    '''
    Search data and displays it in a table
    '''
    result_row_data = worksheet.row_values(result.row)
    table = Table(title='Result')
    table.add_column('Item Name', justify='left')
    table.add_column('Serial No', justify='left')
    table.add_column('Location', justify='left')
    table.add_column('Name', justify='left')
    table.add_row(*result_row_data)
    console.print(table, justify='center')

    search_again_menu(result, worksheet)


def search_data():
    '''
    Allows the user to search by serial number in all worksheets
    Validates the user search input and handles any potential errors
    '''
    while True:
        console.print('Please enter the serial number you wish to search:',
                      justify='center')
        user_input = input().strip()
        pattern = r"^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$"
        if re.match(pattern, user_input) and 4 <= len(user_input) <= 17:
            result_found = False
            try:
                for worksheet in SHEET.worksheets():
                    result = worksheet.find(user_input.upper())
                    # result_found is updated only if there is a match
                    if result:
                        display_data(result, worksheet)
                        result_found = True
                if not result_found:
                    console.print('No results found\n',
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
                The input must be between 4 and 17 characters
                ''', justify='center', style='red'
            )


def quit_menu():
    '''
    Ask if the user wants to quit the program
    '''
    while True:
        console.print('Do you wish to exit the program?',
                      'Press Y for YES or N for NO',
                      justify='center', style='red')
        user_input = input()
        if user_input.lower() == 'y':
            console.print('Exiting... GoodBye!',
                          justify='center', style='green')
            quit()
        elif user_input.lower() == 'n':
            console.print('Redirecting to main menu...',
                          justify='center', style='green')
            main_menu()
        else:
            console.print('Invalid Input. Try again',
                          justify='center', style='red')


def welcome_screen():
    '''
    Prints welcome message with ASCII art
    '''
    console.print(BORDER, justify='center')


def display_info():
    '''
    Displays instructions on how to use
    the application
    '''
    typewritter(INSTRUCTIONS, 0.01)


def main_menu():
    '''
    Main menu function
    '''
    while True:
        console.print(
            '''
    ------ M A I N   M E N U ------

        PRESS C TO ADD STOCK
        PRESS V TO VIEW STOCK
        PRESS S TO SEARCH AND EDIT
        PRESS I FOR INSTRUCTIONS
        PRESS Q TO QUIT\n
    ''', justify='left')
        user_input = input()
        if user_input.lower() == 'c':
            user_input = stock_input()
            entry = Stock(*user_input)

            add_stock(entry)
        elif user_input.lower() == 'v':
            view_stock_menu()
        elif user_input.lower() == 's':
            search_data()
        elif user_input.lower() == 'i':
            display_info()
        elif user_input.lower() == 'q':
            quit_menu()
        else:
            console.print('Invalid input. Please select one of the available ',
                          'options (C,V,S,I,Q)', justify='center', style='red')


if __name__ == "__main__":
    welcome_screen()
    main_menu()
