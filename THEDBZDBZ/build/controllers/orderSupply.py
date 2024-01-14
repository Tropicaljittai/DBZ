import tkinter as tk
from datetime import datetime,timedelta
from tkinter import ttk
class orderSupply_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["orderSupply"]
        self.onSecondTree = False
        
        self.model.auth.add_event_listener(
            "selectSupplier", self.selectedSupp_listener
        )
        self.frame.tree.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.frame.tree2.bind("<ButtonRelease-1>",self.on_second_treeview_click)
        self._bind()

    def _bind(self):
        self.frame.backbutton_3.configure(command=self.back)
        self.frame.updatebutton_11.config(command=self.update)
        self.frame.delbutton_1.config(command=self.delete)
        self.frame.createOrderbutton_3.config(command=self.createOrder)
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



    def selectedSupp_listener(self,data=None):
        self.update_backVisibility()
        print("selectedSupp_listener called")
        selectedSupplier = self.model.auth.selectedSupp
        print(f"Selected Supplier: {selectedSupplier}")
        if selectedSupplier:
            id= selectedSupplier["UserID"]
            name = selectedSupplier["CompanyName"]
            address = selectedSupplier["Address"]
            desc = selectedSupplier["Description"]
            contact = selectedSupplier["Contact"]
            email = selectedSupplier["EmailAddress"]
            
            self.frame.addressDets.config(text=str(address))
            self.frame.contactDets.config(text=str(contact))
            self.frame.emailDets.config(text=str(email))
            self.frame.suppDesc.config(text=str(desc))
            self.frame.suppName.config(text=str(name))

            print("UI elements updated successfully")
        products = self.model.database.fetch_products(selectedSupplier["UserID"])
        self.frame.tree.delete(*self.frame.tree.get_children())

        for product in products:
            _, product_name, product_label, default_price, *_ = product
            self.frame.tree.insert('', "end", values=(product_name, product_label, default_price))

        self.populate_treeview()

    def update_backVisibility(self):
        if self.onSecondTree:
            self.frame.backbutton_3.place(x=1324.0, y=96.0, width=91.0, height=30.0)
        else:
            self.frame.backbutton_3.place_forget()
            
    def populate_treeview(self):
        currentSupp = self.model.auth.selectedSupp
        products = self.model.database.fetch_products(currentSupp["UserID"])
        print(f"Fetched products: {products}")
        self.frame.tree.delete(*self.frame.tree.get_children())

        for product in products:
            _, product_name, product_label, default_price, *_ = product
            self.frame.tree.insert('', "end", values=(product_name, product_label, default_price))

    # def populate_treeview(self):
            
    def on_treeview_click(self, event):
    
        for col in self.frame.tree["columns"]:
            self.frame.tree.heading(col, text="")

        item = self.frame.tree.item(self.frame.tree.selection())
        product_name = item['values'][0] if item['values'] else None

        if product_name and not self.isOn_Variantstreeview():
            self.go_variantsTree(product_name)

    def update_treeview_columns(self, new_columns):
 
        for col in self.frame.tree["columns"]:
            self.frame.tree.heading(col, text="")
        self.frame.tree["columns"] = ()

        self.frame.tree["columns"] = new_columns
        for col in new_columns:
            self.frame.tree.heading(col, text=col)

       
        for col in new_columns:
            self.frame.tree.column(col, anchor=tk.CENTER, width=100)

    def go_variantsTree(self, product_name):
        self.onSecondTree = True
        self.update_backVisibility()
        self.frame.tree.delete(*self.frame.tree.get_children())
        product_id = self.model.database.fetch_productID_fromName(product_name)  # Replace with actual method to get product_id
        variantsData = self.model.database.fetch_productsVariants(product_id)
        columns = ["Id","Variant","Size","Stock","Total Price"]
        self.update_treeview_columns(columns)

        self.frame.tree.unbind("<ButtonRelease-1>")

        for i in variantsData:
            variantId,variant, size, stock, _,_,*_ = i
            total = self.model.database.calculateTotal_Price(product_id,variantId)
            self.frame.tree.insert('', "end", values=(variantId,variant, size, stock,total))
        self.frame.tree.bind("<ButtonRelease-1>", self.on_second_treeview_click)

    def on_second_treeview_click(self, event):
        self.frame.qtyentry_1.delete(0, 'end')
        selectedItem = self.frame.tree.item(self.frame.tree.selection())
        self.frame.qtyentry_1.insert(0,0)
        if selectedItem:
            selectedValues = selectedItem['values']
            self.frame.addbutton_10.config(command=lambda: self.insert_selected_id(selectedValues))

    def isOn_Variantstreeview(self):
        # Check if the current treeview columns match those of the second treeview
        return self.frame.tree["columns"] == ["Id","Variant", "Size", "Stock", "Total Price"]
    
    # def displayItem(self,product_id):
    def back(self):
        self.onSecondTree = False
        self.update_backVisibility()
        columns = ["Name", "Description", "Price"]
        self.update_treeview_columns(columns)
        self.frame.tree.unbind("<ButtonRelease-1>")
        self.frame.tree.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.populate_treeview()

    def insert_selected_id(self,selectedValues):
        
        if int(selectedValues[3])>0:
            variantId= selectedValues[0]
            variant = selectedValues[1]
            size = selectedValues[2]
            productId = self.model.database.getProductId_fromVariantId(variantId)
            productName = self.model.database.fetchProductName(productId)
            qty = self.frame.qtyentry_1.get()

            if int(qty)<=int(selectedValues[3]):
                price = float(qty)*float(selectedValues[4])
                self.frame.tree2.insert("", "end", values=(variantId, productName ,variant, size,qty,price))
                self.sumPrice()
                
            else:
                message = "not enough stock!"
                tk.messagebox.showwarning("Error", message)

            
        else:
            message = "not enough stock!"
            tk.messagebox.showwarning("Error", message)
    def sumPrice(self):
  
        # total_sum = sum(float(i[5].get()) for i in self.frame.tree2)
      
        total_sum=0.0

        for item_id in self.frame.tree2.get_children():
            values = self.frame.tree2.item(item_id, 'values')
            if values and values[5]:
                total_sum += float(values[5])

        self.frame.sum.config(text=f"Rp. {total_sum}")

    def delete(self):
        selected_item = self.frame.tree2.selection()
        if selected_item:
            self.frame.tree2.delete(selected_item)

    def update(self):
    # Get the selected item in the treeview
        selected_item = self.frame.tree2.selection()

        if selected_item:

            current_values = self.frame.tree2.item(selected_item, 'values')


            if current_values and current_values[4]:
          
                new_qty = self.frame.qtyentry_1.get()

             
                if new_qty:
                
                    unitPrice = float(current_values[5]) / float(current_values[4])

                    newPrice = float(new_qty) * unitPrice

                    # Update the quantity and total price in the treeview
                    self.frame.tree2.item(selected_item, values=(current_values[0], current_values[1], current_values[2], current_values[3], new_qty, newPrice))

                    # Update the total price accordingly
                    self.sumPrice()

    def createOrder(self):
        
        # Get necessary details for creating an order
        
       
        total_price = self.sumPrice()
        payment_type = self.frame.pay_combobox.get()
       
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Insert order into the database
        order_id = self.model.database.insertOrder(
        order_type="Supply",
        initiating_user_id=self.model.auth.current_user["UserID"],
        receiving_user_id=self.model.auth.selectedSupp["UserID"],
        external_user_id=None,
        order_date=order_date,
        estimated_arrival=None,
        total_price=total_price,
        shipping_status="Pending",
        is_paid=0,
        payment_type=payment_type
    )

        # Insert order items into the database for each row in tree2
        for item_id in self.frame.tree2.get_children():
            values = self.frame.tree2.item(item_id, 'values')
            if values:
                variant_id, product_name, variant, size, qty, price = values
                # Assuming you have a method to get the product ID from the variant ID
                product_id = self.model.database.getProductId_fromVariantId(variant_id)
                theprice = float(price)/float(qty)
                # Insert order item into the database
                self.model.database.insertOrderItem(
                    order_id=order_id,
                    variant_id=variant_id,
                    quantity=qty,
                    price_per_item=theprice
                )
                self.model.database.reduceStock(variant_id, qty)

        self.model.auth.order_created() 

        self.view.switch("supply")

    
       
        
       