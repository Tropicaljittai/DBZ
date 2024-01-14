import sqlite3
from datetime import datetime
import tkinter as tk
import bcrypt
class Database:
    def __init__(self,  dbPath):
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.executescript('''
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
                BankHolder TEXT,
                Description TEXT);
                    
            CREATE TABLE IF NOT EXISTS FinancialDetails (
                FinancialID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                Date CURRENT_TIMESTAMP,
                Balance REAL,
                Revenue REAL,
                Expenses REAL,
                Budget REAL,
                FOREIGN KEY (UserID) REFERENCES Users(UserID));
                    
            CREATE TABLE IF NOT EXISTS ExternalUsers (
                ExternalUserID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                Name TEXT NOT NULL,
                ContactNumber TEXT,
                Email TEXT,
                Address TEXT,
                BankName TEXT,
                BankNumber TEXT,
                BankHolder TEXT,
                IsSupplier INTEGER,
                FOREIGN KEY (UserID) REFERENCES Users(UserID));

            CREATE TABLE IF NOT EXISTS Products (
                ProductId INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                ProductName TEXT NOT NULL,
                ProductLabel TEXT,
                DefaultPrice REAL, 
                FOREIGN KEY (UserID) REFERENCES Users(UserID));
        
            CREATE TABLE IF NOT EXISTS Variants (
                VariantId INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductId INTEGER NOT NULL,
                Variant TEXT,
                Size TEXT,
                Stock INTEGER,
                ComingStock INTEGER,
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

        self.conn.commit()

    def get_current_date(self):
        # Get the current date
        now = datetime.now()
        # Format the date as a string (e.g., "2023-03-21")
        formatted_date = now.strftime("%Y-%m-%d")
        return formatted_date
    
    def insert_user(self,Name, Password,  BusinessType,Email,Address): #signup
        if BusinessType == "Seller":
            BusinessType = 0
        else:
            BusinessType = 1

        RegistrationDate = self.get_current_date()
        self.cursor.execute('INSERT INTO Users (CompanyName,PasswordHash ,IsSupplier ,EmailAddress ,Address ,RegistrationDate) VALUES (?, ?, ?, ?, ?, ?)', ( Name, Password,  BusinessType,Email,Address,RegistrationDate ))
        self.conn.commit()

    def initializeFinancial_details(self, UserID):
        try:
         
            self.cursor.execute("SELECT COUNT(*) FROM FinancialDetails")
            row_count = self.cursor.fetchone()[0]
            date = datetime.now()

            if row_count == 0:
              
                self.cursor.execute("INSERT INTO FinancialDetails (UserID,Date,Balance,Revenue,Expenses,Budget) VALUES (?,?,?,?,?,?)", (UserID,date,0,0,0,0))
                self.conn.commit()
            else:
    
                self.cursor.execute("SELECT 1 FROM FinancialDetails WHERE UserID = ?", (UserID,))
                row_exists = self.cursor.fetchone() is not None

                if not row_exists:
                    self.cursor.execute("INSERT INTO FinancialDetails (UserID,Date,Balance,Revenue,Expenses,Budget) VALUES (?,?,?,?,?,?)", (UserID,date,0,0,0,0))
                    self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing financial details: {e}")

        
    def updateFinancial_details(self,UserID,Balance,Budget):
        Date = datetime.now()
        self.cursor.execute("SELECT Revenue,Expenses FROM FinancialDetails WHERE UserID = ? ORDER BY Date DESC LIMIT 1",(UserID,))
        Rev_Exp = self.cursor.fetchone()
        Revenue,Expenses = Rev_Exp
        self.cursor.execute("INSERT INTO FinancialDetails (UserID, date, Balance,Revenue, Expenses,Budget) VALUES (?,?,?,?,?,?)", (UserID, Date,Balance,Revenue,Expenses,Budget)) 
        self.conn.commit()

    def earn(self, userID, amount):
        date = datetime.now()
        current_financials = self.get_financialDetails(userID)

        if current_financials:
            print(f"Current financials before earn: {current_financials}")  # Debugging

            new_revenue = current_financials['Revenue'] + amount
            new_balance = current_financials['Balance'] + amount

            print(f"Earn method called for userID {userID} with amount {amount}.")  # Debugging
            print(f"New revenue: {new_revenue}, New balance: {new_balance}")  # Debugging

            self.cursor.execute(
                "INSERT INTO FinancialDetails (UserID, Date, Balance, Revenue, Expenses, Budget) VALUES (?, ?, ?, ?, ?, ?)",
                (userID, date, new_balance, new_revenue, current_financials['Expenses'], current_financials['Budget'])
            )
            self.conn.commit()
        else:
            print("Error: No current financial details found for user.")


    def spend(self, userID, amount):
        date = datetime.now()
        current_financials = self.get_financialDetails(userID)

        if amount> current_financials['Budget']:
            message = "Budget Limit Exceeded!!!"
            
            return tk.messagebox.showwarning("Error", message)
        else:
            new_expenses = current_financials['Expenses'] + amount
            new_balance = current_financials['Balance'] - amount
            new_budget = current_financials['Budget'] - amount


        self.cursor.execute(
            "INSERT INTO FinancialDetails (UserID, Date, Balance, Revenue, Expenses, Budget) VALUES (?, ?, ?, ?, ?, ?)",
            (userID, date, new_balance, current_financials['Revenue'], new_expenses, new_budget)
        )
        self.conn.commit()


    def updateUser_details(self,UserID,CompanyName,IsSupplier,EmailAddress,ContactNumber ,BankName,BankNumber, BankHolder,Description):
        
        update = f"UPDATE Users SET CompanyName=?, IsSupplier=?, EmailAddress=?, ContactNumber=?, BankName=?, BankNumber=?, BankHolder=?, Description=? WHERE UserID=?"

        self.cursor.execute(update, (CompanyName,IsSupplier,EmailAddress,ContactNumber ,BankName,BankNumber, BankHolder,Description, UserID))
        self.conn.commit()


    def get_financialDetails(self,userId):
        self.cursor.execute("SELECT FinancialID, Date, Balance,Revenue,Expenses,Budget FROM FinancialDetails WHERE UserID = ? ORDER BY Date DESC LIMIT 1",(userId,))
        financialDetails = self.cursor.fetchone()
        FinancialID,Date,Balance, Revenue ,Expenses , Budget = financialDetails 
        financialInfo = {
            "FinancialID":FinancialID,
            "Date":Date,
            "Balance":Balance,
            "Revenue":Revenue,
            "Expenses":Expenses,
            "Budget":Budget
        }
        return financialInfo


    
    def getUser_fromEmail(self, email):
   
        self.cursor.execute('SELECT UserID, CompanyName, PasswordHash, IsSupplier, EmailAddress, Address, ContactNumber, BankName, BankNumber, BankHolder, Description FROM Users WHERE EmailAddress = ?', (email,))
        user_data1 = self.cursor.fetchone()
        

        if user_data1:
            userId, company_name, PasswordHash, is_supplier, email_address, address, contact, bankName, bankNumber, accountHolder,Description= user_data1

            user_info = {
                'UserID': userId,
                'CompanyName': company_name,
                'PasswordHash':PasswordHash,
                'IsSupplier': bool(is_supplier), 
                'EmailAddress': email_address,
                'Address': address,
                "Contact":contact,
                "BankName": bankName,
                "BankNumber":bankNumber,
                "AccountHolder":accountHolder,
                "Description":Description

            }
            return user_info
        else:
            return None
        
    def getUser_fromId(self,id):
        self.cursor.execute('SELECT UserID, CompanyName, PasswordHash, IsSupplier, EmailAddress, Address, ContactNumber, BankName, BankNumber, BankHolder, Description FROM Users WHERE UserID = ?', (id,))
        user_data1 = self.cursor.fetchone()
        

        if user_data1:
            UserID, company_name, PasswordHash, is_supplier, email_address, address, contact, bankName, bankNumber, accountHolder,Description= user_data1

            user_info = {
                'UserID': UserID,
                'CompanyName': company_name,
                'PasswordHash':PasswordHash,
                'IsSupplier': bool(is_supplier), 
                'EmailAddress': email_address,
                'Address': address,
                "Contact":contact,
                "BankName": bankName,
                "BankNumber":bankNumber,
                "AccountHolder":accountHolder,
                "Description":Description

            }
            return user_info
        else:
            return None
        
        
    def email_exists(self,email):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE EmailAddress = ? LIMIT 1)", (email,))
        exists = self.cursor.fetchone()[0]
        return exists == 1
    

    
    # def getUser_products(self, userId):
    #     self.cursor.execute('SELECT UserID, CompanyName, PasswordHash, IsSupplier, EmailAddress, Address, ContactNumber, BankName, BankNumber, BankHolder, Description FROM Users WHERE EmailAddress = ?', (email,))
    #     user_data1 = self.cursor.fetchone()
        

    
    def addProducts(self, userId, name, label, price):
        try:
            self.cursor.execute("INSERT INTO Products (UserID, ProductName, ProductLabel, DefaultPrice) VALUES (?, ?, ?, ?)", (userId, name, label, price))
            self.conn.commit()

            # Get the last inserted row ID
            self.cursor.execute("SELECT last_insert_rowid()")
            row_id = self.cursor.fetchone()[0]

            return row_id
        except sqlite3.Error as e:
            print(f"Error adding product: {e}")
            return None


    def fetch_products(self,userId):
        print(f"Fetching products for user ID: {userId}")
        self.cursor.execute('SELECT ProductId, ProductName, ProductLabel, DefaultPrice FROM Products WHERE UserID =?', (userId,))
        products = self.cursor.fetchall()
        print(f"Fetched products: {products}")
        return products
    
    
    def fetch_productID_fromName(self, name):
        self.cursor.execute('SELECT ProductId FROM Products WHERE ProductName =?', (name,))
        result = self.cursor.fetchone()
        if result:
            product_id, = result
            return product_id
        else:
            return None
        
    def fetchProductName(self,productId):
        self.cursor.execute('SELECT ProductName FROM Products WHERE ProductId =?', (productId,))
        result = self.cursor.fetchone()
        if result:
            productname, = result
            return productname
        else:
            return None

    
    def fetch_productsVariants(self,productId):
        self.cursor.execute('SELECT VariantId ,Variant,Size ,Stock , ComingStock, AdditionalPrice ,Description FROM Variants WHERE ProductId =?', (productId,))
        Products = self.cursor.fetchall()
        return Products
    
    
    def addProductVariant(self,productId,ComingStock,Variant,Size ,Stock ,AdditionalPrice ,Description):
        self.cursor.execute("INSERT INTO Variants (ProductId, ComingStock ,Variant,Size ,Stock ,AdditionalPrice ,Description) VALUES (?,?,?,?,?,?,?)", (productId,ComingStock ,Variant,Size ,Stock ,AdditionalPrice ,Description)) 
        self.conn.commit()
    
    
    
    def getProduct_namefromVariantId(self, variantId):
        self.cursor.execute('SELECT ProductId FROM Variants WHERE VariantId = ?', (variantId,))
        data = self.cursor.fetchone()

        if data is not None:
            product_id, = data

            self.cursor.execute('SELECT ProductName FROM Products WHERE ProductId = ?', (product_id,))
            product_name = self.cursor.fetchone()

            if product_name is not None:
                return product_name[0]
            else:
                return "Unknown Product"

        return "Unknown Product"

        

    
    def productId_exists(self,id):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM Products WHERE ProductId = ? LIMIT 1)", (id,))
        exists = self.cursor.fetchone()[0]
        return exists == 1
    def variantId_exists(self,id):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM Variants WHERE VariantId = ? LIMIT 1)", (id,))
        exists = self.cursor.fetchone()[0]
        return exists == 1
    
    def getProductId_fromVariantId(self, variantId):
        self.cursor.execute('SELECT ProductId FROM Variants WHERE VariantId = ?', (variantId,))
        data = self.cursor.fetchone()

        if data is not None:
            return data[0]
        else:
            return None

    def deleteProduct(self, product_id):
        try:
            # Get the list of variant IDs associated with the product
            self.cursor.execute('SELECT VariantId FROM Variants WHERE ProductId = ?', (product_id,))
            variant_ids = [row[0] for row in self.cursor.fetchall()]

            # Delete the variants associated with the product
            self.cursor.execute('DELETE FROM Variants WHERE ProductId = ?', (product_id,))
            self.conn.commit()

            # Delete the product itself
            self.cursor.execute('DELETE FROM Products WHERE ProductId = ?', (product_id,))
            self.conn.commit()

            print(f"Product with ProductID {product_id} deleted successfully.")

            # Delete the associated variant records from OrderItems
            for variant_id in variant_ids:
                self.cursor.execute('DELETE FROM OrderItems WHERE VariantId = ?', (variant_id,))
                self.conn.commit()

            print(f"Associated variants and OrderItems deleted successfully.")
        except sqlite3.Error as e:
            print(f"Error deleting product: {e}")

    def fetchVariantID(self, product_id, variant_name, size):
        self.cursor.execute('SELECT VariantId FROM Variants WHERE ProductId = ? AND Variant = ? AND Size = ?', (product_id, variant_name, size))
        result = self.cursor.fetchone()
        if result:
            variant_id, = result
            return variant_id
        else:
            return None

    
    def calculateTotal_Price(self, productId, variantId):
        self.cursor.execute('SELECT DefaultPrice FROM Products WHERE ProductId = ?', (productId,))
        default = self.cursor.fetchone()[0]  # Use fetchone()[0] to get the value directly

        self.cursor.execute('SELECT AdditionalPrice FROM Variants WHERE VariantId = ?', (variantId,))
        additional = self.cursor.fetchone()[0]  # Use fetchone()[0] to get the value directly

        return float(additional) + float(default)
    


    def addCustomer(self,userId,name,num,Email,address,bankname,banknum,bankhold):
        IsSupplier = 0
        self.cursor.execute("INSERT INTO ExternalUsers (UserID,Name, ContactNumber, Email, Address, BankName, BankNumber, BankHolder,IsSupplier ) VALUES (?,?,?,?,?,?,?,?,?)", (userId,name,num,Email,address,bankname,banknum,bankhold,IsSupplier)) 
        self.conn.commit()

    def fetchExternalCust(self,userId):
        self.cursor.execute('SELECT * FROM ExternalUsers WHERE UserID = ? AND IsSupplier = 0', (userId,))
        cust = self.cursor.fetchall()

        return cust
    
    def fetchExternalSupp(self,userId):
        self.cursor.execute('SELECT * FROM ExternalUsers WHERE UserID = ? AND IsSupplier = 1', (userId,))
        supp = self.cursor.fetchall()

        return supp
    
    def fetchExternalUser_fromName(self, name):
        query = 'SELECT * FROM ExternalUsers WHERE Name = ?'
        self.cursor.execute(query, (name,))
        user_data = self.cursor.fetchone()

        if user_data:
            external_user_id, user_id, name, contact_number, email, address, bank_name, bank_number, bank_holder, is_supplier = user_data

            # Replace None values with empty strings or other placeholders
            contact_number = contact_number or ""
            email = email or ""
            address = address or ""
            bank_name = bank_name or ""
            bank_number = bank_number or ""
            bank_holder = bank_holder or ""

            return {
                "external_user_id": external_user_id,
                "user_id": user_id,
                "name": name,
                "contact_number": contact_number,
                "email": email,
                "address": address,
                "bank_name": bank_name,
                "bank_number": bank_number,
                "bank_holder": bank_holder,
                "is_supplier": is_supplier
            }
        else:
            return None


    def fetchExternalCustNameId(self, userId):
        self.cursor.execute('SELECT ExternalUserID, Name FROM ExternalUsers WHERE UserID = ? AND IsSupplier = 0', (userId,))
        cust_data = self.cursor.fetchall()

        # Create a list of strings in the "id-name" format
        customers = [f"{external_user_id}-{customer_name}" for external_user_id, customer_name in cust_data]

        return customers
    
    def fetchExternalName(self, id):
        self.cursor.execute('SELECT Name FROM ExternalUsers WHERE ExternalUserID = ?', (id,))
        cust_data = self.cursor.fetchone()
        
        if cust_data:
            return cust_data[0]  # Extract the first element of the tuple
        else:
            return None




    
    def getVariantName(self, variantId):
        self.cursor.execute('SELECT Variant FROM Variants WHERE VariantId = ?', (variantId,))
        result = self.cursor.fetchone()

        if result:
            return result[0]  # Extract the variant value from the result
        else:
            return None


        return name
    def fetch_orders(self,userId):
        self.cursor.execute('SELECT * FROM Orders WHERE ReceivingUserID = ?',(userId,))

        orders = self.cursor.fetchall()
        return orders
    
    
    def fetch_supplyOrders(self,userId):
        self.cursor.execute('SELECT * FROM Orders WHERE InitiatingUserID = ?',(userId,))

        orders = self.cursor.fetchall()
        return orders

    
    def reduceStock(self, variantId, quantity):
        

       
        self.cursor.execute('SELECT Stock, ComingStock FROM Variants WHERE VariantId = ?', (variantId,))
        current_stock, coming_stock = self.cursor.fetchone()

        # Check if there is enough stock to reduce
        if int(current_stock) + int(coming_stock) < int(quantity):
            print("Insufficient stock.")
            return

   
        if int(current_stock) >= int(quantity):
           
            new_stock = int(current_stock) - int(quantity)
            self.cursor.execute('UPDATE Variants SET Stock = ? WHERE VariantId = ?', (new_stock, variantId))
        else:
            # If current stock is not enough, reduce both current stock and coming stock
            remaining_quantity = int(quantity) - int(current_stock)
            new_stock = 0
            new_coming_stock = int(coming_stock) - int(remaining_quantity)
            self.cursor.execute('UPDATE Variants SET Stock = ?, ComingStock = ? WHERE VariantId = ?', (new_stock, new_coming_stock, variantId))

        self.conn.commit()
        print(f"Stock for Variant ID {variantId} reduced by {quantity}.")




        
    def insertOrder(self, order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type):
        self.cursor.execute('''
            INSERT INTO Orders (OrderType, InitiatingUserID, ReceivingUserID, ExternalUserID, OrderDate, EstimatedArrival, TotalPrice, ShippingStatus, IsPaid, PaymentType)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type))
        self.conn.commit()

        # Fetch the last inserted order_id
        self.cursor.execute('SELECT last_insert_rowid()')
        order_id = self.cursor.fetchone()[0]
        if shipping_status == 'Shipped':
            self.handle_shipped_status(order_id)
        elif shipping_status == 'Received':
            self.handle_received_status(order_id)

        return order_id
        

    def insertOrderItem(self, order_id, variant_id, quantity, price_per_item):
        self.cursor.execute('''
            INSERT INTO OrderItems (OrderID, VariantId, Quantity, PricePerItem)
            VALUES (?, ?, ?, ?)
        ''', (order_id, variant_id, quantity, price_per_item))
        self.conn.commit()

    def fetch_Orderitems(self, OrderID):
        self.cursor.execute('''
            SELECT OrderItemID, VariantId, Quantity, PricePerItem
            FROM OrderItems
            WHERE OrderID = ?
        ''', (OrderID,))

        order_items = self.cursor.fetchall()
        return order_items
    
    
    def fetchSize(self, variantId):
        self.cursor.execute('SELECT Size FROM Variants WHERE VariantId = ?', (variantId,))
        size = self.cursor.fetchone()

        if size:
            return size[0]  # Extract the size value from the result
        else:
            return None
        

    def updateorderstatus(self, order_id, new_shipment_status, new_eta, new_is_paid):
        try:
            # Assume 'orders' is your orders table
            update_query = "UPDATE orders SET IsPaid=?, ShippingStatus=?, EstimatedArrival=? WHERE OrderID=?"
            update_data = (new_is_paid, new_shipment_status, new_eta, order_id)

            # Execute the update query
            self.cursor.execute(update_query, update_data)

            # Commit the changes
            self.conn.commit()
        
          


            print(f"Order status updated successfully for Order ID: {order_id}")
        except Exception as e:
            # Handle exceptions (e.g., print an error message)
            print(f"Error updating order status: {str(e)}")

    def insertSupplier(self,userId,name,contactnum,bankname,banknum,bankholder,address):
        isSupplier= 1

        self.cursor.execute('''
            INSERT INTO ExternalUsers (UserID, Name, ContactNumber, BankName,
                BankNumber ,
                BankHolder ,
                IsSupplier,Address)
            VALUES (?, ?, ?, ?,?,?,?,?)
        ''', (userId,name,contactnum,bankname,banknum,bankholder,isSupplier,address))
        self.conn.commit()

        self.cursor.execute('SELECT last_insert_rowid()')
        id = self.cursor.fetchone()[0]
        return id
    
    def getExternalUserName(self,variantId):
        self.cursor.execute('SELECT Name FROM ExternalUsers WHERE ExternalUserID = ?', (variantId,))
        name = self.cursor.fetchone()
        return name
    
    def getSupplierData(self, user_data):
            if user_data:
                user_id, company_name, password_hash, is_supplier, email_address, contact, address,RegistrationDate , bank_name, bank_number, account_holder, description = user_data

                return {
                    "UserID": user_id,
                    "CompanyName": company_name,
                    "PasswordHash": password_hash,
                    "IsSupplier": is_supplier,
                    "EmailAddress": email_address,
                    "Address": address,
                    "Contact": contact,
                    "BankName": bank_name,
                    "BankNumber": bank_number,
                    "AccountHolder": account_holder,
                    "Description": description
                }
            

            else:
                return None


    def getAll_suppliers(self):
        IsSupplier = 1
        self.cursor.execute('SELECT * FROM Users WHERE IsSupplier = ?', (IsSupplier,))

        suppliers_data = self.cursor.fetchall()
        return suppliers_data
 

    def acceptOrder(self, orderid):
        try:
            update_query = "UPDATE Orders SET ExternalUserID=? WHERE OrderID=?"
            self.cursor.execute(update_query, (0, orderid))
            self.conn.commit()
            print(f"Accepting order with ID: {orderid}")
        except Exception as e:
            print(f"Error accepting order: {str(e)}")
            

    def deleteOrder(self,id):
       
        self.cursor.execute('DELETE FROM Orders WHERE OrderID = ?', (id,))
        self.conn.commit()

    def getInitiatingUserId(self, order_id):
        self.cursor.execute('SELECT InitiatingUserID FROM Orders WHERE OrderID = ?', (order_id,))
        initiating_user_id = self.cursor.fetchone()
        return initiating_user_id[0] if initiating_user_id else None
    
    def update_coming_stock(self, variant_id, new_coming_stock):
        try:
            # Check if the variant ID exists
            if not self.variantId_exists(variant_id):
                print(f"Variant ID {variant_id} does not exist.")
                return

            # Get the current ComingStock value
            current_coming_stock = self.get_current_coming_stock(variant_id)

            # Calculate the new ComingStock value by adding the new_coming_stock to the current value
            updated_coming_stock = current_coming_stock + new_coming_stock

            # Update the ComingStock field for the specified variant
            update_query = "UPDATE Variants SET ComingStock = ? WHERE VariantId = ?"
            self.cursor.execute(update_query, (updated_coming_stock, variant_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating coming stock: {e}")

        
    

    def get_current_coming_stock(self, variant_id):
        try:
            # Retrieve the current ComingStock value
            select_query = "SELECT ComingStock FROM Variants WHERE VariantId = ?"
            self.cursor.execute(select_query, (variant_id,))
            current_coming_stock = self.cursor.fetchone()

            # If the variant exists, return the current ComingStock value, otherwise return 0
            return current_coming_stock[0] if current_coming_stock else 0
        except sqlite3.Error as e:
            print(f"Error getting current coming stock for Variant ID {variant_id}: {e}")
            return 0
        
    def get_current_stock(self, variant_id):
        # Fetch and return the current stock for a given variant_id
        query = "SELECT Stock FROM Variants WHERE VariantId = ?"
        self.cursor.execute(query, (variant_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0
    
    

    def update_stock(self, variant_id, quantity):
        # Update the current stock for a given variant_id
        current_stock = self.get_current_stock(variant_id)
        new_stock = current_stock + quantity

        query = "UPDATE Variants SET Stock = ? WHERE VariantId = ?"
        self.cursor.execute(query, (new_stock, variant_id))
        self.conn.commit()


        
    def updateOrder(self, order_id, order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type):
        try:
            # Assume 'orders' is your orders table
            update_query = "UPDATE Orders SET OrderType=?, InitiatingUserID=?, ReceivingUserID=?, ExternalUserID=?, OrderDate=?, EstimatedArrival=?, TotalPrice=?, ShippingStatus=?, IsPaid=?, PaymentType=? WHERE OrderID=?"
            update_data = (order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type, order_id)

            # Execute the update query
            self.cursor.execute(update_query, update_data)

            # Commit the changes
            self.conn.commit()

            print(f"Order updated successfully for Order ID: {order_id}")
        except Exception as e:
            # Handle exceptions (e.g., print an error message)
            print(f"Error updating order: {str(e)}")

    def updateOrderItem(self, order_id, variant_id, quantity, price_per_item):
        try:
            # Assume 'order_items' is your order items table
            update_query = "UPDATE OrderItems SET VariantId=?, Quantity=?, PricePerItem=? WHERE OrderID=?"
            update_data = (variant_id, quantity, price_per_item, order_id)

            # Execute the update query
            self.cursor.execute(update_query, update_data)

            # Commit the changes
            self.conn.commit()

            print(f"Order item updated successfully for Order ID: {order_id}")
        except Exception as e:
            # Handle exceptions (e.g., print an error message)
            print(f"Error updating order item: {str(e)}")
    def get_order_status(self, order_id):
        self.cursor.execute('SELECT ShippingStatus FROM Orders WHERE OrderID = ?', (order_id,))
        status = self.cursor.fetchone()
        return status[0] if status else None

    def get_order_total_price(self, order_id):
        self.cursor.execute('SELECT TotalPrice FROM Orders WHERE OrderID = ?', (order_id,))
        total_price = self.cursor.fetchone()
        return total_price[0] if total_price else 0

    def get_order_user_id(self, order_id):
        self.cursor.execute('SELECT InitiatingUserID FROM Orders WHERE OrderID = ?', (order_id,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def reduce_user_balance(self, user_id, amount):
        financial_details = self.get_financialDetails(user_id)
        if financial_details:
            new_balance = financial_details['Balance'] - amount
            self.updateFinancial_details(user_id, new_balance, financial_details['Budget'])

    # Add this method to your Database class
    def move_from_coming_to_stock(self, variant_id, quantity):
        try:
            print(f"Moving from coming stock to stock for Variant ID {variant_id} with Quantity {quantity}")
            
            # Retrieve the current ComingStock and Stock values
            query_select = "SELECT ComingStock, Stock FROM Variants WHERE VariantId = ?"
            self.cursor.execute(query_select, (variant_id,))
            result = self.cursor.fetchone()

            if result:
                coming_stock, current_stock = result
                print(f"Current coming stock: {coming_stock}, Current stock: {current_stock}")

                # Check if there's enough coming stock to move
                if coming_stock >= quantity:
                    # Update ComingStock and Stock
                    new_coming_stock = coming_stock - quantity
                    new_stock = current_stock + quantity
                    query_update = "UPDATE Variants SET ComingStock = ?, Stock = ? WHERE VariantId = ?"
                    self.cursor.execute(query_update, (new_coming_stock, new_stock, variant_id))
                    self.conn.commit()
                    print(f"Updated: New coming stock: {new_coming_stock}, New stock: {new_stock}")
                else:
                    print(f"Not enough coming stock for Variant ID {variant_id}")
            else:
                print(f"No record found for Variant ID {variant_id}")
        except sqlite3.Error as e:
            print(f"Error in move_from_coming_to_stock: {e}")

   
               
    def update_order_status(self, order_id, new_status):
        try:
            current_status = self.get_order_status(order_id)
            self.cursor.execute("UPDATE Orders SET ShippingStatus=? WHERE OrderID=?", (new_status, order_id))
            self.conn.commit()

            print(f"Updating order status to {new_status} for Order ID: {order_id}")

            if new_status == 'Shipped' and current_status != 'Shipped':
                self.handle_shipped_status(order_id)
            elif new_status == 'Received' and current_status != 'Received':
                self.handle_received_status(order_id)

        except Exception as e:
            print(f"Error updating order status: {str(e)}")


        


    def handle_shipped_status(self, order_id):
        print(f"Handling shipped status for Order ID: {order_id}")
        order_items = self.fetch_Orderitems(order_id)
        for item in order_items:
            _, variant_id, quantity, _ = item
            print(f"Increasing coming stock for Variant ID {variant_id} by {quantity}")
            if self.variantId_exists(variant_id):
                self.update_coming_stock(variant_id, quantity)
            else:
                print(f"Variant ID {variant_id} does not exist in the database.")

    def handle_received_status(self, order_id):
        print(f"Handling received status for Order ID: {order_id}")
        order_items = self.fetch_Orderitems(order_id)
        for item in order_items:
            _, variant_id, quantity, _ = item
            print(f"Moving stock from coming to current for Variant ID {variant_id} by {quantity}")
            if self.variantId_exists(variant_id):
                self.move_from_coming_to_stock(variant_id, quantity)
            else:
                print(f"Variant ID {variant_id} does not exist in the database.")

    # ... other existing methods ...

 

    def get_variant_size(self, variant_id):
   

        query = "SELECT Size FROM Variants WHERE VariantId = ?"
        self.cursor.execute(query, (variant_id,))
        result = self.cursor.fetchone()

        if result:
            return result[0]
        else:
            return None


    def get_initiating_user_id(self, order_id):
        try:
            self.cursor.execute('SELECT InitiatingUserID FROM Orders WHERE OrderID = ?', (order_id,))
            result = self.cursor.fetchone()
            if result is not None:
                return result[0]  # InitiatingUserID
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error getting initiating user ID: {e}")
            return None

    def fetchVariantDetails(self, variantId):

        self.cursor.execute('''
            SELECT Variant, Size
            FROM Variants
            WHERE VariantId = ?
        ''', (variantId,))
        result = self.cursor.fetchone()
        if result:
            variant_name, size = result
            return f"{variantId} - {variant_name} - {size}"  # Format: "Variant - Size"
        else:
            return "Unknown Variant"
        
   

    

    