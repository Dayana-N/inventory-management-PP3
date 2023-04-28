# Inventory Management
[Link to deployed project](https://pp3-inventory-management-app.herokuapp.com/)
---
![Image of the app](./images/readme_img/app.PNG)

Inventory Management is a software program developed to facilitate the management of serialized inventory for businesses. This application is specifically tailored for businesses that utilize stock with unique serial numbers. The implemented features allow the user to efficiently add, search, view, change location, and delete stock from the system. These capabilities prove particularly valuable to businesses that install equipment in various locations and rely on engineering services to do so, as the program enables them to keep track of the precise location of each item.

# Table Of Content

-   [User Experience](#user-experience)
    -   [User Stories](#user-stories)
    -   [Goals](#goals)
    -   [Scope](#scope)
-   [Design](#design)
    -   [Colour Scheme](#colour-scheme)
    -   [Flowchart](#flowchart)
-   [Features](#features)
    -   [Welcome Screen](#Welcome-Screen)
    -   [Main Menu](#main-menu)
    -   [C - Add stock](#c---add-stock)
    -   [V - View Stock](#v---view-stock)
    -   [S - Search and edit](#s---search-and-edit)
    -   [I - Instructions](#i---instructions)
    -   [Q - Quit](#q---quit)
-   [Future Features](#future-features)
-   [Testing](#testing)
-   [Bugs](#Bugs)
-   [Technologies And Languages](#technologies-and-languages)
-   [Deployment](#deployment)
    -   [Creating A Fork](#creating-a-fork)
    -   [Cloning Repository](#cloning-repository)
-   [Credits](#credits)
    -   [Media](#media)
    -   [Code](#code)
    -   [Acknowledgements](#acknowledgements)
    -   [Comments](#comments)

---

# User Experience

## User Stories

1. As a warehouse manager, I want to easily add new items to the inventory system, so that I can keep track of all the items that we have in stock.
2. As a warehouse manager, I want to be able to search for specific items in the inventory system, so that I can quickly locate items when I need them.
3. As an engineer, I want to be able to update the location of items in the inventory system, so that I can keep track of the location of items that I need to use in the field.
4. As a warehouse manager, I want to be able to view all stock in the inventory system, so that I can have a comprehensive overview of all items in stock.
5. As an inventory manager, I want to be able to delete items from the inventory system, so that I can remove items that are no longer in use or have been added incorrectly
6. As an inventory manager, I want to be able to ensure that duplicate items are not added to the inventory system, so that I can maintain an accurate and efficient inventory.

## Goals

1. Simplify the process of adding new items to the inventory system
2. Develop a search feature to enable the users to quickly and easily locate items in the inventory system
3. Develop a feature that enables users to easily change the location of items in the inventory system
4. Enable users to delete items from the inventory system in a simple and efficient manner, ensuring the inventory remains up-to-date and accurate.
5. Develop a feature that allows users to easily view all of the stock in the inventory system or refine by location, making it easy to keep track of inventory in different locations.
6. Develop a feature that prevents the addition of duplicate items to the inventory system
7. Delevop easy to navigate menu
8. Add instructions on how to use the application

## Scope

Required functionality:

1. Easy to navigate menu
2. Add stock feature which allows the user to input name of the item, serial number, location and location name
3. Search the inventory by serial number and only add stock if it does not exist already
4. Display all stock or by location feature
5. Search the inventory by serial number and display all the information for this item
6. Change stock location feature
7. Delete stock from the system
8. Display instructions on how to user to program

# Design

## Colour Scheme
The main text colour is the standart white colour.<br>
Red colour was used to highlight invalid input and warning messages. <br>
Green colour was used to highlight success messages<br>
## Flowchart
The flowchart for the program was created by [diagrams.net](https://www.diagrams.net/)
<details>
<summary>Flowchart Image</summary>

![flowchart](./images/readme_img/flowchart.jpg)

</details>

# Features
## Welcome Screen
The welcome screen is displayed when the program runs. It uses ASCII art to surround the welcome message. 
![welcome screen](./images/readme_img/features/welcome-screen.PNG)
## Main Menu
The main menu is displayed when the program runs initially and when the user selects the main menu option from another menu. This menu allows the user to access the program's functionalities.
![main menu](./images/readme_img/features/main-menu.PNG) 
## C - Add stock
---
This option allows the user to add stock to the inventory system. The following steps are to add a stock name, serial number, stock location, and location name. Each input is validated and it will display a warning message to the user with guidelines for the input requirements. The user is presented with three possible locations for the serial number entered. 
1. Warehouse - This location has two options:
- Good - This is where all good stock is stored
- Bad - This is where faulty, broken stock or returns are stored
2. Job/Site - This is the location where the stock was installed
- The user must enter the name of the job.
3. Engineer - This location is selected when the stock is given to engineer's inventory
- Name of the engineer holding the stock must be entered.

![add stock](./images/readme_img/features/add-stock.PNG) <br>
The program will then check if this serial number already exist. If it doesn't exist will display all of the details entered in green with success message and will add the serial number. If the serial number already exist a message in red will appear to warn the user that this serial number is already on the system and will redirect back to the main menu.

## V - View Stock
This option allows the user to view the current inventory by location or all stock. The data is presented in a easy to read table. 
![view stock](./images/readme_img/features/view-stock.PNG) <br>
The user have the options to go back to view menu or back to main menu.

## S - Search and edit
This option allows the user to search the system by serial number. 
1. If the serial number doesn't exist on the system the user will be presented with a message in red advising that this serial number wasn't found. The user will be redirected to the main menu.
![search result not found](./images/readme_img/features/search-unsuccess.PNG) <br>
2. If the serial number exists on the system, the data will be displayed in a table. The user will be presented with a menu that will allow them to search again, edit, delete, or go back to the main menu.
![search result found](./images/readme_img/features/search-success.PNG) <br>
- The search again option will bring the user back to the search screen and will ask for the serial number.
- The edit stock location will allow the user to change the location of the stock. It will require location input followed by location name. If the input is valid the user will be presented with a success message with the new details saved on the system. The user can either search again or go back to the main menu.
![edit stock location](./images/readme_img/features/edit-location.PNG) <br>
- The delete option will ask the user for confirmation if they wish to delete the serial number from the system. Once the user presses Y the data is deleted permanently. 
![delete stock](./images/readme_img/features/delete.PNG) <br>
- The main menu option brings the user back to the main menu.

## I - Instructions
This option will print to the user the instructions on how to use the application. Then the main menu is displayed. 

## Q - Quit
The user will be asked for confirmation if they wish to quit.
- Y exits the program
- N brings the user back to the main menu.
![quit](./images/readme_img/features/quit.PNG) <br>

# Future Features
- I would like to use a database to store all the data.
- I would like to implement a feature showing stock movements for each serial number. 
- I would like to build a front end for this application for easier navigation through the features

# Testing

# Bugs
1. During the testing stages of the application an infinite loop was discovered when invalid input was entered. The message invalid input kept printing. This was resolved by printing the menu within the while loop. 
2. Before a new serial number is added, the system will loop through each spreadsheet and search if the serial number exists and will update a variable with the result. I was getting incorrect results due to the fact that the variable was updated on every loop and if the serial number is not found in the last spreadsheet then the variable is updated as not found. This was resolved by adding a condition to update the variable only if the result is not none. Screenshot attatched showing the value of the variable changing on each loop. Further tests confirmed that the issue was resolved
![bug](./images/readme_img/bug-adding-serial.PNG) <br>

# Technologies And Languages
## Languages Used
- Python
- CSS to add style to the body of layout.html

## Python Modules
- [Gspread](https://docs.gspread.org/en/latest/index.html) - to access Google Sheets and edit data
- [Google auth](https://google-auth.readthedocs.io/en/stable/index.html) - was used for authentication with google APIs using credentials.
- [Sys](https://docs.python.org/3/library/sys.html?highlight=sys#module-sys) - to call specific functions to allow to display the text with typewritter effect
- [Time](https://docs.python.org/3/library/time.html?highlight=time#module-time) - to add a sleep function between displaying each character
- [Re](https://docs.python.org/3/library/re.html?highlight=re#module-re) - to create a regex pattern for input validation
- [Rich](https://rich.readthedocs.io/en/stable/introduction.html) - to create tables and add colour to text
## User defined modules
- app_text - was used to store the welcome screen ASCII and the instructions on how to use the application.
## Technologies and programs


