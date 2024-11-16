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
        if(option == "2"):
            print("Inventory Menu:") #anticipating other functions
            print("0. View Inventory") #only one done so far
            print()
            i_option = input("Enter your menu choice: ")

            if(i_option == "0"):
                inventory.viewInventory()
                #this will loop back to the main while loop afterwards; may create
                #another while loop just for the inventory menu

        #looking at cart options
        if(option == "3"):
            print("Cart Menu:")
            print("0. Add to Cart")
            print("1. Remove from Cart")
            print("2. Checkout Items in Cart")

            print("Enter your menu choice: " , end = "")
            c_input = input()

            if (c_input == "0"):
                print("Here is the current inventory of books:")
                inventory.viewInventory()
                print("What book (based on ISBN number) would you like to add to your cart: ", end = "")
                ISBN = input()

                print("How many books would you like to add to your cart: ", end = "")
                quantity = int(input())
                userID = user.getUserID()
                cart.addToCart(userID, ISBN, quantity)
            elif (c_input == "1"):
                print("What book (based on ISBN number) would you like to remove from your cart: ", end = "")
                ISBN = input()
                userID = user.getUserID()
                cart.removeFromCart(userID, ISBN)
            elif (c_input == "2"):
                userID = user.getUserID()
                cart.checkOut(userID)

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()


def main():
    print("Welcome to the online bookstore!\n")

    initialMenu()

main()
