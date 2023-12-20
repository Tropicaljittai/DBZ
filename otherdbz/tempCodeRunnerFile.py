def orders(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.sidebar()
        
        # self.l = customtkinter.CTkLabel(self, font=custom_font, text="Customer Details", text_color="White")
        # self.label.place(x=200, y= 30)

        # self.title = customtkinter.CTkLabel(self, font=("Arial Rounded MT Bold",25),text="Orders", text_color="#4477F9")
        # self.title.place(x= 210,y=55)
        # self.detail = customtkinter.CTkLabel(self, font=("Arial Rounded MT Bold",25),text="Details", text_color="#4477F9")
        # self.detail.place(x= 1060,y=55)

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=820, height=600)
        self.scrollable_frame.place(x = 200, y = 100)
        self.entries_in_scrollable_frame = []

        
    
        self.view_detail = customtkinter.CTkButton(self, text="View Detail")

        self.view_detail.place(x=200, y=750)

        self.orderIdPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.orderIdPOS.insert(0, "Order Id")
        self.orderIdPOS.configure(state = "readonly")
        self.orderIdPOS.grid(row=0, column=0, padx = (5, 0), pady = (10, 10))

        self.customerIdPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.customerIdPOS.insert(0, "CustomerId")
        self.customerIdPOS.configure(state = "readonly")
        self.customerIdPOS.grid(row=0, column=1, padx = (5, 0),  pady = (10, 10))

        self.addressPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.addressPOS.insert(0, "Address")
        self.addressPOS.configure(state = "readonly")
        self.addressPOS.grid(row=0, column=2, padx = (5, 0),  pady = (10, 10))

        self.totPricePOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.totPricePOS.insert(0, "Payment Status")
        self.totPricePOS.configure(state = "readonly")
        self.totPricePOS.grid(row=0, column=3, padx = (5, 0),  pady = (10, 10))

        self.payStatPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.payStatPOS.insert(0, "Shipping Status")
        self.payStatPOS.configure(state = "readonly")
        self.payStatPOS.grid(row=0, column=4, padx = (5, 0),  pady = (10, 10))

        self.shipStatPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        self.shipStatPOS.insert(0, "Order Date")
        self.shipStatPOS.configure(state = "readonly")
        self.shipStatPOS.grid(row=0, column=5, padx = (5, 0),  pady = (10, 10))

        


        view = customtkinter.CTkButton(self.scrollable_frame, text="view")
        view.grid(row=1+len(self.entries_in_scrollable_frame), column=5, padx=(10,10), pady=10)

        # self.datePOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
        # self.datePOS.insert(0, "Order Date")
        # self.datePOS.configure(state = "readonly")
        # self.datePOS.grid(row=0, column=5, padx = (5, 0),  pady = (10, 10))

        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.midframe = customtkinter.CTkScrollableFrame(self, width=435, height = 400, corner_radius=10)
        self.midframe.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.midframe.grid_rowconfigure(8, weight=1)
        self.midframe.place(x = 1050, y=100)

        self.productId = customtkinter.CTkEntry(self.midframe, justify = 'center',width=100)
        self.productId.insert(0, "Product Id")
        self.productId.configure(state = "readonly")
        self.productId.grid(row=0, column=0, padx = (7, 0), pady = (10, 10))

        self.productNames = customtkinter.CTkEntry(self.midframe, justify = 'center',width=100)
        self.productNames.insert(0, "Name")
        self.productNames.configure(state = "readonly")
        self.productNames.grid(row=0, column=1, padx = (7, 0),  pady = (10, 10))

        self.qty = customtkinter.CTkEntry(self.midframe, justify = 'center',width=100)
        self.qty .insert(0, "Quantity")
        self.qty .configure(state = "readonly")
        self.qty .grid(row=0, column=2, padx = (7, 0),  pady = (10, 10))

        self.prices = customtkinter.CTkEntry(self.midframe, justify = 'center',width=100)
        self.prices.insert(0, "Price")
        self.prices.configure(state = "readonly")
        self.prices.grid(row=0, column=3, padx = (7, 0),  pady = (10, 10))

        amount = database.count_orders()
        orders = database.fetch_orders()
        orderDetails = database.fetch_details()

        self.idsHome = []
        for i in range(amount[0]):
            self.Identry = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
            self.Identry.insert(0, orders[i][0])
            self.Identry.configure(state = "readonly")
            self.Identry.grid(row=1+i, column=0, padx = (5, 0),  pady = (10, 10))
            self.idsHome.append(self.Identry)

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
            self.entry.insert(0, orders[i][7])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=1, padx = (5, 0),  pady = (10, 10))

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center',width=110)
            self.entry.insert(0, orders[i][7])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=2, padx = (5, 0),  pady = (10, 10))

        self.plus_buttons = []

        self.entries_in_scrollable_frame = []
        self.ids_in_frame = []
        self.deletes_in_scrollable_frame = []

        self.idsProduct = []
        for i in range(amount[0]):
            self.Identry = customtkinter.CTkEntry(self.midframe, justify = 'center',width=110)
            self.Identry.insert(0, orders[i][0])
            self.Identry.configure(state = "readonly")
            self.Identry.grid(row=1+i, column=0, padx = (5, 0),  pady = (10, 10))
            self.idsProduct.append(self.Identry)

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.midframe, justify = 'center',width=110)
            self.entry.insert(0, orders[i][7])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=1, padx = (5, 0),  pady = (10, 10))

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.midframe, justify = 'center',width=110)
            self.entry.insert(0, orders[i][7])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=2, padx = (5, 0),  pady = (10, 10))

       