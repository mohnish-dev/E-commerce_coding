import sqlite3
import sys
from inventory import *
from history import *
from datetime import date


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

        #establishing cursor for queries
        cursor = connection.cursor()

        #creating empty ISBN list
        ISBNList = []

        #getting ISBN values from cart for certain user
        ISBNQuery = "SELECT ISBN From Cart WHERE UserID=?"
        
        #using the userID as the ? substition in the query above as a tuple (similar pattern for other queries)
        data = (userID,)
        cursor.execute(ISBNQuery, data)
        
        #result of query
        result = cursor.fetchall()
        

        #appending ISBNs to the ISBN list
        i = 0
        for item in result:
            #result is in tuple format, so to get the certain value a variable is assigned with result[0][0] 
            #(result [i][0] in this case with the for loop)
            ISBN = result[i][0]
            ISBNList.append(ISBN)
            i = i + 1

        
        #if no ISBN is present in the User's cart (the user has no books)
        if len(ISBNList) == 0:
            print("There are no items in your cart to view.")
            cursor.close()
            connection.close()

        #at least 1 ISBN value is present in the user's cart
        else:
            print("Here are the items in your cart:")
            
            #iterating over each item in the ISBN list (which contains the ISBN values in the user's cart)
            for ISBN in ISBNList:

                #viewing inventory data based on ISBN
                CartInventoryQuery = "SELECT * FROM Inventory WHERE ISBN=?"
                data = (ISBN,)
                cursor.execute(CartInventoryQuery, data)
                result2 = cursor.fetchall()

                #query to get current stock of book based on ISBN value 
                CartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                data = (userID, ISBN,)
                cursor.execute(CartQuantityQuery, data)
                result = cursor.fetchall()
                cartQuantity = result[0][0]

                #print statements similar to view inventory
                for row in result2:
                    print('"', row[1], '" by ', row[2], ':', sep="")
                    print("\tISBN:", row[0])
                    print("\tGenre:", row[3])
                    print("\tPages:", row[4])
                    print("\tRelease Date:", row[5])
                    print("\tAmount in Cart:", cartQuantity)
                    print("\tPrice: $", row[6], sep="")
                    print()
            cursor.close()
            connection.close()



    def addToCart(self,userID, ISBN, quantity = 1):

        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            sys.exit()

        cursor = connection.cursor()

        #getting ISBN values from Inventory where ISBN (column data) equals the ISBN parameter value
        bookISBNQuery = "SELECT ISBN FROM Inventory WHERE ISBN=?"
        data = (ISBN,)
        cursor.execute(bookISBNQuery, data)
        result = cursor.fetchall()

        #if the results of query are empty, there are no books with that ISBN in the inventory
        if(len(result) == 0):
            print("Sorry, we do not have that book in our inventory.")
            cursor.close()
            connection.close()
        
        #if the quantity the user enters is less than 1
        elif quantity < 1:
            print("Sorry, you can't add 0 or fewer books to your cart.")
            cursor.close()
            connection.close()

            
        #if the ISBN value (the value the user passed in as a parameter) exists in the inventory database
        elif(len(result) >= 1):

            #getting the current stock of the book with the ISBN parameter value using the inventory getStock() function
            currentISBNInventoryStock = inventory.getStock(ISBN)

            #getting ISBN from cart that is equal to ISBN parameter value and the userID that is equal to the userID parameter value
            cartISBNQuery = "SELECT ISBN FROM Cart WHERE UserID=? AND ISBN=?"
            
            #substituting for two ? values
            data = (userID, ISBN)
            cursor.execute(cartISBNQuery, data)
            result2 = cursor.fetchall()

            #if the book does not exist in the user's cart
            if len(result2) == 0:
                #bool value that is true if the book with the ISBN parameter value is currently in the user's cart
                doesExist = False

            #if teh book exists in the user's cart
            else:
                #setting doesExist to true
                doesExist = True

                #getting the quantity of books from cart where userID and ISBN are equal to the parameter values that are passed in
                cartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                data = (userID, ISBN)
                cursor.execute(cartQuantityQuery, data)
                result2 = cursor.fetchall()

                #variable for stock of book with ISBN parameter value in the user's cart
                currentISBNCartStock = result2[0][0]

            #using if and else statments to determing if the book is inserted into cart or amount is updated in cart
            #if the item with the ISBN parameter value is currently in the user's cart
            if doesExist != True:
                
                #if the current stock of the book in the inventory is equal to 0
                if(currentISBNInventoryStock == 0):
                    print("Sorry, there are no more books in stock.")
                    cursor.close()
                    connection.close()

                #if the quantity parameter value (the amount the user wants to add) is greater than the stock of the book in the inventory
                elif(quantity > currentISBNInventoryStock):
                    print("Sorry, there are not enough books in stock to add that amount to your cart.")
                    cursor.close()
                    connection.close()

                #if the quantity parameter value is less than or equal to the current amount of books in the inventory
                elif(quantity <= currentISBNInventoryStock):

                    #inserting userID, ISBN, and quantity parameter values into cart
                    bookAddQuery = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
                    data = (userID, ISBN, quantity)
                    cursor.execute(bookAddQuery, data)

                    #commiting changes to database
                    connection.commit()
                    print("Item was added to the cart successfully!")

            #if the item with the ISBN parameter value is not in the user's cart
            else:
                
                #if the current stock of the book in the inventory is equal to 0
                if(currentISBNInventoryStock == 0):
                    print("Sorry, there are no more books in stock.")
                    cursor.close()
                    connection.close()

                #if the quantity parameter value + the currentISBNCartStock is greater than the stock of that item in the inventory (currentISBNInventoryStock)
                #essentially stopping the user from adding that number of items to the cart if that number would make the total in the cart exceed the amount of stock in the inventory
                elif(quantity + currentISBNCartStock > currentISBNInventoryStock):
                    print("Sorry, could not add books to your cart because the total number of books in the cart will exceed the amount in stock.")
                    cursor.close()
                    connection.close()

                #if the quantity parameter value (the amount the user wants to add) is greater than the stock of the book in the inventory
                elif(quantity > currentISBNInventoryStock):
                    print("Sorry, there are not enough books in stock to add that amount to your cart.")
                    cursor.close()
                    connection.close()
                
                #if the quantity parameter value is less than or equal to the current amount of books in the inventory
                elif(quantity <= currentISBNInventoryStock):
                    
                    #getting quantity from Cart where UserID and ISBN are equal to userID and ISBN parameter values
                    cartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                    data = (userID, ISBN)
                    cursor.execute(cartQuantityQuery, data)
                    result = cursor.fetchall()

                    #establising cartQuantity
                    cartQuantity = result[0][0]

                    #creating updatedQuantity and setting its value to cartQuantity + the quantity parameter value (the amount the user wants to add)
                    updatedQuantity = cartQuantity + quantity

                    #query to update the current quantity in the cart with the updatedQuantity variable
                    #UserID and ISBN are equal to userID and ISBN parameter values, and Quantity is equal to updatedQuantity
                    bookUpdateQuery = "UPDATE Cart SET Quantity=? WHERE UserID=? AND ISBN=?"
                    data = (updatedQuantity, userID, ISBN)
                    cursor.execute(bookUpdateQuery, data)

                    #commit changes to database
                    connection.commit()
                    print("Item was added to the cart successfully!")
                    cursor.close()
                    connection.close()



    def removeFromCart(self, userID, ISBN):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        #query that gets ISBN from Cart where userID and ISBN are equal to userID and ISBN parameter values
        ISBNCartQuery = "SELECT ISBN FROM Cart WHERE UserID=? AND ISBN=?"
        data = (userID, ISBN)
        cursor = connection.cursor()
        cursor.execute(ISBNCartQuery, data)
        result = cursor.fetchall()

        #if the book with the ISBN parameter value is not in the cart
        if(len(result) == 0):
            print("That book is not in your cart.")
            cursor.close()
            connection.close()
        
        #if the book is in the cart
        elif(len(result) >= 1):
            #query to remove entire row from Cart where UserID and ISBN are equal to the userID and ISBN parameter values
            removeBookQuery = "DELETE FROM Cart WHERE UserID=? AND ISBN=?"
            data = (userID, ISBN,)
            cursor = connection.cursor()
            cursor.execute(removeBookQuery, data)

            #commit the changes to the database
            connection.commit()
            cursor.close()
            connection.close()
            print("Book successfully removed.")
            



    def checkOut(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()


        cursor = connection.cursor()

        #setting bool value that tracks if the user will be able to checkout or not (basically another layer of error checking)
        isNegative = True


        #getting ISBN values from Cart where UserID is equal to the userID parameter value
        cartItemsQuery = "SELECT ISBN FROM Cart WHERE UserID=?"
        data = (userID,)
        cursor.execute(cartItemsQuery, data)
        result = cursor.fetchall()

        #creating empty list that will contain ISBNs in the cart
        cartItemList = []

        i = 0

        for item in result:
            #appending ISBNs to list
            ISBN = result[i][0]
            cartItemList.append(ISBN)
            i = i + 1
        
        #if the list of ISBNs is empty, then the cart does not contain any items
        if len(cartItemList) == 0:
            print("Your cart is empty.")
            cursor.close()
            connection.close()

        #if the cart is not empty
        else:
            #iterating over each ISBN in the cartItemList
            for item in cartItemList:
                #using the getStock() inventory function with the current item (ISBN) value to get its current stock
                inventoryStock = inventory.getStock(item)

                #getting quantity of item in cart where UserID an ISBN are equal to the userID parameter value and the ISBN value in the list (at the particular iteration)
                cartStockQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                data = (userID, item)
                cursor.execute(cartStockQuery, data)
                result = cursor.fetchall()

                #establishing quantity of that specific item (ISBN) value
                cartQuantity = result[0][0]

                #the new stock value that the item (ISBN) value will have in the inventory
                updatedStock = inventoryStock - cartQuantity


                #checking if updatedStock would be less than 0
                if updatedStock < 0:
                    print(f"Too many books with ISBN {item} in the cart.")
                    cursor.close()
                    connection.close()
                    
                    #setting isNegative to false
                    isNegative = False

            #not continuing with function if isNegative is equal to false; allowing user to checkout if it is equal to true
            if isNegative != False:
                #creating empty list of ISBNs
                ISBNList = []

                #getting ISBN values from Cart where UserID is equal to the userID parameter value
                ISBNCartQuery = "SELECT ISBN From Cart WHERE UserID=?"
                data = (userID,)
                cursor.execute(ISBNCartQuery, data)
                result = cursor.fetchall()

                #appending ISBN values (item) to the ISBN list
                i = 0
                for item in result:
                    ISBN = result[i][0]
                    ISBNList.append(ISBN)
                    i = i + 1
                
                #getting total cost of the order
                totalCost = 0

                for item in ISBNList:
                    #getting quantity from Cart where UserID and ISBN are equal to userID and ISBN parameter values
                    CartQuantityQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                    data = (userID, item,)
                    cursor.execute(CartQuantityQuery, data)
                    result = cursor.fetchall()

                    #establishing quantity variable
                    quantity = result[0][0]

                    #establishing itemPrice using getPrice() inventory function and item (ISBN value) as the parameter
                    itemPrice = inventory.getPrice(item)

                    #establishing itemCost (for the item (ISBN value) in the particular iteration)
                    itemCost = itemPrice * quantity

                    #adding itemCost to totalCost
                    totalCost = itemCost + totalCost

                #converting totalCost to a float value
                totalCost = float(totalCost)


                #establishing currentDate  and orderDate using datetime library functions
                currentDate = date.today()
                #establishing and correctly formating orderDate
                orderDate = currentDate.strftime('%m/%d/%Y')


                #get total quantity of items in cart
                #creating empty list used to store ISBN values in the current user's cart
                cartISBNList = []

                #getting ISBN values from Cart where UserID is equal to the userID parameter value
                cartISBNQuery = "SELECT ISBN FROM Cart WHERE UserID=?"
                data = (userID,)
                cursor.execute(cartISBNQuery, data)
                result = cursor.fetchall()
                
                
                #iterating through result, appending item (ISBN values) to the cartISBNList
                i = 0
                for item in result:
                    cartISBN = result[i][0]
                    cartISBNList.append(cartISBN)
                    i += 1

                #initializing totalItemQuantity
                totalItemQuantity = 0

                #iterating through cartISBNList, adding the quantity of that ISBN value in the cart to the total in each iteration
                for item in cartISBNList:
                    #getting quantity from Cart where UserID is equal to userID parameter value and ISBN is equal to item (ISBN value)
                    cartStockQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                    data = (userID, item)
                    cursor.execute(cartStockQuery, data)
                    result = cursor.fetchall()

                    #establishing cartQuantity
                    cartQuantity = result[0][0]

                    #setting totalItemQuantity's value with totalItemQuantity + cartQuantity
                    totalItemQuantity = totalItemQuantity + cartQuantity

                #creating orderID variable and assigning it with the createOrder history function
                #using userID parameter value along with totalItemQuantity, totalCost, and orderDate
                orderID = history.createOrder(userID, totalItemQuantity, totalCost, orderDate)

                #adding items to the order using addOrderItems() history function, which uses the userID parameter value and the orderID created above
                history.addOrderItems(userID, orderID)
                    
                #iterating through items in the cartIBSNList, removing each one in each iteration 
                for item in cartISBNList:
                    #getting quantity from Cart where UserID and ISBN are equal to userID parameter value and item (IBSN value)
                    cartStockQuery = "SELECT Quantity FROM Cart WHERE UserID=? AND ISBN=?"
                    
                    #creating ISBN variable as item tuple to use it in decreaseStock function
                    ISBN = (item,)
                    data = (userID, item)
                    cursor.execute(cartStockQuery, data)
                    result = cursor.fetchall()

                    #quantity of item (ISBN) in user's cart
                    cartQuantity = result[0][0]

                    #decreasing stock of that item in the inventory by the amount of that item in the cart
                    #using decreaseStock() inventory function
                    inventory.decreaseStock(ISBN, cartQuantity)
    
                    #query to remove entire row from Cart where UserID is equal to the userID parameter value and ISBN is equal to item (ISBN value)
                    removeBookQuery = "DELETE FROM Cart WHERE UserID=? AND ISBN=?"
                    data = (userID, item)

                    cursor = connection.cursor()
                    cursor.execute(removeBookQuery, data)

                    #commiting to database
                    connection.commit()

                #will print when successfully checked out    
                print("Successfuly Checked Out!")
                cursor.close()
                connection.close()
