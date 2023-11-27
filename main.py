import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
from PIL import Image
from tkinter import messagebox
import database
from tkinter import END

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

    def sidebar(self):
        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1600}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Inventory", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.home)
        self.sidebar_button.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Employees")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Suppliers", command=self.supplier)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Customers", command=self.customer)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Orders")
        self.sidebar_button_4.grid(row=5, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Products", command=self.products)
        self.sidebar_button_5.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, text="Sales")
        self.sidebar_button_6.grid(row=7, column=0, padx=20, pady=10)


    def home(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.sidebar()

        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=800, height=600)
        self.scrollable_frame.place(x = 200, y = 100)

        self.create_invoice = customtkinter.CTkButton(self, text="Create Invoice")
        self.create_invoice.place(x=200, y=750)

        self.idsPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center')
        self.idsPOS.insert(0, "Product Id")
        self.idsPOS.configure(state = "readonly")
        self.idsPOS.grid(row=0, column=0, padx = (10, 0), pady = (10, 10))

        self.namesPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center')
        self.namesPOS.insert(0, "Name")
        self.namesPOS.configure(state = "readonly")
        self.namesPOS.grid(row=0, column=1, padx = (10, 0),  pady = (10, 10))

        self.pricesPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center')
        self.pricesPOS.insert(0, "Price")
        self.pricesPOS.configure(state = "readonly")
        self.pricesPOS.grid(row=0, column=2, padx = (10, 0),  pady = (10, 10))

        self.qtyPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center')
        self.qtyPOS.insert(0, "QTY")
        self.qtyPOS.configure(state = "readonly")
        self.qtyPOS.grid(row=0, column=3, padx = (10, 0),  pady = (10, 10))

        self.totalPOS = customtkinter.CTkEntry(self.scrollable_frame, justify = 'center')
        self.totalPOS.insert(0, "Total")
        self.totalPOS.configure(state = "readonly")
        self.totalPOS.grid(row=0, column=4, padx = (10, 0),  pady = (10, 10))

        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.midframe = customtkinter.CTkScrollableFrame(self, width=500, height = 685, corner_radius=10)
        self.midframe.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.midframe.grid_rowconfigure(8, weight=1)
        self.midframe.place(x = 1050, y=100)

        self.ids = customtkinter.CTkEntry(self.midframe, justify = 'center')
        self.ids.insert(0, "Product Id")
        self.ids.configure(state = "readonly")
        self.ids.grid(row=0, column=0, padx = (10, 0), pady = (10, 10))

        self.names = customtkinter.CTkEntry(self.midframe, justify = 'center')
        self.names.insert(0, "Name")
        self.names.configure(state = "readonly")
        self.names.grid(row=0, column=1, padx = (10, 0),  pady = (10, 10))

        self.prices = customtkinter.CTkEntry(self.midframe, justify = 'center')
        self.prices.insert(0, "Price")
        self.prices.configure(state = "readonly")
        self.prices.grid(row=0, column=2, padx = (10, 0),  pady = (10, 10))

        amount = database.count_product()

        products = database.fetch_products()

        self.idsHome = []
        for i in range(amount[0]):
            self.Identry = customtkinter.CTkEntry(self.midframe, justify = 'center')
            self.Identry.insert(0, products[i][0])
            self.Identry.configure(state = "readonly")
            self.Identry.grid(row=1+i, column=0, padx = (10, 0),  pady = (10, 10))
            self.idsHome.append(self.Identry)

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.midframe, justify = 'center')
            self.entry.insert(0, products[i][1])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=1, padx = (10, 0),  pady = (10, 10))

        for i in range(amount[0]):
            self.entry = customtkinter.CTkEntry(self.midframe, justify = 'center')
            self.entry.insert(0, products[i][7])
            self.entry.configure(state = "readonly")
            self.entry.grid(row=1+i, column=2, padx = (10, 0),  pady = (10, 10))

        self.plus_buttons = []

        for i in range(amount[0]):
            plus_button = customtkinter.CTkButton(self.midframe, text="+", width=30, command=lambda index=i: get_number(index))
            plus_button.grid(row=i+1, column=3, padx=(10, 10), pady=10)
            self.plus_buttons.append(plus_button)

        self.entries_in_scrollable_frame = []
        
        def get_number(index):
            selected_id = self.idsHome[index].get()
            insert_selected_id(selected_id)


        def insert_selected_id(selected_id):
            new_entry = customtkinter.CTkEntry(self.scrollable_frame, justify='center')
            new_entry.insert(0, selected_id)
            new_entry.configure(state="readonly")
            new_entry.grid(row=1+len(self.entries_in_scrollable_frame), column=0, padx=(10, 0), pady=(10, 10))

            self.plus = customtkinter.CTkButton(self.scrollable_frame, text="X", width=30)
            self.plus.grid(row=1+len(self.entries_in_scrollable_frame), column=5, padx=(10,10), pady=10)

            # Add the new entry to a list if you need to access it later
            self.entries_in_scrollable_frame.append(new_entry)







