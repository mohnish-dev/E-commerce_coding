from inventory import Inventory  # Importing Inventory class to interact with inventory data
import sqlite3  
import sys 
import random  
import string  

class OrderHistory:
    def __init__(self, db_name="methods.db"):
        self.db_name = db_name

    def viewHistory(self, userID: str) -> None:
        try:
            # Connect to the database
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()

            # Fetch all orders for the specified UserID
            query = "SELECT * FROM Orders WHERE UserID=?"
            db_cursor.execute(query, (userID,))
            orders = db_cursor.fetchall()

            if not orders:
                print("No order history found for this user.")
            else:
                print(f"Order History for User {userID}:")
                for order in orders:
                    print(f"OrderNumber: {order[0]}, Items: {order[2]}, Cost: {order[3]}, Date: {order[4]}")
            print()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            db_connection.close()

    def viewOrder(self, userID: str, orderNumber: str) -> None:
        try:
            # Connect to the database
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()
            '''
            # Fetch specific order details
            query = "SELECT * FROM Orders WHERE OrderNumber=? AND UserID=?"
            db_cursor.execute(query, (orderNumber, userID))
            order = db_cursor.fetchone()

            if not order:
                print("Order not found or does not belong to this user.")
            else:
                print(f"Order Details:")
                print(f"OrderNumber: {order[0]}, Items: {order[2]}, Cost: {order[3]}, Date: {order[4]}")
            print()'''



            ISBNList = []

            ISBNQuery = "SELECT ISBN From OrderItems WHERE OrderNumber=?"
            data = (orderNumber,)
            db_cursor.execute(ISBNQuery, data)
            result = db_cursor.fetchall()
            i = 0

            for item in result:
                ISBN = result[i][0]
                ISBNList.append(ISBN)
                i = i + 1

            if len(ISBNList) == 0:
                print("There are no items in your order to view.")

            else:
                print("Here are the items in your order:")
                for ISBN in ISBNList:
                    CartInventoryQuery = "SELECT * FROM Inventory WHERE ISBN=?"
                    data = (ISBN,)

                    db_cursor.execute(CartInventoryQuery, data)
                    result2 = db_cursor.fetchall()

                    OrderQuantityQuery = "SELECT Quantity FROM OrderItems WHERE OrderNumber=? AND ISBN=?"

                    data = (orderNumber, ISBN,)

                    db_cursor.execute(OrderQuantityQuery, data)

                    result = db_cursor.fetchall()

                    orderItemQuantity = result[0][0]

                    

                    for row in result2:

                        print('"', row[1], '" by ', row[2], ':', sep="")
                        print("\tISBN:", row[0])
                        print("\tGenre:", row[3])
                        print("\tPages:", row[4])
                        print("\tRelease Date:", row[5])
                        print("\tAmount in Order:", orderItemQuantity)
                        print("\tPrice: $", row[6], sep="")
                        print()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            db_connection.close()

    def createOrder(self, userID: str, quantity: int, cost: float, date: str) -> str:
        while True:
            # Generate a 6-digit numeric OrderID
            orderID = str(random.randint(100000, 999999))

            try:
                # Establish a connection to the database
                db_connection = sqlite3.connect(self.db_name)
                db_cursor = db_connection.cursor()

                # Check if the generated orderID already exists in the Orders table
                db_cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderNumber = ?", (orderID,))
                if db_cursor.fetchone()[0] == 0:
                    break  # The orderID is unique, break the loop

            except sqlite3.Error as error:
                # Handle errors during ID validation
                print(f"Error occurred while checking order ID uniqueness: {error}")
            finally:
                # Ensure the database connection is closed after checking
                db_connection.close()

        try:
            # Reconnect to the database to insert the new order
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()

            # Format the cost as a string with a dollar sign
            cost = f"${cost:.2f}"

            # Insert the new order into the Orders table
            db_cursor.execute(
                "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)",
                (orderID, userID, quantity, cost, date)
            )

            db_connection.commit()  # Commit changes to the database
            print(f"Order {orderID} created successfully.")
        except sqlite3.Error as error:
            # Handle errors during order creation
            print(f"Error occurred while creating order: {error}")
        finally:
            # Ensure the database connection is closed
            db_connection.close()

        return orderID

    def addOrderItems(self, userID: str, orderID: str) -> None:
        try:
            # Establish a connection to the database
            db_connection = sqlite3.connect(self.db_name)
        except:
            # Handle database connection failure
            print("Database connection failed.")
            sys.exit()

        db_cursor = db_connection.cursor()

        # Query to fetch all items from the user's cart
        query_cart = "SELECT * FROM Cart WHERE userID=?"
        db_cursor.execute(query_cart, (userID,))
        cart_contents = db_cursor.fetchall()

        if not cart_contents:
            # Notify the user if the cart is empty
            print("Shopping cart is empty.")
            db_connection.close()
            return

        # Transfer each item from the cart to the OrderItems table
        for cart_item in cart_contents:
            query_add = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
            db_cursor.execute(query_add, (orderID, cart_item[1], cart_item[2]))

        # Clear the user's cart after transferring items
        db_cursor.execute("DELETE FROM Cart WHERE userID=?", (userID,))
        db_connection.commit()  # Commit changes to the database

        print("Cart items added to order successfully.")
        db_connection.close()
