import tkinter as tk


class productsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["products"]
        self._bind()

    def _bind(self):
        self.frame.addBtn.config(command = self.add)
        self.frame.variantsBtn.config(command = self.seeVariant)
        self.frame.order.config(command=self.go_to_orders)
        self.frame.deleteBtn.config(command= self.delete_product)
        self.frame.tree.bind('<ButtonRelease>', self.display_data)

    def go_to_orders(self):
        self.view.switch("orders")


    def populate_treeview(self):
        currentUser = self.model.auth.current_user
        products = self.model.database.fetch_products(currentUser["UserID"])
        self.frame.tree.delete(*self.frame.tree.get_children())
        for i in products:
            self.frame.tree.insert('', "end", values=i)


    def seeVariant(self):
        id = self.model.database.fetch_productID_fromName(self.frame.nameEntry.get())
        self.model.auth.updateProductName(id)
        self.view.switch("variants")
        
        

        

    def clear(self):
        entries = [self.frame.nameEntry,
            self.frame.descriptionEntry,
            self.frame.idEntry,
            self.frame.priceEntry,
            ]
        
        for entry in entries:
            entry.delete(0, 'end')

            
    def add(self):
        currentUser = self.model.auth.current_user
        userId = currentUser["UserID"]
        name = self.frame.nameEntry.get()
        idCheck = self.frame.idEntry.get()
        description =  self.frame.descriptionEntry.get()
        price =  self.frame.priceEntry.get()
        if not (name and description and price):
            tk.messagebox.showerror('Error', 'Enter all fields.')
        elif self.model.database.productId_exists(idCheck):
            tk.messagebox.showerror('Error', "Id already exists.")
        else:
            id=self.model.database.addProducts(userId,name,description,price)
            self.populate_treeview()
            tk.messagebox.showinfo('Success', 'Data has been inserted')
            self.model.auth.updateProductName(id)
            self.view.switch("variants")
    
        
            
        

    def display_data(self, event):
        selected_item = self.frame.tree.focus()
        if selected_item:
            row = self.frame.tree.item(selected_item)['values']
            self.clear()
            self.frame.idEntry.insert(0, row[0])
            self.frame.nameEntry.insert(0, row[1])
            self.frame.descriptionEntry.insert(0, row[2])
            self.frame.priceEntry.insert(0,row[3])
        
        else:
            pass
    
    def delete_product(self):
        selected_item = self.frame.tree.focus()
        if selected_item:
            product_id = self.frame.tree.item(selected_item)['values'][0]
            confirmed = tk.messagebox.askyesno('Confirmation', f'Do you want to delete product with ID {product_id}?')
            if confirmed:
                self.model.database.deleteProduct(product_id)
                self.populate_treeview()
                self.clear()
                tk.messagebox.showinfo('Success', f'Product with ID {product_id} deleted successfully.')
        else:
            tk.messagebox.showwarning('Warning', 'Select a product to delete.')

        

        
        




    
        

    #     # Bind any other event handlers or logic as needed
    #     self.frame.entry.bind("<KeyRelease>", self.on_entry_change)

    # def on_entry_change(self, event):
    #     updated_text = self.frame.entry.get()
         
        

    #         # Define a dictionary to store Entry widgets, their types, and database field references
    #     self.entry_info = {
    #         self.frame.entry_name: ("name", "name_field_in_database"),
    #         self.frame.entry_email: ("email", "email_field_in_database"),
    #         # Add more entries with types and database field references as needed
    #     }

    #     self._set_default_texts()

    # def _set_default_texts(self):
    #     for entry, (entry_type, database_field) in self.entry_info.items():
    #         default_text = self.model.get_default_text_from_database(entry_type, database_field)
    #         entry.insert(0, default_text)

    #     # Bind event handlers or logic for entries as needed
