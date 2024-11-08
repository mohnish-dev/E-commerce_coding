import sqlite3
import sys

class Inventory:

    #constructor, passes the database name
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    #viewInventory function (no parameters)
    def viewInventory(self):
        print("Working on it")

        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #SELECT query for viewing the Invetory (which is just selecting everything)
        cursor.execute("SELECT * FROM Inventory")

        #actually getting the results of the query (list of tuples)
        result = cursor.fetchall()

        print("\nInventory Results:\n\n")

        #outputs each item in inventory and its information in a formatted way
        for row in result:
            print('"', row[1], '" by ', row[2], ':', sep="")
            print("\tISBN:", row[0])
            print("\tGenre:", row[3])
            print("\tPages:", row[4])
            print("\tRelease Date:", row[5])
            print("\tStock:", row[7])
            print("\tPrice: $", row[6], sep="")
            print()