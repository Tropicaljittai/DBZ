from tkinter import ttk
import tkinter as tk
from datetime import datetime, timedelta

class ordersController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["orders"]
        self.onSecondTree = False
        self._bind()

        self.model.auth.add_event_listener("order_created", self.order_created_listener)
        self.frame.tree.bind("<ButtonRelease-1>", lambda event: self.on_treeview_click(event))
        self.frame.tree2.bind("<ButtonRelease-1>", lambda event: self.on_treeview2_click(event))

    def _bind(self):
        self.frame.backbutton_3.config(command=self.back)
        self.frame.newOrderbutton_11.config(command=self.createOrder)
        self.frame.acceptbutton_4.config(command=self.accept)
        self.frame.rejectbutton_5.config(command=self.reject)
        self.frame.supplybutton_7.config(command=self.goToSupply)

    def order_created_listener(self, data):
        self.populate_treeview()

    def createOrder(self):
        self.view.switch("createOrder")
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

    def update_treeview_columns(self, new_columns):
        if self.onSecondTree == True:
            for col in self.frame.tree["columns"]:
                self.frame.tree.heading(col, text="")
        self.frame.tree["columns"] = ()

        # Set up new columns
        self.frame.tree["columns"] = new_columns
        for col in new_columns:
            self.frame.tree.heading(col, text=col)

        # Configure properties of the new columns (adjust as needed)
        for col in new_columns:
            self.frame.tree.column(col, anchor=tk.CENTER, width=100)


    def update_backVisibility(self):
        if self.onSecondTree:
            self.frame.backbutton_3.place(x=903, y=146, width=54, height=16.0)
        else:
            self.frame.backbutton_3.place_forget()



    def populate_treeview(self):
        orders = self.model.database.fetch_orders(self.model.auth.current_user["UserID"])
        orders.reverse()

        self.frame.tree.delete(*self.frame.tree.get_children())
        self.frame.tree2.delete(*self.frame.tree2.get_children())

        for order in orders:
            order_id, order_type, initiating_user_id, receiving_user_id, external_user_id, order_date, estimated_arrival, total_price, shipping_status, is_paid, payment_type = order
            customerName = self.model.database.fetchExternalName(external_user_id)
            if is_paid == 0:
                payment = "Not paid"
            else:
                payment = "paid"
            if external_user_id == 0:
                user = self.model.database.getUser_fromId(initiating_user_id)
                if user:
                    userName = user["CompanyName"]
                else:
                    userName = "N/A"

                self.frame.tree.insert('', "end", values=(order_id, initiating_user_id, userName, payment, shipping_status, estimated_arrival))

            elif external_user_id is None:
                user = self.model.database.getUser_fromId(initiating_user_id)
                if user:
                    userName = user["CompanyName"]
                else:
                    userName = "N/A"
                self.frame.tree2.insert('', "end", values=(order_id, userName, order_date))

            else:
                self.frame.tree.insert('', "end", values=(order_id, external_user_id, customerName, payment, shipping_status, estimated_arrival))

    def on_treeview_click(self, event):
        if self.onSecondTree:
            return  # If already on the second treeview, do nothing

        item = self.frame.tree.item(self.frame.tree.selection())
        orderId = item['values'][0] if item['values'] else None

        if orderId and not self.isOn_itemsview():
            # Clear existing columns only when not on the second treeview
            for col in self.frame.tree["columns"]:
                self.frame.tree.heading(col, text="")

            self.frame.etaentry_1.delete(0, 'end')
            self.frame.etaentry_1.insert(0, "days")

            # Change this line to use lambda
            self.frame.viewbutton_2.config(command=self.go_itemsTree)
            self.frame.updatebutton_1.config(command=self.update)

            payment_status = item['values'][3] if item['values'] else ""
            shipment_status = item['values'][4] if item['values'] else ""
            self.pay_combobox.set(payment_status)
            self.ship_combobox.set(shipment_status)

    def go_itemsTree(self):
        item = self.frame.tree.item(self.frame.tree.selection())
        orderid = item['values'][0] if item['values'] else None

        self.onSecondTree = True
        self.update_backVisibility()
        self.frame.tree.delete(*self.frame.tree.get_children())

        # Add this print statement
        print("Fetching Order Items for Order ID:", orderid)
        orderItems = self.model.database.fetch_Orderitems(orderid)
        print("Fetched Order Items:", orderItems)

        columns = ["VariantId", "Product", "Variant", "Size", "Quantity", "Total Price"]
        self.update_treeview_columns(columns)


    
        self.frame.tree.unbind("<ButtonRelease-1>")

        if not orderItems:
            print("No items found for Order ID:", orderid)

        for orderItem in orderItems:
            OrderItemID, variantID, quantity, price_per_item = orderItem
            total_price = quantity * price_per_item
            productId = self.model.database.getProductId_fromVariantId(variantID)
            productname = self.model.database.fetchProductName(productId)
            size = self.model.database.fetchSize(variantID)
            variant = self.model.database.getVariantName(variantID)
            values = (variantID, productname, variant, size, quantity, total_price)
            print("Inserting into Treeview:", values)
            self.frame.tree.insert('', "end", values=values)

    def accept(self):
        item = self.frame.tree2.item(self.frame.tree2.selection())
        orderId = item['values'][0] if item['values'] else None
        self.model.database.acceptOrder(orderId)
        self.frame.tree2.delete(*self.frame.tree2.get_children())
        self.frame.tree.delete(*self.frame.tree.get_children())
        self.populate_treeview()

    def reject(self):
        item = self.frame.tree2.item(self.frame.tree2.selection())
        orderId = item['values'][0] if item['values'] else None
        self.model.database.deleteOrder(orderId)
        self.populate_treeview()

    def createComboBox(self):
        self.pay_combobox = ttk.Combobox(self.frame, values=["Paid", "Not Paid"])
        self.pay_combobox.place(x=250.0, y=605, width=122, height=38)

        self.ship_combobox = ttk.Combobox(self.frame, values=["Pending", "Shipped", "Received"])
        self.ship_combobox.place(x=520, y=605, width=122, height=38)

    def isOn_itemsview(self):
        # Check if the current treeview columns match those of the second treeview
        return self.frame.tree["columns"] == ["VariantId", "Product", "Variant", "Size", " Quantity", "Total Price"]

    def back(self):
        self.onSecondTree = False
        self.update_backVisibility()
        columns = ["OrderID", "CustomerID", "Name", "PaymentStatus", "ShipmentStatus", "ETA"]
        self.update_treeview_columns(columns)
        self.frame.tree.unbind("<ButtonRelease-1>")
        self.frame.tree.bind("<ButtonRelease-1>", lambda event: self.on_treeview_click(event))
        self.frame.tree2.delete(*self.frame.tree2.get_children())
        self.populate_treeview()

   
    def update(self):
        
        item = self.frame.tree.item(self.frame.tree.selection())
        orderID = item['values'][0] if item['values'] else None
        shipment = self.ship_combobox.get()
        pay = self.pay_combobox.get()

        if pay == "Paid":
            pay = 1
        else:
            pay = 0

        etadays = self.frame.etaentry_1.get()
        current_datetime = datetime.now()
        eta = current_datetime + timedelta(days=int(etadays))
        theEta = eta.date()

        self.model.database.updateorderstatus(orderID, shipment, theEta, pay)
        self.populate_treeview()

        user = self.model.auth.current_user
        userId = user["UserID"]
        orderItems = self.model.database.fetch_Orderitems(orderID)
        initialuser = self.model.database.get_initiating_user_id(orderID)

        total_quantity = 0  # Initialize the total quantity variable
        theOrderPrice = 0

        
        

        for orderItem in orderItems:
            OrderItemID, variantID, quantity, price_per_item = orderItem
            total_quantity += quantity  # Accumulate the quantity

            total_price = price_per_item*quantity
            theOrderPrice += total_price


        if initialuser is None:
            if pay == 1:

                self.model.database.earn(userId, float(theOrderPrice))
            
        else:
            if pay ==1:
                self.model.database.spend(initialuser,float(theOrderPrice))
            


            

        
            

        self.populate_treeview()




    def go_itemsTree2(self):
        item = self.frame.tree2.item(self.frame.tree2.selection())
        order_id = item['values'][0] if item['values'] else None

        self.onSecondTree = True
        self.update_backVisibility()
        self.frame.tree.delete(*self.frame.tree.get_children())

        # Fetch and populate order items for the selected order
        order_items = self.model.database.fetch_Orderitems(order_id)

        columns = ["VariantId", "Product", "Variant", "Size", "Quantity", "Total Price"]
        self.update_treeview_columns(columns)

        if not order_items:
            print("No items found for Order ID:", order_id)
        else:
            for order_item in order_items:
                OrderItemID, variantID, quantity, price_per_item = order_item
                total_price = quantity * price_per_item
                productId = self.model.database.getProductId_fromVariantId(variantID)
                productname = self.model.database.fetchProductName(productId)
                size = self.model.database.fetchSize(variantID)
                variant = self.model.database.getVariantName(variantID)
                values = (variantID, productname, variant, size, quantity, total_price)
                print("Inserting into Treeview:", values)
                self.frame.tree.insert('', "end", values=values)


        self.frame.tree.unbind("<ButtonRelease-1>")

# ...

    def on_treeview2_click(self, event):
        if self.onSecondTree:
            return

        item = self.frame.tree2.item(self.frame.tree2.selection())
        order_id = item['values'][0] if item['values'] else None

        if order_id and not self.isOn_itemsview():
            # Clear existing columns only when not on the second treeview
            for col in self.frame.tree["columns"]:
                self.frame.tree.heading(col, text="")

            self.frame.viewbutton_2.config(command=self.go_itemsTree2)

    # ...

    