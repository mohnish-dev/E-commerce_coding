from inventory import Inventory  # Importing Inventory class to interact with inventory data
import sqlite3  
import sys  
import random   

class OrderHistory:
    def __init__(self, db_name="methods.db"):
        # Constructor initializing the database name
        self.db_name = db_name

    def viewHistory(self, userID: str) -> None:
        """
        Fetch and display the order history for a given user.
        :param userID: ID of the user whose order history is to be fetched
        """
        try:
            # Connect to the database
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()

            # Query to fetch all orders for the specified user
            query = "SELECT * FROM Orders WHERE UserID=?"
            db_cursor.execute(query, (userID,))
            orders = db_cursor.fetchall()

            # Check if orders exist and display them
            if not orders:
                print("No order history found for this user.")
            else:
                print(f"Order History for User {userID}:")
                for order in orders:
                    print(f"OrderNumber: {order[0]}, Items: {order[2]}, Cost: {order[3]}, Date: {order[4]}")
            print()

        except sqlite3.Error as e:
            # Handle database errors
            print(f"Database error: {e}")
        finally:
            # Ensure the database connection is closed
            db_connection.close()

    def viewOrder(self, userID: str, orderID: str) -> None:
        """
        Fetch and display the details of a specific order for a given user.
        :param userID: ID of the user
        :param orderID: ID of the order to view
        """
        try:
            # Connect to the database
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()

            # Check if the order belongs to the user
            ownership_query = "SELECT UserID FROM Orders WHERE OrderNumber=?"
            db_cursor.execute(ownership_query, (orderID,))
            owner_result = db_cursor.fetchone()

            if not owner_result or owner_result[0] != userID:
                print("You are not authorized to view this order.")
                return

            ISBNList = []  # List to store ISBNs in the order

            # Query to fetch ISBNs of items in the order
            ISBNQuery = "SELECT ISBN From OrderItems WHERE OrderNumber=?"
            db_cursor.execute(ISBNQuery, (orderID,))
            result = db_cursor.fetchall()
            i = 0

            # Populate ISBNList with ISBNs from the query result
            for item in result:
                ISBN = result[i][0]
                ISBNList.append(ISBN)
                i = i + 1

            # Check if the order exists
            if len(ISBNList) == 0:
                print("The order you are looking for does not exist.")
            else:
                # Display details for each item in the order
                print("Here are the items in your order:")
                for ISBN in ISBNList:
                    CartInventoryQuery = "SELECT * FROM Inventory WHERE ISBN=?"
                    data = (ISBN,)

                    db_cursor.execute(CartInventoryQuery, data)
                    result2 = db_cursor.fetchall()

                    OrderQuantityQuery = "SELECT Quantity FROM OrderItems WHERE OrderNumber=? AND ISBN=?"
                    data = (orderID, ISBN,)
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
            # Handle database errors
            print(f"Database error: {e}")
        finally:
            # Ensure the database connection is closed
            db_connection.close()


    def createOrder(self, userID: str, quantity: int, cost: float, date: str) -> str:
        """
        Create a new order for a user.
        :param userID: ID of the user
        :param quantity: Number of items in the order
        :param cost: Total cost of the order
        :param date: Date of the order
        :return: The generated OrderID
        """
        while True:
            # Generate a 6-digit numeric OrderID
            orderID = str(random.randint(100000, 999999))

            try:
                # Connect to the database and check if OrderID is unique
                db_connection = sqlite3.connect(self.db_name)
                db_cursor = db_connection.cursor()

                db_cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderNumber = ?", (orderID,))
                if db_cursor.fetchone()[0] == 0:
                    break  # Unique OrderID found, break the loop

            except sqlite3.Error as error:
                # Handle errors during ID validation
                print(f"Error occurred while checking order ID uniqueness: {error}")
            finally:
                # Ensure the database connection is closed
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
        """
        Add items from a user's cart to an order.
        :param userID: ID of the user
        :param orderID: ID of the order
        """
        try:
            # Establish a connection to the database
            db_connection = sqlite3.connect(self.db_name)
        except:
            # Handle database connection failure
            print("Database connection failed.")
            sys.exit()

        db_cursor = db_connection.cursor()

        # Query to fetch all items from the user's cart
        query_cart = "SELECT * FROM Cart WHERE UserID=?"
        db_cursor.execute(query_cart, (userID,))
        cart_contents = db_cursor.fetchall()

        # Check if the cart is empty
        if not cart_contents:
            print("Shopping cart is empty.")
            db_connection.close()
            return

        # Transfer each item from the cart to the OrderItems table
        for cart_item in cart_contents:
            orderItemsAddQuery = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
            data = (orderID, cart_item[1], cart_item[2])
            db_cursor.execute(orderItemsAddQuery, data)
            db_connection.commit()

        print("Cart items added to order successfully.")
        db_connection.close()