# ----------------------------------------------------- PRODUCTS PAGE -----------------------------------------------------

    def products(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1600}x{900}")

        self.sidebar()

        custom_font=("Arial",30)


        self.label = customtkinter.CTkLabel(self, font=custom_font, text="Product Details", text_color="White")
        self.label.place(x=200, y= 30)

        frame = customtkinter.CTkFrame(self, width= 400, height = 400)
        frame.place(x= 200, y=100)

        self.name = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.name.place(x=240, y= 160)

        self.id = customtkinter.CTkEntry(self, placeholder_text="Id")
        self.id.place(x=410, y= 160)

        self.stock = customtkinter.CTkEntry(self, placeholder_text="Total Stock")
        self.stock.place(x=240, y= 220)

        self.label = customtkinter.CTkEntry(self, placeholder_text="Label")
        self.label.place(x=240, y= 280)

        products = database.fetch_supplier_ids()
        value = []
        for i in products:
            i = str(i)
            i = i[1:len(i)-1]
            i = i.replace("'", '')
            i = i.replace(",", ' -')
            value.append(i)

        self.outgoingStock = customtkinter.CTkEntry(self, placeholder_text="Outgoing Stock")
        self.outgoingStock.place(x=410, y= 280)
        
        self.supplier_product = customtkinter.CTkComboBox(self, values=value, state="readonly")
        self.supplier_product.set("Supplier")
        self.supplier_product.place(x=240, y= 340)

        self.price = customtkinter.CTkEntry(self, placeholder_text="Price")
        self.price.place(x=410, y= 340)

        self.add_button = customtkinter.CTkButton(self, command=self.insert, text="Add")
        self.add_button.place(x=240, y=400)

        self.update_button = customtkinter.CTkButton(self, command=self.update, text="Update")
        self.update_button.place(x=410, y=400)

        self.delete_button = customtkinter.CTkButton(self, command=self.delete, text="Delete")
        self.delete_button.place(x=240, y=440)

        self.clearbutton = customtkinter.CTkButton(self, command=lambda:self.clear(True), text="Clear")
        self.clearbutton.place(x=410, y=440)

        self.tabview = customtkinter.CTkTabview(self, width=250)


        self.status = customtkinter.CTkComboBox(self, values=["Received", "Shipped", "On Hand"], state="readonly")
        self.status.set("Status")
        self.status.place(x=410, y=220)

        self.style = ttk.Style(self)

        self.style.theme_use("default")
    
        self.style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            rowheight=50,
                            fieldbackground="#343638",
                            bordercolor="#343638")
        
        
        self.style.map('Treeview', background=[('selected', '#22559b')])
        
        self.style.configure("Treeview.Heading",
                                    background="#565b5e",
                                    foreground="white",
                                    relief="flat")
        
        self.style.map("Treeview.Heading",
                      background=[('active', '#3484F0')])
        
        self.tree = ttk.Treeview(self, height=20)

        self.tree['columns'] = ('ID', 'Name', 'Label', 'Status', 'Total Stock', 'Outgoing Stock', 'Supplier', 'Price')

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=170)
        self.tree.column('Name', anchor=tk.CENTER, width=170)
        self.tree.column('Label', anchor=tk.CENTER, width=170)
        self.tree.column('Status', anchor=tk.CENTER, width=170)
        self.tree.column('Total Stock', anchor=tk.CENTER, width=170)
        self.tree.column('Outgoing Stock', anchor=tk.CENTER, width=170)
        self.tree.column('Supplier', anchor=tk.CENTER, width=170)
        self.tree.column('Price', anchor=tk.CENTER, width=170)

        self.tree.heading('ID', text="Id")
        self.tree.heading('Name', text="Name")
        self.tree.heading('Label', text="Label")
        self.tree.heading('Status', text="Status")
        self.tree.heading('Total Stock', text="Total Stock")
        self.tree.heading('Outgoing Stock', text='Outgoing Stock')
        self.tree.heading('Supplier', text="Supplier")
        self.tree.heading('Price', text="Price (Rp)")

        self.tree.place(x = 1000, y = 150)
        self.tree.bind('<ButtonRelease>', self.display_data)

        self.add_to_treeview()

    def display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear()
            self.id.insert(0, row[0])
            self.name.insert(0, row[1])
            self.label.insert(0, row[2])
            self.status.set(row[3])
            self.stock.insert(0, row[4])
            self.outgoingStock.insert(0, row[5])
            self.supplier_product.set(row[6])           
            self.price.insert(0, row[7])
        else:
            pass

    def delete(self):
        selected_item = self.tree.focus()
        if not selected_item:   
            messagebox.showerror('Error', 'Choose a product to delete')
        else:
            id_entry = self.id.get()
            database.delete_products(id_entry)
            self.add_to_treeview()
            self.clear()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a product to update')
        else:
            id_entry = self.id.get()
            name_entry = self.name.get()
            label_entry = self.label.get()
            status_entry = self.status.get()
            stock_entry = self.stock.get()
            outgoing_stock_entry = self.outgoingStock.get()
            supplier_entry = self.supplier_product.get()
            price_entry = self.price.get()
            database.update_products(id_entry, name_entry, label_entry, status_entry, stock_entry, outgoing_stock_entry, supplier_entry, price_entry)
            self.add_to_treeview()
            self.clear()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been updated')

    def insert(self):
        id_entry = self.id.get()
        name_entry = self.name.get()
        label_entry = self.label.get()
        status_entry = self.status.get()
        stock_entry = self.stock.get()
        outgoing_stock_entry = self.outgoingStock.get()
        supplier_entry = self.supplier_product.get()
        price_entry = self.price.get()
        if not (id_entry and name_entry and label_entry and status_entry and stock_entry and outgoing_stock_entry and supplier_entry and price_entry):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exists(id_entry):
            messagebox.showerror('Error', "Id already exists.")
        else:
            try:
                stock_value = int(stock_entry)
                database.insert_product(id_entry, name_entry, label_entry, status_entry, stock_entry, outgoing_stock_entry, supplier_entry, price_entry)
                self.add_to_treeview()
                self.clear()
                # create_chart()
                messagebox.showinfo('Success', 'Data has been inserted')
            except ValueError:
                messagebox.showerror('Error', 'Stock should be an integer.')

    def clear(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id.delete(0,END)
        self.id.configure(placeholder_text = "Id")
        self.name.delete(0,END)
        self.name.configure(placeholder_text = "Name")
        self.label.delete(0,END)
        self.label.configure(placeholder_text = "Label")
        self.status.set("Status")
        self.stock.delete(0,END)
        self.stock.configure(placeholder_text = "Stock/Quantity")
        self.outgoingStock.delete(0,END)
        self.outgoingStock.configure(placeholder_text = "Outgoing Stock")
        self.supplier_product.set("Supplier")
        self.price.delete(0,END)
        self.price.configure(placeholder_text = "Price")

    def add_to_treeview(self):
        products = database.fetch_products()
        self.tree.delete(*self.tree.get_children())
        for i in products:
            self.tree.insert('', END, values=i)

# ----------------------------------------------------- SUPPLIER PAGE -----------------------------------------------------

    def supplier(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1600}x{900}")

        self.sidebar()

        custom_font=("Arial",30)
        custom_font2=(7)


        self.label = customtkinter.CTkLabel(self, font=custom_font, text="Supplier Details", text_color="White")
        self.label.place(x=200, y= 30)

        frame = customtkinter.CTkFrame(self, width= 400, height = 500)
        frame.place(x= 200, y=100)
        
        self.supplierName = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.supplierName.place(x=240, y= 160)

        self.supplierId = customtkinter.CTkEntry(self, placeholder_text="Id")
        self.supplierId.place(x=410, y= 160)

        self.invoiceNum = customtkinter.CTkEntry(self, placeholder_text="Invoice Number")
        self.invoiceNum.place(x=240, y= 220)

        self.contact = customtkinter.CTkEntry(self, placeholder_text="Contact")
        self.contact.place(x=240, y= 280)

        self.supplier_entry = customtkinter.CTkEntry(self, placeholder_text="Description", height=90)
        self.supplier_entry.place(x=410, y= 220)

        self.bankNumSupplier = customtkinter.CTkEntry(self, placeholder_text="Bank Number")
        self.bankNumSupplier.place(x=240, y= 340)

        self.bankNameSupplier = customtkinter.CTkEntry(self, placeholder_text="Bank Name")
        self.bankNameSupplier.place(x=410, y= 340)

        self.accHolderSupplier = customtkinter.CTkEntry(self, placeholder_text="Account Holder")
        self.accHolderSupplier.place(x=240, y= 400)

        self.add_button = customtkinter.CTkButton(self, command=self.insert_supplier, text="Add")
        self.add_button.place(x=240, y=440)

        self.update_button = customtkinter.CTkButton(self, command=self.update_supplier, text="Update")
        self.update_button.place(x=410, y=440)

        self.delete_button = customtkinter.CTkButton(self, command=self.delete_supplier, text="Delete")
        self.delete_button.place(x=240, y=480)

        self.clearbutton = customtkinter.CTkButton(self, command=lambda:self.clear_supplier(True), text="Clear")
        self.clearbutton.place(x=410, y=480)

        self.tabview = customtkinter.CTkTabview(self, width=250)

        self.style = ttk.Style(self)

        self.style.theme_use("default")
    
        self.style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            rowheight=50,
                            fieldbackground="#343638",
                            bordercolor="#343638")
        
        
        self.style.map('Treeview', background=[('selected', '#22559b')])
        
        self.style.configure("Treeview.Heading",
                                    background="#565b5e",
                                    foreground="white",
                                    relief="flat")
        
        self.style.map("Treeview.Heading",
                      background=[('active', '#3484F0')])

        self.tree_supplier = ttk.Treeview(self, height=20)

        self.tree_supplier['columns'] = ('ID', 'Name', 'Invoice No.', 'Contact', 'Bank Number', 'Bank Name', 'Account Holder', 'Description')

        self.tree_supplier.column('#0', width=0, stretch=tk.NO)
        self.tree_supplier.column('ID', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Name', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Invoice No.', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Contact', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Bank Number', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Bank Name', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Account Holder', anchor=tk.CENTER, width=170)
        self.tree_supplier.column('Description', anchor=tk.CENTER, width=170)

        self.tree_supplier.heading('ID', text="Id")
        self.tree_supplier.heading('Name', text="Name")
        self.tree_supplier.heading('Invoice No.', text="Invoice No.")
        self.tree_supplier.heading('Contact', text="Contact")
        self.tree_supplier.heading('Bank Number', text="Bank Number")
        self.tree_supplier.heading('Bank Name', text="Bank Name")
        self.tree_supplier.heading('Account Holder', text="Account Holder")
        self.tree_supplier.heading('Description', text="Description")

        self.tree_supplier.place(x = 1000, y = 150)
        self.tree_supplier.bind('<ButtonRelease>', self.display_data_supplier)

        self.add_to_treeview_supplier()

    def display_data_supplier(self, event):
        selected_item = self.tree_supplier.focus()
        if selected_item:
            row = self.tree_supplier.item(selected_item)['values']
            self.clear_supplier()
            self.supplierId.insert(0, row[0])
            self.supplierName.insert(0, row[1])
            self.invoiceNum.insert(0, row[2])
            self.contact.insert(0, row[3])
            self.bankNumSupplier.insert(0, row[4])
            self.bankNameSupplier.insert(0, row[5])
            self.accHolderSupplier.insert(0, row[6])
            self.supplier_entry.insert(0, row[7])
        else:
            pass

    def delete_supplier(self):
        selected_item = self.tree_supplier.focus()
        if not selected_item:   
            messagebox.showerror('Error', 'Choose a supplier detail to delete')
        else:
            id_entry = self.supplierId.get()
            database.delete_supplier(id_entry)
            self.add_to_treeview_supplier()
            self.clear_supplier()
            # self.create_chart()
            messagebox.showinfo('Success', 'Supplier detail has been deleted')

    def update_supplier(self):
        selected_item = self.tree_supplier.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a product to update')
        else:
            id_entry = self.supplierId.get()
            name_entry = self.supplierName.get()
            label_entry = self.invoiceNum.get()
            status_entry = self.contact.get()
            bankNum = self.bankNumSupplier.get()
            bankName = self.bankNameSupplier.get()
            accHolder = self.accHolderSupplier.get()
            stock_entry = self.supplier_entry.get()
            database.update_supplier(id_entry, name_entry, label_entry, status_entry, bankNum, bankName, accHolder, stock_entry)
            self.add_to_treeview_supplier()
            self.clear_supplier()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been updated')

    def insert_supplier(self):
        id_entry = self.supplierId.get()
        name_entry = self.supplierName.get()
        label_entry = self.invoiceNum.get()
        status_entry = self.contact.get()
        bankNum = self.bankNumSupplier.get()
        bankName = self.bankNameSupplier.get()
        accHolder = self.accHolderSupplier.get()
        stock_entry = self.supplier_entry.get()
        if not (id_entry and name_entry and label_entry and status_entry and stock_entry and bankName and bankNum and accHolder):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.SupplierId_exists(id_entry):
            messagebox.showerror('Error', "Id already exists.")
        else:
            try:
                database.insert_supplier(id_entry, name_entry, label_entry, status_entry, bankNum, bankName, accHolder, stock_entry)
                self.add_to_treeview_supplier()
                self.clear_supplier()
                # create_chart()
                messagebox.showinfo('Success', 'Data has been inserted')
            except ValueError:
                messagebox.showerror('Error', 'Stock should be an integer.')

    def clear_supplier(self, *clicked):
        if clicked:
            self.tree_supplier.selection_remove(self.tree_supplier.focus())
            self.tree_supplier.focus('')
        self.supplierId.delete(0,END)
        self.supplierId.configure(placeholder_text = "Id")
        self.supplierName.delete(0,END)
        self.supplierName.configure(placeholder_text = "Name")
        self.invoiceNum.delete(0,END)
        self.invoiceNum.configure(placeholder_text = "Invoice No.")
        self.contact.delete(0,END)
        self.contact.configure(placeholder_text = "Contact")
        self.bankNumSupplier.delete(0,END)
        self.bankNumSupplier.configure(placeholder_text = "Bank Number")
        self.bankNameSupplier.delete(0,END)
        self.bankNameSupplier.configure(placeholder_text = "Bank Name")
        self.accHolderSupplier.delete(0,END)
        self.accHolderSupplier.configure(placeholder_text = "Account Holder")
        self.supplier_entry.delete(0,END)
        self.supplier_entry.configure(placeholder_text = "Description")


    def add_to_treeview_supplier(self):
        products = database.fetch_supplier()
        self.tree_supplier.delete(*self.tree_supplier.get_children())
        for i in products:
            self.tree_supplier.insert('', END, values=i)

