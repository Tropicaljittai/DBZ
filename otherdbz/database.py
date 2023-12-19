import sqlite3

def create_table():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id TEXT PRIMARY KEY,
            ProductName TEXT,
            ProductStock INTEGER,
            ShippedStock INTEGER,
            RecievedStock INTEGER,
            OnHandStock INTEGER,
            Description TEXT,
            SupplierId TEXT,
            Price INTEGER,
            Cost INTEGER,
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId))''')
    
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

        CREATE TABLE IF NOT EXISTS Variants (
            VariantId TEXT PRIMARY KEY,
            ProductId INTEGER NOT NULL,
            Variant TEXT,
            Size TEXT,
            Stock INTEGER,
            AdditionalPrice REAL,
            Description TEXT,
            FOREIGN KEY (ProductId) REFERENCES Products(ProductId));
    ''')

    connect.commit()
    connect.close()

def fetch_stocks(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT ProductStock FROM Products WHERE id = ?', (id,))
    Products = cursor.fetchone()
    connect.close()
    return Products

def fetch_for_home():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT id, ProductName, Price FROM Products')
    Products = cursor.fetchall()
    connect.close()
    return Products

def fetchPOS(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT ProductName, Price, ProductStock FROM Products WHERE id = ?', (id,))
    Products = cursor.fetchall()
    connect.close()
    return Products

def count_product():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Products')
    Products = cursor.fetchone()
    connect.close()
    return Products

def fetch_products():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Products')
    Products = cursor.fetchall()
    connect.close()
    return Products


def insert_product(id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Products (id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price))
    connect.commit()
    connect.close()

def delete_products(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Products WHERE id = ?', (id,))
    connect.commit()
    connect.close()

def update_products(id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Products SET ProductName = ?, ProductStock = ?, ShippedStock = ?, RecievedStock = ?, OnHandStock = ?, Description = ?, SupplierId = ?, Price = ?, Cost = ? WHERE id = ?", (ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost, id))
    connect.commit()
    connect.close()

def id_exists(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Products WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def create_supplier():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId TEXT PRIMARY KEY,
            SupplierName TEXT,
            InvoiceNum INTEGER,
            SupplierEmail TEXT,
            SupplierBankNum INTEGER,
            SupplierBankName TEXT,
            SupplierAccountHolder TEXT,
            Description TEXT)''')
    connect.commit
    connect.close

def fetch_supplier():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Supplier')
    Products = cursor.fetchall()
    connect.close()
    return Products

def fetch_supplier_ids():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT SupplierId, SupplierName FROM Supplier')
    Products = cursor.fetchall()
    connect.close()
    return Products

def insert_supplier(SupplierId, SupplierName, InvoiceNum, SupplierEmail, SupplierBankNum, SupplierBankName, SupplierAccountHolder, Description):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Supplier (SupplierId, SupplierName, InvoiceNum, SupplierEmail, SupplierBankNum, SupplierBankName, SupplierAccountHolder, Description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (SupplierId, SupplierName, InvoiceNum, SupplierEmail, SupplierBankNum, SupplierBankName, SupplierAccountHolder, Description))
    connect.commit()
    connect.close()

def delete_supplier(SupplierId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Supplier WHERE SupplierId = ?', (SupplierId,))
    connect.commit()
    connect.close()
    
def update_supplier(SupplierId, SupplierName, InvoiceNum, SupplierEmail, SupplierBankNum, SupplierBankName, SupplierAccountHolder, Description):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Supplier SET SupplierName = ?, InvoiceNum = ?, SupplierEmail = ?, SupplierBankNum = ?, SupplierBankName = ?, SupplierAccountHolder = ?, Description = ? WHERE SupplierId = ?", (SupplierName, InvoiceNum, SupplierEmail, SupplierBankNum, SupplierBankName, SupplierAccountHolder, Description, SupplierId))
    connect.commit()
    connect.close()

def SupplierId_exists(SupplierId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Supplier WHERE SupplierId = ?', (SupplierId,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def create_orders():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            OrderId TEXT PRIMARY KEY,  
            OrderQuantity INTEGER,
            OrderStatus TEXT,
            OrderDate TEXT,
            OrderTotal INTEGER,
            InvoiceNum INTEGER,
            PaymentType TEXT,
            Pay INTEGER,
            Due INTEGER,
            CustomerId TEXT,
            FOREIGN KEY (CustomerId) REFERENCES Customer(id))''')
    connect.commit
    connect.close

def fetch_orders():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Orders')
    Products = cursor.fetchall()
    connect.close()
    return Products

def insert_orders(id, OrderQuantity, OrderStatus, OrderDate, OrderTotal, InvoiceNum, PaymentType, Pay, Due, CustomerId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Orders (id, OrderQuantity, OrderStatus, OrderDate, OrderTotal, InvoiceNum, PaymentType, Pay, Due, CustomerId) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, OrderQuantity, OrderStatus, OrderDate, OrderTotal, InvoiceNum, PaymentType, Pay, Due, CustomerId))
    connect.commit()
    connect.close()

def delete_orders(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Orders WHERE id = ?', (id,))
    connect.commit()
    connect.close()

def update_orders(id, OrderQuantity, OrderStatus, OrderTotal, InvoiceNum, PaymentType, Pay, Due, CustomerId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Orders SET OrderQuantity = ?, OrderStatus = ?, OrderTotal = ?, InvoiceNum = ?, PaymentType = ?, Pay = ?, Due = ?, CustomerId = ? WHERE OrderId = ?", ( OrderQuantity, OrderStatus, OrderTotal, InvoiceNum, PaymentType, Pay, Due, CustomerId, id))
    connect.commit()
    connect.close()

def id_exists_order(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Orders WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def create_customer():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone INTEGER,
            address TEXT,
            bankName TEXT,
            accNum INTEGER,
            account_holder TEXT)''')
    connect.commit
    connect.close

def fetch_customer():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Customer')
    Products = cursor.fetchall()
    connect.close()
    return Products

def fetch_customer_ids():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT id, name FROM Customer')
    Products = cursor.fetchall()
    connect.close()
    return Products


def insert_Customer(id, name, email, phone, address, bankName, accNum, account_holder):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Customer (id, name, email, phone, address, bankName, accNum, account_holder) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (id, name, email, phone, address, bankName, accNum, account_holder))
    connect.commit()
    connect.close()

def delete_Customer(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Customer WHERE id = ?', (id,))
    connect.commit()
    connect.close()

def update_Customer(id, name, email, phone, address, bankName, accNum, account_holder):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Customer SET  name = ?, email = ?, phone = ?, address = ?, bankName = ?, accNum = ?, account_holder = ? WHERE id = ?", (name, email, phone, address, bankName, accNum, account_holder, id))
    connect.commit()
    connect.close()

def id_exists_customer(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Customer WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def create_details():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS OrderDetails (
            OrderId TEXT PRIMARY KEY,
            ProductId TEXT,
            Quantity INTEGER,
            TotalCost INTEGER,
            FOREIGN KEY (OrderId) REFERENCES Orders(OrderId)
            FOREIGN KEY (ProductId) REFERENCES Products(id))''')
    connect.commit
    connect.close
 
def fetch_details():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM OrderDetails')
    Products = cursor.fetchall()
    connect.close()
    return Products



def insert_details(OrderId, ProductId, Quantity, TotalCost):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO OrderDetails (OrderId, ProductId, Quantity, TotalCost) VALUES (?, ?, ?, ?)', (OrderId, ProductId, Quantity, TotalCost))
    connect.commit()
    connect.close()

def delete_details(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM OrderDetails WHERE OrderId = ?', (id,))
    connect.commit()
    connect.close()

def update_details(OrderId, ProductId, Quantity, TotalCost):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE OrderDetails SET Quantity = ?, TotalCost = ? WHERE id = ? AND ProductId = ?", ( Quantity, TotalCost, OrderId, ProductId))
    connect.commit()
    connect.close()

def id_exists_details(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM OrderDetails WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

create_table()
create_supplier()
create_customer()
create_orders()
create_details()