from user import *
from cart import *
from inventory import *
from history import *

def orderHistoryMenu(user, history):
    while user.getLoggedIn():
        print("Order History Menu:")
        print("0. Go Back")
        print("1. View Order History")
        print("2. View Order")
        print()
        
        option = input("Enter your menu choice: ")
        print()
        
        if option == "0":
            # Return to the main menu
            break
        
        elif option == "1":
            # View the order history for the logged-in user
            userID = user.getUserID()
            history.viewHistory(userID)
        
        elif option == "2":
            # View details of a specific order
            userID = user.getUserID()
            orderID = input("Enter the Order ID you want to view: ")
            print()
            history.viewOrder(userID, orderID)
        
        else:
            # Handle invalid menu options
            print("That's not a valid menu option. Please try again.")
        print()
