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



    def checkOut(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()


        cursor = connection.cursor()



        cartItemsQuery = "SELECT ISBN FROM Cart WHERE UserID=?"

        data = (userID,)

        cursor.execute(cartItemsQuery, data)

        result = cursor.fetchall()

        inventoryItemList = []

        i = 0

        for item in result:
            ISBN = result[i][0]
            inventoryItemList.append(ISBN)
            i = i + 1


        #for item in result:
            #for item in result[i]:
                #inventoryItemList.append(item)
            #i = i + 1



        for item in inventoryItemList:
            inventoryStockQuery = "SELECT Stock FROM Inventory WHERE ISBN=?"
            data = (item,)
            cursor.execute(inventoryStockQuery, data)
            result = cursor.fetchall()
            inventoryStock = result[0][0]

            cartStockQuery = "SELECT Quantity FROM Cart WHERE ISBN=?"
            cursor.execute(cartStockQuery, data)
            result = cursor.fetchall()
            cartStock = result[0][0]

            updatedStock = inventoryStock - cartStock

            if updatedStock < 0:
                print(f"Too many books with ISBN {item} in the cart.")
                successful = False
                break
            else:
                inventoryUpdateQuery = "UPDATE Inventory set Stock=? WHERE ISBN=?"

            data = (updatedStock, item)

            cursor.execute(inventoryUpdateQuery, data)

            connection.commit()


            #removing specific isbn from cart
            removeUserBooksQuery = "DELETE FROM Cart WHERE UserID=? AND ISBN=?"

            data = (userID, item)

            cursor.execute(removeUserBooksQuery, data)

            connection.commit()

            

        if successful != False:
            print("Successfully Checked Out!")


            
