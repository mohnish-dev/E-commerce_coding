import sqlite3
import sys

## attempts to connect to the database
try:
    connection = sqlite3.connect("methods.db")

    print("Successful connection.")

except:
    print("Failed connection.")

    ## exits the program if unsuccessful
    sys.exit()

## cursor to send queries through
cursor = connection.cursor()
print("\n--------------------------------------------")

## inventory table

print("\nCreating Inventory table...")

inventory = """CREATE TABLE Inventory (
    ISBN varchar(14) NOT NULL,
    Title varchar(50),
    Author varchar(50),
    Genre varchar(50),
    Pages int(4),
    ReleaseDate int(4),
    Price decimal(4,2),
    Stock int(4),
    PRIMARY KEY(ISBN)
);"""

cursor.execute(inventory)
print("Finished creating Inventory table.")
print("\nAdding Inventory records...")

## inventory inserts

query = "INSERT INTO Inventory (ISBN, Title, Author, Genre, Pages, ReleaseDate, Price, Stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
data = [
    ('978-0451524935', '1984', 'George Orwell', 'Dystopian', '328', '1949', '19.99', '12'),
    ('978-0446310789', 'To Kill a Mockingbird', 'Harper Lee', 'Southern Gothic', '281', '1960', '25.00', '100'),
    ('978-0156028356', 'The Color Purple', 'Alice Walker', 'Epistolary', '304', '1982', '15.98', '37'),
    ('978-1400033416', 'Beloved', 'Toni Morrison', 'American Literature', '324', '1987', '20.99', '56'),
    ('978-1501156748', 'Misery', 'Stephen King', 'Psychological Horror', '310', '1987', '9.50', '42'),
    ('978-0312424404', 'Gilead', 'Marilynne Robinson', 'Novel', '256', '2004', '19.99', '39'),
    ('978-0307265432', 'The Road', 'Cormac McCarthy', 'Post apocalyptic fiction', '287', '2006', '15.99', '17'),
]

cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building Inventory table.")
print("\n--------------------------------------------")



## user table

print("\nCreating User table...")

user = """CREATE TABLE User (
    UserID varchar(7) NOT NULL,
    Email varchar(100) NOT NULL UNIQUE,
    Password varchar(100),
    FirstName varchar(50),
    LastName varchar(50),
    Address varchar(100),
    City varchar(50),
    State varchar(2),
    Zip int(5),
    Payment varchar(50),
    PRIMARY KEY(UserID)
);"""

cursor.execute(user)
print("Finished creating User table.")
print("\nAdding User records...")

## user inserts

query = "INSERT INTO User (UserID, Email, Password, FirstName, LastName, Address, City, State, Zip, Payment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
data = [
    ('12-3456', 'muffinman@gmail.com', 'ilikebaking', 'Muffin', 'Man', '12 Drury Lane', 'Starkville', 'MS', '39759', 'PayPal'),
    ('89-3167', 'cookies@aol.com', 'youcantcatchme', 'Gingerbread', 'Man', '63 Gingerbread Cove', 'Memphis', 'TN', '38135', 'Discover'),
    ('90-6720', 'shrek@yahoo.com', 'onions1', 'Shrek', 'Ogre', '901 Swamp Pit Drive', 'Senatobia', 'MS', '38668', 'MasterCard'),
]

cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building User table.")
print("\n--------------------------------------------")




## cart table

print("\nCreating Cart table...")

cart = """CREATE TABLE Cart (
    UserID varchar(7) NOT NULL,
    ISBN varchar(14) NOT NULL,
    Quantity int(3),
    FOREIGN KEY(UserID) REFERENCES User(UserID),
    FOREIGN KEY(ISBN) REFERENCES Inventory(ISBN)
);"""

cursor.execute(cart)
print("Finished creating Cart table.")
print("\nAdding Cart records...")

## cart inserts

query = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
data = [
    ('12-3456', '978-0451524935', '1'),
    ('12-3456', '978-0307265432', '3'),
    ('12-3456', '978-0156028356', '1'),
    ('89-3167', '978-0307265432', '1'),
    ('89-3167', '978-1400033416', '20'),
    ('90-6720', '978-0451524935', '1'),
    ('90-6720', '978-1501156748', '2'),
    ('90-6720', '978-0446310789', '1'),
    ('90-6720', '978-0312424404', '1'),
]

cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building Cart table.")
print("\n--------------------------------------------")




## orders table

print("\nCreating Orders table...")

order = """CREATE TABLE Orders (
    OrderNumber varchar(6) NOT NULL,
    UserID varchar(7) NOT NULL,
    ItemNumber int(5),
    Cost varchar(10),
    Date varchar(25),
    PRIMARY KEY(OrderNumber),
    FOREIGN KEY(UserID) REFERENCES User(UserID)
);"""

cursor.execute(order)
print("Finished creating Orders table.")
print("\nAdding Orders records...")

## orders inserts

query = "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)"
data = [
    ('526848', '12-3456', '2', '$35.97', '4/5/1994'),
    ('547296', '12-3456', '12', '$245.89', '6/17/2006'),
    ('782906', '90-6720', '10', '$206.45', '5/8/2020')
]


cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building Orders table.")
print("\n--------------------------------------------")




## order items table

print("\nCreating OrderItems table...")

order = """CREATE TABLE OrderItems (
    OrderNumber varchar(6) NOT NULL,
    ISBN varchar(14) NOT NULL,
    Quantity int(3),
    FOREIGN KEY(OrderNumber) REFERENCES Orders(OrderNumber),
    FOREIGN KEY(ISBN) REFERENCES Inventory(ISBN)
);"""

cursor.execute(order)
print("Finished creating OrderItems table.")
print("\nAdding OrderItems records...")

## orders inserts

query = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
data = [
    ('526848', '978-0451524935', '1'),
    ('526848', '978-0156028356', '1'),
    ('547296', '978-0312424404', '10'),
    ('547296', '978-0446310789', '1'),
    ('547296', '978-1400033416', '1'),
    ('782906', '978-0451524935', '2'),
    ('782906', '978-0307265432', '1'),
    ('782906', '978-1501156748', '1'),
    ('782906', '978-0156028356', '1'),
    ('782906', '978-0446310789', '5')
]


cursor.executemany(query, data)
connection.commit()

## shows changes
print(cursor.rowcount, "record(s) inserted.")
print("\nFinished building OrderItems table.")
print("\n--------------------------------------------")



## close the cursor and connection once you're done
cursor.close()
connection.close()
