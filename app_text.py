'''
This file holds all large strings
'''

BORDER = '''
    _________________________________________________________________________
   |   ___________________________________________________________________   |
   |  |                                                                   |  |
   |  |                ===============================                    |  |
   |  |                | |      W E L C O M E      | |                    |  |
   |  |                | |           T O           | |                    |  |
   |  |                | |  INVENTORY MANAGEMENT   | |                    |  |
   |  |                | |                         | |                    |  |
   |  |                ===============================                    |  |
   |  |                                                                   |  |
   |  |___________________________________________________________________|  |
   |_________________________________________________________________________|
'''
INSTRUCTIONS = '''
Inventory Management allows you to manage serialized inventory.
The program can help any business track its serialized stock.
When you run the program you will be presented with the main menu.\n
PRESS C TO ADD STOCK
PRESS V TO VIEW STOCK,
PRESS S TO SEARCH AND EDIT
PRESS I FOR INSTRUCTIONS
PRESS Q TO QUIT \n
To add stock to the system press C. The system will then ask for
name of the particular item/stock and serial number. After that, you can
add the location of the stock:\n
PRESS W FOR WAREHOUSE
PRESS J FOR JOB/SITE
PRESS E TO ASSIGN TO ENGINEER\n
If you select W for warehouse the system will ask if the stock
should be added to G for good stock location (working stock) or
B for bad stock location (faulty stock, broken returns, etc)\n
If you select J for job/site, the system will ask for the name of
the site that the stock was installed/shipped to\n
If you select E for an engineer, the system will ask for the
name of the engineer that holds this stock.\n
The system will then check if the serial number exists on the system and if
it doesn't it will add it to the system and will display all the information
added. If the serial number already exists the system will display a message
in red letting the user know that the serial number already exists and will
redirect to the main menu.\n
If you wish to view stock from the main menu press V. The system will ask if
you wish to view all stock, or by location and will then display the data in
a table.\n
If you wish to search and edit you can do so by pressing S to search.
The system will ask for the serial number and will search the system. If the
serial number is not found the system will let the user know and will redirect
to the main menu. If the serial number is found it will be displayed in
a table. You will can then \n
PRESS:
S TO SEARCH AGAIN
E TO EDIT STOCK LOCATION
D TO DELETE
M FOR MAIN MENU\n
To edit the location of the displayed serial number press E. The system will
ask for the new location and will update the system.\n
To delete the displayed serial number press D. The system will ask if you wish
to proceed and will delete the serial number permanently from the system.\n
Full documentation can be found at:
https://github.com/Dayana-N/inventory-management-PP3
'''
