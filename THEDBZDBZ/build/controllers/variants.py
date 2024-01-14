import tkinter as tk


class variantsController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["variants"]
        
        self._bind()
        self.model.auth.add_event_listener(
            "currentProduct", self.productChanged_listener
        )

    def _bind(self):
        self.frame.add.config(command = self.addVariant)
        self.frame.tree.bind('<ButtonRelease>', self.display_data)
        self.frame.orders.config(command=self.goToOrder)
        self.frame.back.config(command = self.go_to_products)
      

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

    def productChanged_listener(self,data=None):
        currentProd = self.model.auth.currentProd
        if currentProd:
            Name = currentProd["name"]
            self.frame.prodName.config(text=str(Name))
        self.populate_treeview()

    # def populate_treeview(self):
    #     currentProd = self.model.auth.currentProd
    #     if currentProd and "id" in currentProd:
    #         products = self.model.database.fetch_productsVariants(currentProd["id"])
    #         self.frame.tree.delete(*self.frame.tree.get_children())
    #         for i in products:
    #             self.frame.tree.insert('', "end", values=i)
    def populate_treeview(self):
        currentProd = self.model.auth.currentProd
    
        if currentProd and "id" in currentProd:
            products = self.model.database.fetch_productsVariants(currentProd["id"])
            
            self.frame.tree.delete(*self.frame.tree.get_children())
            for i in products:
                self.frame.tree.insert('', "end", values=i)


     


    def addVariant(self):
        currentProd = self.model.auth.currentProd
        comingStock = self.frame.shippedStockentry_6.get()
        name = self.frame.variantentry_1.get()
        id = currentProd["id"]
        description =  self.frame.descentry_5.get()
        price =  self.frame.priceentry_3.get()
        size = self.frame.sizeentry_4.get()
        stock = self.frame.stockentry_2.get()
        if not (id and name and description and price):
            tk.messagebox.showerror('Error', 'Enter all fields.')
     
        else:
            self.model.database.addProductVariant( id ,comingStock,name,size,stock,price,description)
            self.populate_treeview()
            tk.messagebox.showinfo('Success', 'Data has been inserted')


    def clear(self):
        entries = [
            self.frame.shippedStockentry_6,
            self.frame.descentry_5,
            self.frame.variantentry_1,
            self.frame.sizeentry_4,
            self.frame.stockentry_2,
            self.frame.priceentry_3
        ]

        for entry in entries:
            entry.delete(0, tk.END)


    def display_data(self, event):
        selected_item = self.frame.tree.focus()
        if selected_item:
            row = self.frame.tree.item(selected_item)['values']
            self.clear()
            self.frame.descentry_5.insert(0, row[6])
            self.frame.variantentry_1.insert(0, row[1])
            self.frame.sizeentry_4.insert(0,row[2])
            self.frame.stockentry_2.insert(0, row[3])
            self.frame.priceentry_3.insert(0, row[5])
            self.frame.shippedStockentry_6.insert(0,row[4])
        else:
            pass


     
     
     
      

   


