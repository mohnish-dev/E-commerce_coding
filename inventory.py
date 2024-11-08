import sqlite3
import sys

class Inventory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    def viewInventory(self):
        print("Working on it")

        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Inventory")

        result = cursor.fetchall()

        print("Inventory Results:\n\n")

        for row in result:
            print("Test")
