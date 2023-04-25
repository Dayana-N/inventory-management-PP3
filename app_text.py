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
Inventory Management is a program designed to manage serialized inventory for
businesses. Upon launching the program, you will see a main menu with the
following options:

Press C to add stock
Press V to view stock
Press S to search and edit
Press I for instructions
Press Q to quit

To add stock, press C and enter the name of the item/stock and its serial
number. Then, select the location of the stock from the following menu:

Press W for warehouse
Press J for job/site
Press E to assign to an engineer

If the selected location is a warehouse, you will be prompted to choose
between adding the stock to the "G" for good stock location or "B" for
bad stock location.
If the selected location is a job/site, the system will ask for the name
of the site where the stock was installed/shipped to.
If the selected location is an engineer, the system will ask for the name of
the engineer.

The system will then check if the serial number already exists in the database.
If it doesn't, the system will add it. If it does, the system will display a
message in red and redirect to the main menu.

To view stock, press V and choose whether to view all stock or by location.
The data will be displayed in a table.

To search and edit, press S and enter the serial number. If the serial number
is found, it will be displayed in a table, and the following menu will appear:

Press S to search again
Press E to edit stock location
Press D to delete
Press M for the main menu

To edit the location of the displayed serial number, press E and enter the
new location. To delete the serial number, press D and confirm the deletion.

Full documentation can be found at:
https://github.com/Dayana-N/inventory-management-PP3
'''
