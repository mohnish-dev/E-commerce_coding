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
            # Establish a connection to the database
            db_connection = sqlite3.connect(self.db_name)
        except:
            # Handle database connection failure
            print("Database connection failed.")
            sys.exit()

        db_cursor = db_connection.cursor()

        # Query to fetch all orders for the specified user
        query = "SELECT * FROM Orders WHERE userID=?"
        db_cursor.execute(query, (userID,))
        orders = db_cursor.fetchall()

        if not orders:
            # Notify the user if no orders exist
            print("No order records found.")
        else:
            # Display all orders
            print("Order History:")
            for order in orders:
                print(f"Order ID: {order[0]}, Date: {order[3]}, Total Cost: ${order[2]:.2f}")
        print()

        # Close the database connection
        db_connection.close()

    def viewOrder(self, userID: str, orderID: str) -> None:
        try:
            # Establish a connection to the database
            db_connection = sqlite3.connect(self.db_name)
        except:
            # Handle database connection failure
            print("Database failed to connect.")
            sys.exit()

        db_cursor = db_connection.cursor()

        # Verify the order belongs to the specified user
        query = "SELECT * FROM Orders WHERE orderID=? AND userID=?"
        db_cursor.execute(query, (orderID, userID))
        order = db_cursor.fetchone()

        if not order:
            # Notify the user if the order is not found
            print("Order not found.")
            db_connection.close()
            return

        # Fetch items associated with the order
        query_items = "SELECT * FROM OrderItems WHERE orderID=?"
        db_cursor.execute(query_items, (userID,))
        items = db_cursor.fetchall()

        # Display order details
        print(f"Purchase ID: {orderID}, Date: {order[3]}, Total Cost: ${order[2]:.2f}")
        inventory_helper = Inventory()  # Initialize the Inventory class

        # Display item details for the order
        for item in items:
            item_info = inventory_helper.search_inventory_by_isbn(item[2])  # Fetch item details from inventory
            if item_info:
                print(f"Title: {item_info[1]}, Quantity: {item[3]}")
        print()

        # Close the database connection
        db_connection.close()

    def createOrder(self, userID: str, quantity: int, cost: float, date: str) -> str:
        # Generate a unique order ID using random alphanumeric characters
        orderID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        try:
            # Establish a connection to the database
            db_connection = sqlite3.connect(self.db_name)
            db_cursor = db_connection.cursor()

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
            query_add = "INSERT INTO OrderItems (orderID, userID, isbn, quantity) VALUES (?, ?, ?, ?)"
            db_cursor.execute(query_add, (orderID, userID, cart_item[2], cart_item[3]))

        # Clear the user's cart after transferring items
        db_cursor.execute("DELETE FROM Cart WHERE userID=?", (userID,))
        db_connection.commit()  # Commit changes to the database

        print("Cart items added to order successfully.")
        db_connection.close()