# ----------------------------------------------------- CUSTOMER PAGE -----------------------------------------------------

    def customer(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1600}x{900}")

        self.sidebar()

        custom_font=("Arial",30)
        custom_font2=(7)


        self.label = customtkinter.CTkLabel(self, font=custom_font, text="Customer Details", text_color="White")
        self.label.place(x=200, y= 30)

        frame = customtkinter.CTkFrame(self, width= 400, height = 400)
        frame.place(x= 200, y=100)

        self.custName = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.custName.place(x=240, y= 160)

        self.CustId = customtkinter.CTkEntry(self, placeholder_text="Id")
        self.CustId.place(x=410, y= 160)

        self.CustEmail = customtkinter.CTkEntry(self, placeholder_text="Email")
        self.CustEmail.place(x=240, y= 220)

        self.CustPhone = customtkinter.CTkEntry(self, placeholder_text="Phone")
        self.CustPhone.place(x=410, y= 220)

        self.CustBankName = customtkinter.CTkEntry(self, placeholder_text="Bank Name")
        self.CustBankName.place(x=410, y= 280)

        self.CustAddress = customtkinter.CTkEntry(self, placeholder_text="Address")
        self.CustAddress.place(x=240, y= 280)

        self.CustBankNum = customtkinter.CTkEntry(self, placeholder_text="Account Number")
        self.CustBankNum.place(x=240, y= 340)

        self.CustBankHolder = customtkinter.CTkEntry(self, placeholder_text="Account Holder")
        self.CustBankHolder.place(x=410, y= 340)



        self.add_button = customtkinter.CTkButton(self, command=self.insert_customer, text="Add")
        self.add_button.place(x=240, y=400)

        self.update_button = customtkinter.CTkButton(self, command=self.update_customer, text="Update")
        self.update_button.place(x=410, y=400)

        self.delete_button = customtkinter.CTkButton(self, command=self.delete_customer, text="Delete")
        self.delete_button.place(x=240, y=440)

        self.clearbutton = customtkinter.CTkButton(self, command=lambda:self.clear_customer(True), text="Clear")
        self.clearbutton.place(x=410, y=440)

        self.tabview = customtkinter.CTkTabview(self, width=250)


        self.style = ttk.Style(self)

        self.style.theme_use("default")
    
        self.style.configure("Treeview",
                            background="#2a2d2e",
                            foreground="white",
                            rowheight=50,
                            fieldbackground="#343638",
                            bordercolor="#343638")
        
        
        self.style.map('Treeview', background=[('selected', '#22559b')])
        
        self.style.configure("Treeview.Heading",
                                    background="#565b5e",
                                    foreground="white",
                                    relief="flat")
        
        self.style.map("Treeview.Heading",
                      background=[('active', '#3484F0')])

        self.tree = ttk.Treeview(self, height=20)

        self.tree['columns'] = ('ID', 'Name', 'Email', 'Phone', 'Address', 'Bank Name', 'Account Number', 'Account Holder')

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=170)
        self.tree.column('Name', anchor=tk.CENTER, width=170)
        self.tree.column('Email', anchor=tk.CENTER, width=170)
        self.tree.column('Phone', anchor=tk.CENTER, width=170)
        self.tree.column('Address', anchor=tk.CENTER, width=170)
        self.tree.column('Bank Name', anchor=tk.CENTER, width=170)
        self.tree.column('Account Number', anchor=tk.CENTER, width=170)
        self.tree.column('Account Holder', anchor=tk.CENTER, width=170)

        self.tree.heading('ID', text="Id")
        self.tree.heading('Name', text="Name")
        self.tree.heading('Email', text="Email")
        self.tree.heading('Phone', text="Phone")
        self.tree.heading('Address', text="Address")
        self.tree.heading('Bank Name', text='Bank Name')
        self.tree.heading('Account Number', text="Account Number")
        self.tree.heading('Account Holder', text="Account Holder")

        self.tree.place(x = 1000, y = 150)
        self.tree.bind('<ButtonRelease>', self.display_data_customer)

        self.add_to_treeview_customer()

    def display_data_customer(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_customer()
            self.CustId.insert(0, row[0])
            self.custName.insert(0, row[1])
            self.CustEmail.insert(0, row[2])
            self.CustPhone.insert(0, row[3])
            self.CustAddress.insert(0, row[4])
            self.CustBankName.insert(0, row[5])
            self.CustBankNum.insert(0, row[6])
            self.CustBankHolder.insert(0, row[7])           
        else:
            pass

    def delete_customer(self):
        selected_item = self.tree.focus()
        if not selected_item:   
            messagebox.showerror('Error', 'Choose a customer to delete')
        else:
            id_entry = self.CustId.get()
            database.delete_Customer(id_entry)
            self.add_to_treeview_customer()
            self.clear_customer()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_customer(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a customer to update')
        else:
            id_entry = self.CustId.get()
            name_entry = self.custName.get()
            email_entry = self.CustEmail.get()
            phone_entry = self.CustPhone.get()
            address_entry = self.CustAddress.get()
            bank_entry = self.CustBankName.get()
            bankNum_entry = self.CustBankNum.get()
            bankHolder_entry = self.CustBankHolder.get()
            database.update_Customer(id_entry, name_entry, email_entry, phone_entry, address_entry, bank_entry, bankNum_entry, bankHolder_entry)
            self.add_to_treeview_customer()
            self.clear_customer()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been updated')

    def insert_customer(self):
        id_entry = self.CustId.get()
        name_entry = self.custName.get()
        email_entry = self.CustEmail.get()
        phone_entry = self.CustPhone.get()
        address_entry = self.CustAddress.get()
        bank_entry = self.CustBankName.get()
        bankNum_entry = self.CustBankNum.get()
        bankHolder_entry = self.CustBankHolder.get()
        if not (id_entry and name_entry and email_entry and phone_entry and address_entry and bank_entry and bankNum_entry and bankHolder_entry):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exists_customer(id_entry):
            messagebox.showerror('Error', "Id already exists.")
        else:
            try:
                database.insert_Customer(id_entry, name_entry, email_entry, phone_entry, address_entry, bank_entry, bankNum_entry, bankHolder_entry)
                self.add_to_treeview_customer()
                self.clear_customer()
                # create_chart()
                messagebox.showinfo('Success', 'Data has been inserted')
            except ValueError:
                messagebox.showerror('Error', 'Stock should be an integer.')

    def clear_customer(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.CustId.delete(0,END)
        self.CustId.configure(placeholder_text = "Id")
        self.custName.delete(0,END)
        self.custName.configure(placeholder_text = "Name")
        self.CustEmail.delete(0,END)
        self.CustEmail.configure(placeholder_text = "Email")
        self.CustPhone.delete(0,END)
        self.CustPhone.configure(placeholder_text = "Phone")
        self.CustAddress.delete(0,END)
        self.CustAddress.configure(placeholder_text = "Address")
        self.CustBankName.delete(0,END)
        self.CustBankName.configure(placeholder_text = "Bank Name")
        self.CustBankNum.delete(0,END)
        self.CustBankNum.configure(placeholder_text = "Account Number")
        self.CustBankHolder.delete(0,END)
        self.CustBankHolder.configure(placeholder_text = "Account Holder")

    def add_to_treeview_customer(self):
        products = database.fetch_customer()
        self.tree.delete(*self.tree.get_children())
        for i in products:
            self.tree.insert('', END, values=i)

if __name__ == "__main__":
    app = App()
    app.home()
    app.mainloop()