class OrderHistory:
    def __init__(self, totalAmount=0, customerID=0):
        self.__totalAmount = totalAmount
        self.__customerID = customerID

    def __del__(self):
        print(f"OrderHistory for customer {self.__customerID} is being deleted")

    def getTotalAmount(self):
        return self.__totalAmount

    def getCustomerID(self):
        return self.__customerID

    def setTotalAmount(self, totalAmount):
        self.__totalAmount = totalAmount

    def setCustomerID(self, customerID):
        self.__customerID = customerID

    def display(self):
        print(f"Customer ID: {self.__customerID}, Total Amount: {self.__totalAmount}")

    def deleteHistory(self):
        self.__totalAmount = 0
        print("Order history deleted.")
