import OrderHistory

def main():
    order1 = OrderHistory.OrderHistory(totalAmount=150, customerID=101)
    print("Total Amount: ", order1.getTotalAmount())



if __name__ == "__main__":
    main()