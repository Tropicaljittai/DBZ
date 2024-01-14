from tkinter import ttk
import tkinter as tk
from pathlib import Path
import customtkinter

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
from tkinter import ttk
from datetime import datetime

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Franz\Documents\THEDBZDBZ\build\assets\entries")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
class createOrder_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["createOrder"]
        self.onSecondTree = False
        self.update_backVisibility()
        self.entry_vertical_offset = 200

        self.frame.tree.bind("<ButtonRelease-1>", self.on_treeview_click)
        self.frame.tree2.bind("<ButtonRelease-1>",self.onTreeview2_click)

        # customers = self.fetch_connected_customers()

        
      
        self._bind()

    def _bind(self):
        self.frame.backbutton_3.configure(command=self.back)
        self.frame.invoicebutton_4.config(command=self.createOrder)
        self.frame.arrowbutton_2.config(command=self.goToOrder)
        self.frame.customersbutton_6 .config(command=self.go_to_cust)

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
        
    def update_backVisibility(self):
        if self.onSecondTree:
            self.frame.backbutton_3.place(x=1324.0, y=96.0, width=91.0, height=30.0)
        else:
            self.frame.backbutton_3.place_forget()
        

   

    def populate_treeview(self):
        currentUser = self.model.auth.current_user
        products = self.model.database.fetch_products(currentUser["UserID"])
        self.frame.tree.delete(*self.frame.tree.get_children())

        for product in products:
            _, product_name, product_label, default_price, *_ = product
            self.frame.tree.insert('', "end", values=(product_name, product_label, default_price))

    def on_treeview_click(self, event):
        # Clear existing columns
        for col in self.frame.tree["columns"]:
            self.frame.tree.heading(col, text="")

        item = self.frame.tree.item(self.frame.tree.selection())
        product_name = item['values'][0] if item['values'] else None

        if product_name and not self.isOn_Variantstreeview():
            self.go_variantsTree(product_name)
        # else:


    def update_treeview_columns(self, new_columns):
        # Clear existing columns
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
            self.frame.addbutton_11.config(command=lambda: self.insert_selected_id(selectedValues))

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
       

        
            # self.frame.calculateTotal_Price.delete()
            # self.sum_entry.insert(0, int(total_sum))
            # self.sum_entry.configure(state='readonly')
        
        
    def delete(self):
        selected_item = self.frame.tree2.selection()

        if selected_item:
            # Get the values of the item being deleted
            deleted_values = self.frame.tree2.item(selected_item, 'values')

            # Delete the selected item from the treeview
            self.frame.tree2.delete(selected_item)

            # Recalculate the total sum after deletion
            self.sumPrice()

            # # If you want to reduce the total sum by the deleted item's price, you can do the following:
            # if deleted_values and deleted_values[5]:
            #     deleted_price = float(deleted_values[5])
            #     self.frame.sum.config(text=f"Rp. {self.frame.total_sum - deleted_price}")

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
            

            
    def onTreeview2_click(self, event):
        self.frame.qtyentry_1.delete(0, 'end')
        selectedItem = self.frame.tree2.item(self.frame.tree2.selection())
        if selectedItem:
            selectedValues = selectedItem['values']
        self.frame.qtyentry_1.insert(0,selectedValues[4])
        self.frame.delbutton_1.config(command=self.delete)
        self.frame.updatebutton_12.config(command = self.update)

    def createCustComboBox(self):
        currentUser = self.model.auth.current_user
        userId = currentUser["UserID"]
        customers = self.model.database.fetchExternalCustNameId(userId)
        self.customer_combobox = ttk.Combobox(self.frame, values=customers)
        self.customer_combobox.set("Select Customer")  # Set the default text
        self.customer_combobox.place(x=640, y=678, width=110, height=20)

        self.pay_combobox = ttk.Combobox(self.frame, values=["Cash","Debit","E-money"])
        self.pay_combobox.set("Select Payment Type")  # Set the default text
        self.pay_combobox.place(x=640, y=720, width=110, height=20)

        

    def createOrder(self):
        
        # Get necessary details for creating an order
        
        external_user_id, customer_name = self.customer_combobox.get().split('-')
        total_price = self.sumPrice()
        payment_type = self.pay_combobox.get()
       
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Insert order into the database
        order_id = self.model.database.insertOrder(
        order_type="Order",
        initiating_user_id=None,
        receiving_user_id=self.model.auth.current_user["UserID"],
        external_user_id=external_user_id,
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
        self.view.switch("orders")

        # userId = self.model.auth.current_user["UserID"]
        # totalPrice = self.sumPrice()
        # PaymentType = self.pay_combobox.get()

        # # Get the selected customer (ExternalUserID and Name) from the combobox
        # selected_customer = self.customer_combobox.get()

        # # Check if a customer is selected
        # if selected_customer != "Select Customer":
        #     # Extract ExternalUserID and Name from the selected_customer string
        #     external_user_id, customer_name = map(str.strip, selected_customer.split('-', 1))

        #     # Now you can use external_user_id and customer_name in your insertOrderInitial method
        #     userId = self.model.auth.current_user["UserID"]
        #     totalPrice = self.sumPrice()
        #     PaymentType = self.pay_combobox.get()

        #     # You need to obtain the values for variantId and pricePer from somewhere
        #     variantId = "your_variant_id"
        #     pricePer = "your_price_per"
        #     qty = "your_qty"

        #     # Call the insertOrderInitial method with the required parameters
        #     self.model.database.insertOrderInitial(
        #         userId, totalPrice, PaymentType, external_user_id, variantId, pricePer, qty
        #     )
        # else:
        #     # Handle the case where no customer is selected
        #     tk.messagebox.showwarning("Error", "Please select a customer.")

     


       
            


                

            
        
        