from datetime import datetime, timedelta
from tkinter import ttk
import tkinter as tk


class supplyController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["supply"]
        self._bind()
    
        self.model.auth.add_event_listener("order_created", self.order_created_listener)
    

    def _bind(self):
        self.frame.orderbutton_3.config(command = self.add)
        self.frame.tree.bind('<ButtonRelease>', self.display_data)
        self.frame.updatebutton_6.config(command = self.update)
        self.frame.orderbutton_2.config(command = self.searchSupplier)
    

    def order_created_listener(self, data):
        self.populateTreeView()
    
    def searchSupplier(self):
        self.view.switch("searchSupplier")

    def go_to_details(self):
        self.view.switch("accountDetails")
    def go_to_cust(self):
        self.view.switch("customers")
    def go_to_products(self):
        self.view.switch("products")
    def goToDash(self):
        self.view.switch("dashboard")
    def goToOrder(self):
        self.view.switch("orders")
    def goToSupply(self):
        self.view.switch("supply")

    def createComboBox(self):

        self.product_combobox = ttk.Combobox(self.frame)
        self.product_combobox.place(x=1030, y=530, width=110, height=20)
        self.product_combobox.set("Select Product") 
        self.product_combobox.bind("<<ComboboxSelected>>", self.populateVariantComboBox)

        self.variant_combobox = ttk.Combobox(self.frame)
        self.variant_combobox.place(x=1208, y=530, width=110, height=20)
        self.variant_combobox.set("Select Variant")  

        self.ship_combobox = ttk.Combobox(self.frame, values=["Pending","Shipped","Received"])

        self.ship_combobox.place(x=1030, y=600, width=110, height=20)

     
        self.populateProductComboBox()

    def populateProductComboBox(self):
        user_products = self.model.database.fetch_products(self.model.auth.current_user["UserID"])


        product_names = [product[1] for product in user_products]
        self.product_combobox["values"] = product_names

    def populateVariantComboBox(self, event):
        product_name = self.product_combobox.get()

        # Fetch the product ID based on the selected product name
        product_id = self.model.database.fetch_productID_fromName(product_name)

        if product_id:
            # Fetch variants for the selected product ID
            variants = self.model.database.fetch_productsVariants(product_id)

            if variants:
                # Clear existing values in the variant_combobox
                self.variant_combobox.set("")  # Clear current selection
                self.variant_combobox["values"] = []  # Clear current values

                # Populate the variant_combobox with variant details
                variant_details = [f"{variant[0]} - {variant[1]} - {variant[2]}" for variant in variants]
                self.variant_combobox["values"] = variant_details
            else:
                # If no variants found, clear the variant_combobox
                self.variant_combobox.set("No Variants Available")
                self.variant_combobox["values"] = []
        else:
            # If no product selected, clear the variant_combobox
            self.variant_combobox.set("Select Product First")
            self.variant_combobox["values"] = []


    
 
         



    def add(self):
        # Get values from entry fields and combo boxes
        product_name = self.product_combobox.get()
        variant_info = self.variant_combobox.get()
        parts = variant_info.split(" - ")
        variant_name = parts[1]

        quantity = self.frame.qtyentry_9.get()
        price = self.frame.supplyPriceentry_11.get()
        etadays = self.frame.etaentry_10.get()
        shipment_status = self.ship_combobox.get()
        bankname = self.frame.banknameentry_2.get()

        supplierName = self.frame.supplierNameentry_3.get()
        bankNum = self.frame.banknumentry_5.get()

        accountHolder = self.frame.accountholderentry_7.get()
        contact = self.frame.contactentry_8.get()
        address = self.frame.addressentry_6.get()

        userId = self.model.auth.current_user["UserID"]

        # Validate input
        if not product_name or not variant_name or not quantity or not price or not etadays or not shipment_status:
            tk.messagebox.showerror("Error", "All fields must be filled.")
            return

        # Fetch necessary IDs
        variantId = parts[0]

        # Calculate total price
        total_price = float(quantity) * float(price)

        date = datetime.now()
        current_datetime = datetime.now()
        eta = current_datetime + timedelta(days=int(etadays))
        theEta = eta.date()

        userId = self.model.auth.current_user["UserID"]
        current_financials = self.model.database.get_financialDetails(userId)

        if total_price> current_financials['Budget']:
            message = "Budget Limit Exceeded!!!"
            
            return tk.messagebox.showwarning("Error", message)
        else:
             # Insert the order
            order_id = self.model.database.insertOrder(
                "Supply",
                self.model.auth.current_user["UserID"],
                None,
                self.model.database.insertSupplier(
                    userId, supplierName, contact, bankname, bankNum, accountHolder, address
                ),
                date,
                theEta,
                total_price,
                shipment_status,
                0,
                None,
            )

            self.model.database.insertOrderItem(order_id, variantId, quantity, price)

            

            variant_size = self.model.database.get_variant_size(variantId)

            

            if not product_name or not variant_name or not variant_size or not quantity or not price or not etadays or not shipment_status:
                tk.messagebox.showerror("Error", "All fields must be filled.")
                return

            # Deduct the total price from the user's balance
            self.model.database.spend(userId, total_price)

            # Display the added values in the TreeView

        

            # Debug print statements
            print(f"Added order: ID={order_id}, Product={product_name}, Variant={variant_name}, Quantity={quantity}, Price={price}")

            # Display the added values in the TreeView
         
            
            self.populateTreeView()

       



      
    


    
    
    def populateTreeView(self):
     

        print("Populating TreeView...")
        orders = self.model.database.fetch_supplyOrders(self.model.auth.current_user["UserID"])
        self.frame.tree.delete(*self.frame.tree.get_children())  # Clear existing items
        orders.reverse()

           
        for order in orders:
            # Extract order information
            order_id, order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type = order

            # Fetch additional information related to the order
            order_items = self.model.database.fetch_Orderitems(order_id)

            if order_type == "Supply":
                for order_item in self.model.database.fetch_Orderitems(order_id):
                    orderitem_id, variant_id, quantity, price_per_item = order_item

                    product_name = self.model.database.getProduct_namefromVariantId(variant_id)
                    variant_name = self.model.database.getVariantName(variant_id)
                    variant_size = self.model.database.get_variant_size(variant_id)  # Ensure this fetches the correct size

    
                    supplierName = self.model.database.getExternalUserName(external_user_id)

                    user_data = self.model.database.getUser_fromId(receiving_user_id)
                    if user_data:
                        userSupplier = user_data["CompanyName"]
                    else:
                        userSupplier = "N/A" 

                    if supplierName == None:
                        supplierName = userSupplier
                        
                    # Display order item information in the TreeView
                    self.frame.tree.insert('', "end", values=(order_id, product_name, variant_name, variant_size, supplierName, quantity, price_per_item, estimated_arrival, shipping_status))

            

    def clear(self):
        entries = [self.frame.supplierNameentry_3,
                self.frame.qtyentry_9,
                self.frame.supplyPriceentry_11,
                self.frame.etaentry_10,
                self.frame.banknameentry_2,
                self.frame.banknumentry_5,
                self.frame.accountholderentry_7,
                self.frame.contactentry_8,
                self.frame.addressentry_6,
            ]
        
        for entry in entries:
            entry.delete(0, 'end')
        
    
    def display_data(self, event):
        selected_item = self.frame.tree.focus()
        

        if selected_item:
            order_id = self.frame.tree.item(selected_item)['values'][0]
            orderItems = self.model.database.fetch_Orderitems(order_id)
            for orderItem in orderItems:
                OrderItemID, variantID, quantity, price_per_item = orderItem
            row = self.frame.tree.item(selected_item)['values']
            self.clear()
            self.product_combobox.set(row[1])
            variant_info = self.model.database.fetchVariantDetails(variantID)  # Display ID, Variant, and Size
            self.variant_combobox.set(variant_info)
            self.frame.supplierNameentry_3.insert(0, row[4])
            self.frame.qtyentry_9.insert(0, row[5])
            self.frame.supplyPriceentry_11.insert(0, row[6])

            # Calculate the difference in days between ETA and today
            eta_date = datetime.strptime(row[7], "%Y-%m-%d").date()
            today_date = datetime.now().date()
            days_difference = (eta_date - today_date).days
            self.frame.etaentry_10.insert(0, days_difference)  # Automatically set the length in days

            self.ship_combobox.set(row[8])

            name = self.frame.supplierNameentry_3.get()
            self.frame.banknameentry_2.insert(0, self.model.database.fetchExternalUser_fromName(name)["bank_name"])
            self.frame.banknumentry_5.insert(0, self.model.database.fetchExternalUser_fromName(name)["bank_number"])
            self.frame.accountholderentry_7.insert(0, self.model.database.fetchExternalUser_fromName(name)["bank_holder"])
            self.frame.contactentry_8.insert(0, self.model.database.fetchExternalUser_fromName(name)["contact_number"])
            self.frame.addressentry_6.insert(0, self.model.database.fetchExternalUser_fromName(name)["address"])

              
                





                
            
            

    def update(self):
        selected_item = self.frame.tree.focus()
        if selected_item:
            order_id = self.frame.tree.item(selected_item)['values'][0]
            new_shipment_status = self.ship_combobox.get()
            print(f"Debug: Updating order {order_id} with new status: {new_shipment_status}")

            self.model.database.update_order_status(order_id, new_shipment_status )
            
        
        # Debug print statements
        print(f"Debug: product_combobox.get() = {self.product_combobox.get()}")
        print(f"Debug: variant_combobox.get() = {self.variant_combobox.get()}")
        
        # Get values from entry fields and combo boxes
        product_name = self.product_combobox.get()
        full_variant_info = self.variant_combobox.get()
        
        # Extract variant name without size
        variant_name = full_variant_info.split(" - ")[1] if " - " in full_variant_info else full_variant_info
        variant_id = full_variant_info.split(" - ")[0] if " - " in full_variant_info else full_variant_info
        
        quantity = self.frame.qtyentry_9.get()
        price = self.frame.supplyPriceentry_11.get()
        etadays = self.frame.etaentry_10.get()
        shipment_status = self.ship_combobox.get()
        bankname = self.frame.banknameentry_2.get()
        supplierName = self.frame.supplierNameentry_3.get()
        bankNum = self.frame.banknumentry_5.get()
        accountHolder = self.frame.accountholderentry_7.get()
        contact = self.frame.contactentry_8.get()
        address = self.frame.addressentry_6.get()

        # Print additional debug information
        print(f"Debug: Selected Product and Variant - Product={product_name}, Variant={variant_name}")

        # Validate input
        if not product_name or not variant_name or not quantity or not price or not etadays or not shipment_status:
            tk.messagebox.showerror("Error", "All fields must be filled.")
            return
            

        # Fetch necessary IDs
        product_id = self.model.database.fetch_productID_fromName(product_name)
    

        # Calculate total price
        total_price = float(quantity) * float(price)

        date = datetime.now()
        current_datetime = datetime.now()
        eta = current_datetime + timedelta(days=int(etadays))
        theEta = eta.date()

        user =self.model.auth.current_user
        userId = user["UserID"]
        # Update the order
        selected_item = self.frame.tree.focus() 
      

        if selected_item:
            total_quantity=0
            theOrderPrice = 0
            order_id = self.frame.tree.item(selected_item)['values'][0]
            orderItems = self.model.database.fetch_Orderitems(order_id)

            self.model.database.updateOrder(order_id, "Supply", self.model.auth.current_user["UserID"], None,
                                            self.model.database.insertSupplier(userId, supplierName, contact, bankname,
                                                                              bankNum, accountHolder, address),
                                            date, theEta, total_price, shipment_status, 0, None)

          
            print(f"Updated order: ID={order_id}, Product={product_name}, Variant={variant_name}, Quantity={quantity}, Price={price}, ETA={theEta}, Status={shipment_status}")
            self.model.database.updateOrderItem(order_id, variant_id, quantity, price)



            print("Updating TreeView after changes...")
            self.populateTreeView()
        else:
            tk.messagebox.showerror("Error", "Please select an item in the TreeView to update.")



            




