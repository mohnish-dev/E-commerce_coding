import sqlite3
import sys


class Cart:

#constuctor with database name
    def __init__(self, databaseName = "methods.db"):
        self.databaseName = databaseName

    #def viewCart(userID):

    def addToCart(self,userID, ISBN, quantity = 1):

        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        bookISBNQuery = "SELECT ISBN FROM Inventory WHERE ISBN=?"
        data = (ISBN,)

        cursor = connection.cursor()

        cursor.execute(bookISBNQuery, data)
        result = cursor.fetchall()

        if(len(result) == 0):
            print("That book is not in our inventory.")
        elif(len(result) >= 1):
            data = (ISBN,)
            bookQuantityQuery = "SELECT Stock FROM Inventory WHERE ISBN=?"
            cursor.execute(bookQuantityQuery, data)
            result = cursor.fetchall()
            bookQuantity = result[0][0]

            if(quantity < bookQuantity):
                bookAddQuery = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
                data = (userID, ISBN, quantity)
                cursor.execute(bookAddQuery, data)
                connection.commit()
                print("Item was added successfully!")
            elif(bookQuantity == 0):
                print("There are no more books in stock.")
            else:
                print("There are not enough books in stock.")

    def removeFromCart(self, userID, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ISBNCartQuery = "SELECT ISBN FROM Cart WHERE ISBN=?"
        data = (ISBN,)

        cursor = connection.cursor()

        cursor.execute(ISBNCartQuery, data)
        result = cursor.fetchall()

        if(len(result) == 0):
            print("That book is not in your cart.")
        
        elif(len(result) >= 1):
            removeBookQuery = "DELETE FROM Cart WHERE ISBN=?"
            data = (ISBN,)

            cursor = connection.cursor()
            cursor.execute(removeBookQuery, data)
            connection.commit()
            print("Book successfully removed.")



    #def checkOut(userID):
            
