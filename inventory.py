import sqlite3
import sys

class Inventory:

    #constructor, passes the database name
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    #viewInventory function (no parameters)
    def viewInventory(self):
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
        #ensures the list isn't empty
        if len(result) > 0:
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
        else:
            print("Sorry, we could not find anything in the inventory.")
        
        cursor.close()
        connection.close()

    def searchInventory(self):
        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #selecting everything with a specific title (? is used for string substitution)
        query = "SELECT * FROM Inventory WHERE Title=?"
        data = (input("\nType the title you would like to search for: "),)
        #have to store as tuple
        #data = (title,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        print()
        #ensures the list isn't empty
        if len(result) > 0:
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
        else:
            print("Sorry, we could not find that title in our inventory.")

        cursor.close()
        connection.close()

    def decreaseStock(self, ISBN, quantity = 1):
        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        #our query for getting the stock
        stockQuery = "SELECT Stock FROM Inventory WHERE ISBN=?"
        cursor.execute(stockQuery, ISBN)
        #list of tuple, so using [0][0] to get the actual value
        stock = cursor.fetchall()[0][0]
        #stops stock from having a negative number
        if quantity > stock:
            stock = "0"
        else:
            stock = str(stock - quantity)

        #actual query to decrease the Stock amount in Inventory table
        decreaseQuery = "UPDATE Inventory SET Stock=? WHERE ISBN=?"
        data = (stock, ISBN[0],)
        cursor.execute(decreaseQuery, data)
        #have to actually commit the change
        connection.commit()

        #displays the updated stock to the user
        cursor.execute(stockQuery, ISBN)
        stock = cursor.fetchall()[0][0]
        print("The new stock is ", stock, ".\n", sep="")


