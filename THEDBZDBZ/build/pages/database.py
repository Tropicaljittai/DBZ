import sqlite3
from datetime import datetime

def create_table():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            CompanyName TEXT UNIQUE NOT NULL,
            PasswordHash TEXT NOT NULL,
            IsSupplier INTEGER,
            EmailAddress TEXT UNIQUE NOT NULL,
            ContactNumber TEXT,
            Address TEXT,
            RegistrationDate DATE NOT NULL,
            BankName TEXT,
            BankNumber TEXT, 
            BankHolder TEXT);
                   
        CREATE TABLE IF NOT EXISTS FinancialDetails (
            FinancialID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER,
            Date DATE,
            Balance REAL,
            Revenue REAL,
            Expenses REAL,
            Budget REAL,
            FOREIGN KEY (UserID) REFERENCES Users(UserID));
                   
        CREATE TABLE IF NOT EXISTS ExternalUsers (
            ExternalUserID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            ContactNumber TEXT,
            Address TEXT,
            BankName TEXT,
            BankNumber TEXT,
            BankHolder TEXT);

        CREATE TABLE IF NOT EXISTS Products (
            ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ProductName TEXT NOT NULL,
            ProductLabel TEXT,
            DefaultPrice REAL, 
            FOREIGN KEY (UserID) REFERENCES Users(UserID));
    
        CREATE TABLE IF NOT EXISTS Variants (
            VariantId TEXT PRIMARY KEY,
            ProductId INTEGER NOT NULL,
            Variant TEXT,
            Size TEXT,
            Stock INTEGER,
            AdditionalPrice REAL,
            Description TEXT,
            FOREIGN KEY (ProductId) REFERENCES Products(ProductId));
        
        CREATE TABLE IF NOT EXISTS Orders (
            OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderType TEXT,
            InitiatingUserID INTEGER,
            ReceivingUserID INTEGER,
            ExternalUserID INTEGER,
            OrderDate DATE,
            EstimatedArrival DATE,
            TotalPrice REAL,
            ShippingStatus TEXT,
            ShippingAddress TEXT,
            InvoiceNum INTEGER,
            IsPaid INTEGER,
            PaymentType TEXT,
            FOREIGN KEY (InitiatingUserID) REFERENCES Users(UserID),
            FOREIGN KEY (ReceivingUserID) REFERENCES Users(UserID),
            FOREIGN KEY (ExternalUserID) REFERENCES ExternalUsers(ExternalUserID));
        
        CREATE TABLE IF NOT EXISTS OrderItems (
            OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderID INTEGER,
            VariantId TEXT,
            Quantity INTEGER,
            PricePerItem REAL,
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
            FOREIGN KEY (VariantId) REFERENCES Variants(VariantID));
    ''')

    connect.commit()
    connect.close()
def get_current_date():
    # Get the current date
    now = datetime.now()
    # Format the date as a string (e.g., "2023-03-21")
    formatted_date = now.strftime("%Y-%m-%d")
    return formatted_date
def insert_user(Name, Password,  BusinessType,Email,ContactNumber,Address,BankName ,BankNumber, BankHolder):
    connect = sqlite3.connect('Products.db')
    if BusinessType == "Seller":
        BusinessType = 0
    else:
        BusinessType = 1

    RegistrationDate = get_current_date()
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Users (CompanyName,PasswordHash ,IsSupplier ,EmailAddress ,ContactNumber ,Address ,RegistrationDate ,BankName ,BankNumber , BankHolder ) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?,?)', ( Name, Password,  BusinessType,Email,ContactNumber,Address,RegistrationDate ,BankName ,BankNumber, BankHolder))
    connect.commit()
    connect.close()      

def email_exists(email):
    connect = sqlite3.connect('Products.db') 
    cursor = connect.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE EmailAddress = ? LIMIT 1)", (email,))
    exists = cursor.fetchone()[0]
    connect.close()
    return exists == 1

create_table()