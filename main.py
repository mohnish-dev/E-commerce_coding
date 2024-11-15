from OrderHistory import OrderHistory

def main():
    # Create an OrderHistory object with initial values
    order = OrderHistory(totalAmount=100, customerID=1)
    
    # Display the initial order details
    print("Initial order details:")
    order.display()
    
    # Test getTotalAmount and getCustomerID
    print("\nTesting getters:")
    print("Total Amount:", order.getTotalAmount())
    print("Customer ID:", order.getCustomerID())
    
    # Test setTotalAmount and setCustomerID
    print("\nTesting setters:")
    order.setTotalAmount(200)
    order.setCustomerID(2)
    print("Updated order details:")
    order.display()
    
    # Test deleteHistory
    print("\nTesting deleteHistory:")
    order.deleteHistory()
    order.display()

    # Explicitly delete the order object (optional)
    del order
    print("Order object deleted explicitly.")

if __name__ == "__main__":
    main()
