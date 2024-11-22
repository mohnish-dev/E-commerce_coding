from user import *
from cart import *
from inventory import *
from history import *


## COMPLETE initial pre-login menu
def initialMenu():
    ## objects for the classes
    user = User()
    cart = Cart()
    inventory = Inventory()
    history = OrderHistory()

    ## initial menu
    while(1):
        print("Pre-Login Menu:")
        print("0. Login")
        print("1. Create Account")
        print("2. Exit Program")
        initial = input("Enter your menu choice: ")
        print()

        if(initial == "0"):
            user.login()

        elif(initial == "1"):
            user.createAccount()

        ## exit program
        elif(initial == "2"):
            print("Good-bye!")
            break

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

        ## checks status after one menu loop...
        ## goes into main menu if applicable
        if(user.getLoggedIn()):
            mainMenu(user, cart, inventory, history)


## incomplete main menu...
def mainMenu(user, cart, inventory, history):
    while(user.getLoggedIn()):
        print("Main Menu:")
        print("0. Logout")
        print("1. View Account Information")
        print("2. Inventory Information")
        print("3. Cart Information")
        print("4. Order Information")
        option = input("Enter your menu choice: ")
        print()

        ## logging out
        if(option == "0"):
            user.logout()

            print("Successful logout.")

        # looking at inventory options
        elif(option == "2"):
            #initializing our option variable so that it's != 0
            print("Inventory Menu:")
            print("0. Go Back")
            print("1. View Inventory")
            print("2. Search Inventory (for a specific item)")
            print()
            i_option = input("Enter your menu choice: ")

            if(i_option == "0"):
                continue

            elif(i_option == "1"):
                inventory.viewInventory()

            elif(i_option == "2"):
                inventory.searchInventory()

            else:
                print("Oops, you didn't enter a valid menu option. Please try again.")

        #looking at cart options
        elif(option == "3"):
            print("Cart Menu:")
            print("0. Go back")
            print("1. View Cart")
            print("2. Add items to Cart")
            print("3. Remove an Item from Cart")
            print("4. Check Out")
            print()

            print("Enter your menu choice: " , end = "")
            c_input = input()
            print()

            if (c_input == "0"):
                continue

            elif (c_input == "1"):
                print("Here are the items in your cart:")
                userID = user.getUserID()
                cart.viewCart(userID)

            elif (c_input == "2"):
                print()
                print("Here is the current inventory of books:")
                print()
                inventory.viewInventory()
                print("What book (based on ISBN number) would you like to add to your cart: ", end = "")
                ISBN = input()

                print("How many books would you like to add to your cart: ", end = "")
                quantity = int(input())
                userID = user.getUserID()
                cart.addToCart(userID, ISBN, quantity)

            elif (c_input == "3"):
                print("What book (based on ISBN number) would you like to remove from your cart: ", end = "")
                ISBN = input()
                userID = user.getUserID()
                cart.removeFromCart(userID, ISBN)

            elif (c_input == "4"):
                userID = user.getUserID()
                cart.checkOut(userID)

            else:
                print("That's not a menu option. Please try again.")

        ## incorrect menu option
        else:
            print(option)
            print("That's not a menu option. Please try again.")

        print()

def main():
    print("Welcome to the online bookstore!\n")

    initialMenu()

main()
