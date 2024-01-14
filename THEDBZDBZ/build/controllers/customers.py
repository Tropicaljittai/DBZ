class customersController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["customers"]
        self._bind()
    def _bind(self):
        self.frame.addbutton_2.config(command=self.add)
        self.frame.productsbutton_9.config(command=self.go_to_products)
        self.frame.ordersbutton_10.config(command=self.goToOrder)


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

    
    def add(self):
        userId = self.model.auth.current_user["UserID"]
        name = self.frame.nameentry_1.get()
        num = self.frame.phoneentry_2.get()
        address =self.frame.addressentry_3.get()
        bankname = self.frame.bankNameentry_5.get()
        banknum = self.frame.bankNumentry_6.get()
        bankhold =self.frame.accountHolderentry_7.get()
        email = self.frame.emailentry_4.get()

        self.model.database.addCustomer(userId,name,num,email,address,bankname,banknum,bankhold)
        self.populate_treeview()

    def clear(self):
        entries = [self.frame.nameentry_1,
            self.frame.phoneentry_2,
            self.frame.addressentry_3,
            self.frame.bankNameentry_5,
            self.frame.bankNumentry_6,
            self.frame.accountHolderentry_7
            ]
        
        for entry in entries:
            entry.delete(0, 'end')

    # def display_data(self, event):
    #     selected_item = self.frame.tree.focus()
    #     if selected_item:
    #         row = self.frame.tree.item(selected_item)['values']
    #         self.clear()
    #         self.frame.idEntry.insert(0, row[0])
    #         self.frame.nameEntry.insert(0, row[1])
    #         self.frame.descriptionEntry.insert(0, row[2])
    #         self.frame.priceEntry.insert(0,row[3])
        
    #     else:
    #         pass
    
    def populate_treeview(self):
        userId = self.model.auth.current_user["UserID"]
        customers = self.model.database.fetchExternalCust(userId)
        self.frame.tree.delete(*self.frame.tree.get_children())
        for i in customers:
            _,_, name, number, email,address,bankname,banknum,bankholder, *_ = i
            self.frame.tree.insert('', "end", values=(name, number, email,address,bankname,banknum,bankholder))

