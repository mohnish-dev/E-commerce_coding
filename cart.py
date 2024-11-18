import sqlite3
import sys
from inventory import *
from history import *


inventory = Inventory()
history = OrderHistory()

class Cart:

#constuctor with database name
    def __init__(self, databaseName = "methods.db"):
        self.databaseName = databaseName

    def viewCart(self, userID):
        #making sure we can connect to the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        cursor = connection.cursor()

        ISBNList = []

        ISBNQuery = "SELECT ISBN From Cart WHERE UserID=?"
        data = (userID,)
        cursor.execute(ISBNQuery, data)
        result = cursor.fetchall()
        i = 0

        for item in result:
            ISBN = result[i][0]
            ISBNList.append(ISBN)
            i = i + 1

        if len(ISBNList) == 0:
            print("There are no items in your cart to view.")

        else:
            for ISBN in ISBNList:
                CartInventoryQuery = "SELECT * FROM Inventory WHERE ISBN=?"
                data = (ISBN,)

                cursor.execute(CartInventoryQuery, data)
                result2 = cursor.fetchall()

                CartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"

                data = (userID, ISBN,)

                cursor.execute(CartQuantityQuery, data)

                result = cursor.fetchall()

                cartQuantity = result[0][0]

                for row in result2:

                    print('"', row[1], '" by ', row[2], ':', sep="")
                    print("\tISBN:", row[0])
                    print("\tGenre:", row[3])
                    print("\tPages:", row[4])
                    print("\tRelease Date:", row[5])
                    print("\tAmount in Cart:", cartQuantity)
                    print("\tPrice: $", row[6], sep="")
                    print()



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

                cartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                data = (userID, ISBN)
                cursor.execute(cartQuantityQuery, data)
                result = cursor.fetchall()

                if len(result) == 0:
                    bookAddQuery = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
                    data = (userID, ISBN, quantity)
                    cursor.execute(bookAddQuery, data)
                    connection.commit()
                    print("Item was added successfully!")
                else:
                    cartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                    data = (userID, ISBN)
                    cursor.execute(cartQuantityQuery, data)
                    result = cursor.fetchall()
                    cartQuantity = result[0][0]

                    updatedQuantity = cartQuantity + quantity
                    bookUpdateQuery = "UPDATE Cart SET Quantity=? WHERE UserID=? AND ISBN=?"
                    data = (updatedQuantity, userID, ISBN)
                    cursor.execute(bookUpdateQuery, data)
                    connection.commit()
                    print("Item was added successfully!")

                
            elif(bookQuantity == 0):
                print("There are no more books in stock.")
            else:
                print("There are not enough books in stock to add that amount to your cart.")

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

        print(result)

        inventoryItemList = []

        i = 0

        for item in result:
            ISBN = result[i][0]
            inventoryItemList.append(ISBN)
            i = i + 1
        print (inventoryItemList)


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

            cartStockQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
            data = (userID, item,)
            cursor.execute(cartStockQuery, data)
            result = cursor.fetchall()
            cartStock = result[0][0]

            updatedStock = inventoryStock - cartStock



            if updatedStock < 0:
                print(f"Too many books with ISBN {item} in the cart.")
                successful = False
                break
            else:
                inventoryUpdateQuery = "UPDATE Inventory SET Stock=? WHERE ISBN=?"
                data = (updatedStock, ISBN)
                cursor.execute(inventoryUpdateQuery, data)
                connection.commit
                #inventory.decreaseStock(ISBN, cartStock)
                
                removeBookQuery = "DELETE FROM Cart WHERE ISBN=?"
                data = (ISBN,)

                cursor = connection.cursor()
                cursor.execute(removeBookQuery, data)
                connection.commit()

        if successful != False:
            #for when the history class is complete
            #history.createOrder(userID, quantity, cost, date)
            #history.addOrderItems(userID, orderID)
            print("Successfuly Checked Out!")

    
    def getCost(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        cursor = connection.cursor()

        ISBNList = []
        ISBNCartQuery = "SELECT ISBN From Cart WHERE UserID=?"
        data = (userID,)
        cursor.execute(ISBNCartQuery, data)
        result = cursor.fetchall()

        i = 0
        for item in result:
            ISBN = result[i][0]
            ISBNList.append(ISBN)
            i = i + 1

        totalCost = 0
        i = 0

        for item in ISBNList:
            CartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
            data = (userID, item,)
            cursor.execute(CartQuantityQuery, data)
            result = cursor.fetchall()
            quantity = result[0][0]

            ItemPriceQuery = "SELECT Price FROM Inventory WHERE ISBN=?"
            data = (item,)
            cursor.execute(ItemPriceQuery, data)
            result = cursor.fetchall()
            itemPrice = result[0][0]

            itemCost = itemPrice * quantity

            totalCost = itemCost + totalCost


        return(totalCost)


            
