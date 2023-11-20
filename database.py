import sqlite3

def create_table():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            id TEXT PRIMARY KEY,
            ProductName TEXT,
            ProductLabel TEXT,
            ProductStatus TEXT,
            ProductStock INTEGER,
            SupplierId TEXT,
            Sales INTEGER,
            FOREIGN KEY (SupplierId) REFERENCES Supplier(SupplierId))''')
    connect.commit
    connect.close

def fetch_products():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Products')
    Products = cursor.fetchall()
    connect.close()
    return Products



def insert_product(id, ProductName, ProductLabel, ProductStatus, ProductStock, SupplierId):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Products (id, ProductName, ProductLabel, ProductStatus, ProductStock, SupplierId) VALUES (?, ?, ?, ?, ?, ?)', (id, ProductName, ProductLabel, ProductStatus, ProductStock, SupplierId))
    connect.commit()
    connect.close()

def delete_products(id):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Products WHERE id = ?', (id,))
    connect.commit()
    connect.close()

def update_products(id, ProductName, ProductLabel, ProductStatus, ProductStock, SupplierId):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Products SET ProductName = ?, ProductLabel = ?, ProductStatus = ?, ProductStock = ?, SupplierId = ? WHERE id = ?", (ProductName, ProductLabel, ProductStatus, ProductStock, SupplierId, id))
    connect.commit()
    connect.close()

def id_exists(id):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Products WHERE id = ?', (id,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

def create_supplier():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Supplier (
            SupplierId TEXT PRIMARY KEY,
            SupplierName TEXT,
            InvoiceNum INTEGER,
            SupplierContact INTEGER,
            Description TEXT)''')
    connect.commit
    connect.close

def fetch_supplier():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM Supplier')
    Products = cursor.fetchall()
    connect.close()
    return Products

def fetch_supplier_ids():
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT SupplierId, SupplierName FROM Supplier')
    Products = cursor.fetchall()
    connect.close()
    return Products

def insert_supplier(SupplierId, SupplierName, InvoiceNum, SupplierContact, Description):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Supplier (SupplierId, SupplierName, InvoiceNum, SupplierContact, Description) VALUES (?, ?, ?, ?, ?)', (SupplierId, SupplierName, InvoiceNum, SupplierContact, Description))
    connect.commit()
    connect.close()

def delete_supplier(SupplierId):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('DELETE FROM Supplier WHERE SupplierId = ?', (SupplierId,))
    connect.commit()
    connect.close()
    
def update_supplier(SupplierId, SupplierName, InvoiceNum, SupplierContact, Description):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Supplier SET SupplierName = ?, InvoiceNum = ?, SupplierContact = ?, Description = ? WHERE SupplierId = ?", (SupplierName, InvoiceNum, SupplierContact, Description, SupplierId))
    connect.commit()
    connect.close()

def SupplierId_exists(SupplierId):
    connect = sqlite3.connect('Products.db')
    cursor = connect.cursor()
    cursor.execute('SELECT COUNT(*) FROM Supplier WHERE SupplierId = ?', (SupplierId,))
    result = cursor.fetchone()
    connect.close()
    return result[0] > 0

create_table()
create_supplier()