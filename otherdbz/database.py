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
            ShippedStock INTEGER,
            RecievedStock INTEGER,
            OnHandStock INTEGER,
            AdditionalPrice REAL,
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
    cursor.execute('INSERT INTO Products (id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, ProductName, ProductStock, ShippedStock, RecievedStock, OnHandStock, Description, SupplierId, Price, Cost))
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

def count_variants():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Variants')
    Products = cursor.fetchone()
    connect.close()
    return Products

def fetch_variants():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Variants')
    Products = cursor.fetchall()
    connect.close()
    return Products

def insert_variants(VariantId, ProductId, Variant, Size, ShippedStock, RecievedStock, OnHandStock, AdditionalPrice):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Variants (VariantId, ProductId, Variant, Size, ShippedStock, RecievedStock, OnHandStock, AdditionalPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (VariantId, ProductId, Variant, Size, ShippedStock, RecievedStock, OnHandStock, AdditionalPrice))
    connect.commit()
    connect.close()

def delete_variants(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Variants WHERE VariantId = ?', (id,))
    connect.commit()
    connect.close()

def update_variants(VariantId, Variant, Size, ShippedStock, RecievedStock, OnHandStock, AdditionalPrice):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Variants SET Variant = ?, Size = ?, ShippedStock = ?, RecievedStock = ?, OnHandStock = ?, AdditionalPrice = ? WHERE VariantId = ?", (Variant, Size, ShippedStock, RecievedStock, OnHandStock, AdditionalPrice, VariantId))
    connect.commit()
    connect.close()

def id_exists_variants(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Variants WHERE VariantId = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def check_stock_sum_update(product_id, variant_id, shipped_stock, received_stock, onhand_stock):
    # Connect to the SQLite database (change 'your_database.db' to your actual database file)
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    try:
        # Execute the SQL query to get the sum of columns in Variants table
        cursor.execute(f"SELECT IFNULL(SUM(ShippedStock) , 0) + {shipped_stock}, IFNULL(SUM(RecievedStock), 0) + {received_stock}, IFNULL(SUM(OnHandStock), 0) + {onhand_stock} FROM Variants WHERE ProductId = {product_id} AND VariantId != {variant_id}")
        variants_sum = cursor.fetchone()

        # Execute the SQL query to get the sum of columns in Products table for the specified ProductId
        cursor.execute(f"SELECT IFNULL(SUM(ShippedStock), 0), IFNULL(SUM(RecievedStock), 0), IFNULL(SUM(OnHandStock), 0) FROM Products WHERE id = {product_id}")
        products_sum = cursor.fetchone()
        
        # Check if the sum in Variants is greater than the sum in Products
        for i in range(len(variants_sum)):
            if variants_sum[i] > products_sum[i]: 
                return False
            else:
                return True

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        connection.close()

def check_stock_sum(product_id, shipped_stock, received_stock, onhand_stock):
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    try:
        # Execute the SQL query to get the sum of columns in Variants table
        cursor.execute(f"SELECT SUM(ShippedStock) + {shipped_stock}, SUM(RecievedStock) + {received_stock}, SUM(OnHandStock) + {onhand_stock} FROM Variants WHERE ProductId = {product_id}")
        variants_sum = cursor.fetchone()

        # Execute the SQL query to get the sum of columns in Products table for the specified ProductId
        cursor.execute(f"SELECT SUM(ShippedStock), SUM(RecievedStock), SUM(OnHandStock) FROM Products WHERE id = {product_id}")
        products_sum = cursor.fetchone()

        # Check if the sum in Variants is greater than the sum in Products
        for i in range(len(variants_sum)):
            if variants_sum[i] > products_sum[i]: 
                return False
            else:
                return True

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        # Close the database connection
        connection.close()


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
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT,  
            ItemQuantity INTEGER,
            PaymentStatus TEXT,
            ShipmentStatus TEXT,
            OrderDate TEXT,
            OrderTotal INTEGER,
            PaymentType TEXT,
            CustomerId TEXT,
            FOREIGN KEY (CustomerId) REFERENCES Customer(id))''')
    connect.commit()
    connect.close()

def fetch_orders():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Orders')
    Products = cursor.fetchall()
    connect.close()
    return Products

def insert_orders(ItemQuantity, PaymentStatus, ShipmentStatus, OrderDate, OrderTotal, PaymentType, CustomerId):
    try:
        connect = sqlite3.connect('Data.db')
        cursor = connect.cursor()

        cursor.execute('INSERT INTO Orders (ItemQuantity, PaymentStatus, ShipmentStatus, OrderDate, OrderTotal, PaymentType, CustomerId) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                       (ItemQuantity, PaymentStatus, ShipmentStatus, OrderDate, OrderTotal, PaymentType, CustomerId))
        
        order_id = cursor.lastrowid  # Get the last inserted id
        connect.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        connect.close()

    return order_id

def delete_orders(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Orders WHERE OrderId = ?', (id))
    connect.commit()
    connect.close()

def update_orderStatus(orderId, PaymentStatus,ShipmentStatus):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Orders SET PaymentStatus = ?, ShipmentStatus = ?, WHERE OrderId = ?", (orderId, PaymentStatus, ShipmentStatus))
    connect.commit()
    connect.close()

def id_exists_order(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Orders WHERE OrderId = ?', (id))
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

def get_isPaid(orderId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    try:
        cursor.execute('SELECT PaymentStatus FROM Orders WHERE orderId = ?', (orderId,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None  

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        connect.close()

def get_customer_name_by_id(customer_id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    try:
        cursor.execute('SELECT name FROM Customer WHERE id = ?', (customer_id,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        connect.close()

def get_shipStat(orderId):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    try:
        cursor.execute('SELECT ShipmentStatus FROM orders WHERE id = ?', (orderId,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None 

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        connect.close()

        

def fetch_customer_address(customer_id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()

    try:
        cursor.execute('SELECT address FROM Customer WHERE id = ?', (customer_id,))
        result = cursor.fetchone()

        if result:
            return result[0] 
        else:
            return None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

    finally:
        connect.close()


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
        CREATE TABLE IF NOT EXISTS OrderDetails(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            OrderId INTEGER,
            ProductId TEXT,
            Quantity INTEGER,
            FOREIGN KEY (OrderId) REFERENCES Orders(OrderId)
            FOREIGN KEY (ProductId) REFERENCES Products(id))''')
    connect.commit
    connect.close

def count_orders():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Orders')
    Orders = cursor.fetchone()
    connect.close()
    return Orders
    
def count_details():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM OrderDetails')
    Orders = cursor.fetchone()
    connect.close()
    return Orders


def fetch_details():
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM OrderDetails')
    Products = cursor.fetchall()
    connect.close()
    return Products


def insert_details(OrderId, ProductId, Quantity):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO OrderDetails (OrderId, ProductId, Quantity) VALUES (?, ?, ?)', (OrderId, ProductId, Quantity))
    connect.commit()
    connect.close()

def delete_details(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM OrderDetails WHERE Id = ?', (id,))
    connect.commit()
    connect.close()

# def update_details(OrderId, ProductId, Quantity):
#     connect = sqlite3.connect('Data.db')
#     cursor = connect.cursor()
#     cursor.execute("UPDATE OrderDetails SET Quantity = ?, TotalCost = ? WHERE id = ? AND ProductId = ?", ( Quantity, TotalCost, OrderId, ProductId))
#     connect.commit()
#     connect.close()

def id_exists_details(id):
    connect = sqlite3.connect('Data.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM OrderDetails WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def get_highest_product_id():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(id) FROM Products")
    
    highest_product_id = cursor.fetchone()[0]

    if highest_product_id is None:
        connection.close()
        return 0
    
    connection.close()
    return highest_product_id

def get_highest_variant_id():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(VariantId) FROM Variants")
    
    highest_variant_id = cursor.fetchone()[0]

    if highest_variant_id is None:
        connection.close()
        return 0
    
    connection.close()
    return int(highest_variant_id)

def get_highest_customer_id():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(id) FROM Customer")
    
    highest_product_id = cursor.fetchone()[0]

    if highest_product_id is None:
        connection.close()
        return 0
    
    connection.close()
    return int(highest_product_id)

def get_highest_supplier_id():
    connection = sqlite3.connect('Data.db')
    cursor = connection.cursor()

    cursor.execute("SELECT MAX(SupplierId) FROM Supplier")
    
    highest_product_id = cursor.fetchone()[0]

    if highest_product_id is None:
        connection.close()
        return 0
    
    connection.close()
    return int(highest_product_id)

create_table()
create_supplier()
create_customer()
create_orders()
create_details()


        