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
        #have to store as tuple
        data = (input("\nType the title you would like to search for: "),)

        cursor.execute(query, data)
        result = cursor.fetchall()

        print()
        if len(result) > 0:
            #outputs each item in inventory and its information in a formatted way (same as viewInventory)
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
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            sys.exit()

        cursor = connection.cursor()

        #our query for getting the stock
        stockQuery = "SELECT Stock FROM Inventory WHERE ISBN=?"

        #ensuring the ISBN is correctly formatted and actually exists in Inventory
        try:
            cursor.execute(stockQuery, ISBN)
            #list of tuple, so using [0][0] to get the actual value
            stock = cursor.fetchall()[0][0]
        #if it doesn't exist in inventory
        except IndexError:
            print("Could not decrease the stock of ", ISBN[0], "; please make sure the ISBN is correct.\n", sep="")
            return
        #if the formatting is wrong (or some other error)
        except:
            print(ISBN, "was not inputted in the correct format.\n")
            return

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
        #if it doesn't exist in Inventory

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

        #checks that the query actually returned a result; otherwise, program will crash with list index error
        try:
            #returns the result (have to go into a list of a tuple)
            return result[0][0]
        except:
            print("Could not find the title for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")
        
    
    def getAuthor(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        #I wasn't sure how to create one, singular function that would get whatever value was needed from Inventory table
        #but I didn't want all these getters bloating my code...
        #so I put everything on one line separated by semicolons :)
        #it's the same code as getTitle, just with Author instead of Title
        cursor = connection.cursor();query = "SELECT Author FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the author for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")
    
    def getGenre(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Genre FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the genre for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")
    
    def getPages(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Pages FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the pages for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")
    
    def getReleaseDate(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT ReleaseDate FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the release date for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")
    
    def getPrice(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()
        cursor = connection.cursor();query = "SELECT Price FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the price for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")

    def getStock(self, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.");sys.exit()        
        cursor = connection.cursor();query = "SELECT Stock FROM Inventory WHERE ISBN=?";data = (ISBN,);cursor.execute(query, data);result = cursor.fetchall();cursor.close();connection.close()
        try:
            return result[0][0]
        except:
            print("Could not find the stock for ", ISBN, "; please make sure the ISBN is correct.\n", sep="")