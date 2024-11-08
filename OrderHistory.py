class OrderHistory:
    def __init__(self, totalAmount=0, customerID=0):
        self.__totalAmount = totalAmount
        self.__customerID = customerID

    def __del__(self):
        print(f"OrderHistory for customer {self.__customerID} is being deleted")

    def getTotalAmount(self):
        return self.__totalAmount