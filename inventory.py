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
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            sys.exit()

        cursor = connection.cursor()

        #selecting everything with a specific title (? is used for string substitution)
        query = "SELECT * FROM Inventory WHERE Title=?"
        sentinel = "Not N"
        while (sentinel != "N"): ###
            #have to store as tuple
            data = (input("\nType the title you would like to search for: "),)

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
                    sentinel = input("Would you like to search for another title? (Type N to quit or anything else to continue) ") ###
            else:
                sentinel = input("Sorry, we could not find that title in our inventory. Would you like to try again? (Type N to quit or anything else to continue) ") ###

        print()
        cursor.close()
        connection.close()

    def decreaseStock(self, ISBN, quantity = 1):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            sys.exit()

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

        cursor.close()
        connection.close()

    def getTitle(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            sys.exit()

        cursor = connection.cursor()

        #searching for a particular attribute of a certain ISBN; for this function, Title
        query = "SELECT Title FROM Inventory WHERE ISBN=?"
        data = (ISBN,)
        cursor.execute(query, data)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        #returns the result (have to go into a list of a tuple)
        return result[0][0]
        
    
    def getAuthor(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        #I wasn't sure how to create one, singular function that would get whatever value was needed from Inventory table
        #but I didn't want all these getters bloating my code...
        #so I put everything on one line separated by semicolons :)
        #it's the same code as getTitle, just with Author instead of Title
        cursor = connection.cursor();query = "SELECT Author FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]
    
    def getGenre(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Genre FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]
    
    def getPages(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Pages FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]
    
    def getReleaseDate(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT ReleaseDate FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]
    
    def getPrice(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Price FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]

    def getStock(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()        
        cursor = connection.cursor();query = "SELECT Stock FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close();return result[0][0]