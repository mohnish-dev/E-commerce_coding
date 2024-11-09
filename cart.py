import sqlite3
from user import *
from inventory import *
import sys


def convertTuple(tuple):
        result = ""
        for i in tuple:
            for i in list:
                result = result + i
        result = int(result)
        return result

class Cart:

#constuctor with database name
    def __init__(self, user, inventory, databaseName = "methods.db"):
        self.databaseName = databaseName
        self.user = user
        self.inventory = inventory

    def cartAdd(self,user, inventory, item, quantity):

        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        booksTitleQuery = "SELECT Title FROM Inventory WHERE Title=?"
        data = (item,)

        cursor = connection.cursor()

        cursor.execute(booksTitleQuery, data)
        result = cursor.fetchall()

        if(len(result) == 0):
            print("That books is not in our inventory.")
        elif(len(result) >= 1):
            bookQuantityQuery = "SELECT Stock FROM Inventory WHERE Title=?"
            cursor.execute(bookQuantityQuery, data)
            result = cursor.fetchall()
            bookQuantity = result[0][0]

            if(quantity < bookQuantity):
                bookISBNQuery = "SELECT ISBN FROM Inventory WHERE Title=?"
                cursor.execute(bookISBNQuery, data)
                result = cursor.fetchall()
                isbnNumber = result[0][0]
                print(isbnNumber)
                bookAddQuery = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
                userID = user.getUserID()
                data = (userID, isbnNumber, quantity)
                #data = ('12-90909', '090909093', '3')
                cursor.execute(bookAddQuery, data)
                connection.commit()
                print("Item was added successfully!")
            elif(bookQuantity == 0):
                print("There are no more books in stock.")
            else:
                print("There are not enough books in stock.")
            
