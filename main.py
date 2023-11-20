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
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Inventory", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.home)
        self.sidebar_button.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Employees")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Suppliers", command=self.supplier)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)

    def home(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.sidebar()

        custom_font=("Arial",30)
        self.button_customer = customtkinter.CTkButton(self, text = 'Customers', font=custom_font, width=200)
        self.button_customer.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.button_orders = customtkinter.CTkButton(self, text = 'Orders', font=custom_font, width=200)
        self.button_orders.grid(row=0, column=2, padx=(20, 15), pady=(20, 0), sticky="nsew")

        self.button_product = customtkinter.CTkButton(self, text = 'Products', command=self.products,font=custom_font, width=200)
        self.button_product.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.button_sales = customtkinter.CTkButton(self, text = 'Sales', font=custom_font, width=200)
        self.button_sales.grid(row=1, column=2, padx=(20, 15), pady=(20, 0),sticky="nsew")


    def products(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1600}x{900}")

        self.sidebar()

        custom_font=("Arial",30)
        custom_font2=(7)


        self.label = customtkinter.CTkLabel(self, font=custom_font, text="Product Details", text_color="White")
        self.label.place(x=200, y= 30)

        frame = customtkinter.CTkFrame(self, width= 400, height = 400)
        frame.place(x= 200, y=100)

        self.name = customtkinter.CTkEntry(self, placeholder_text="Name")
        self.name.place(x=240, y= 160)

        self.id = customtkinter.CTkEntry(self, placeholder_text="Id")
        self.id.place(x=410, y= 160)

        self.stock = customtkinter.CTkEntry(self, placeholder_text="Stock/Quantity")
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
        
        self.supplier_product = customtkinter.CTkComboBox(self, values=value, state="readonly")
        self.supplier_product.set("Supplier")
        self.supplier_product.place(x=410, y= 280)

        self.add_button = customtkinter.CTkButton(self, command=self.insert, text="Add")
        self.add_button.place(x=240, y=340)

        self.update_button = customtkinter.CTkButton(self, command=self.update, text="Update")
        self.update_button.place(x=410, y=340)

        self.delete_button = customtkinter.CTkButton(self, command=self.delete, text="Delete")
        self.delete_button.place(x=240, y=400)

        self.clearbutton = customtkinter.CTkButton(self, command=lambda:self.clear(True), text="Clear")
        self.clearbutton.place(x=410, y=400)

        self.tabview = customtkinter.CTkTabview(self, width=250)


        self.status = customtkinter.CTkComboBox(self, values=["Received", "Shipped", "On Hand"], state="readonly")
        self.status.set("Status")
        self.status.place(x=410, y=220)

        self.style = ttk.Style(self)

        self.style.theme_use('clam')
        self.style.configure('Treeview', font=custom_font2, foreground='#fff', background='#0A0B0C', fieldbackground='#1B1B21', rowheight=50)
        self.style.map('Treeview', background=[('selected', '#AA04A7')])

        self.tree = ttk.Treeview(self, height=20)

        self.tree['columns'] = ('ID', 'Name', 'Label', 'Status', 'Stock', 'Supplier')

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=220)
        self.tree.column('Name', anchor=tk.CENTER, width=220)
        self.tree.column('Label', anchor=tk.CENTER, width=220)
        self.tree.column('Status', anchor=tk.CENTER, width=220)
        self.tree.column('Stock', anchor=tk.CENTER, width=220)
        self.tree.column('Supplier', anchor=tk.CENTER, width=220)

        self.tree.heading('ID', text="Id")
        self.tree.heading('Name', text="Name")
        self.tree.heading('Label', text="Label")
        self.tree.heading('Status', text="Status")
        self.tree.heading('Stock', text="Stock")
        self.tree.heading('Supplier', text="Supplier")

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
            self.supplier_product.set(row[5])
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
            supplier_entry = self.supplier_product.get()
            database.update_products(id_entry, name_entry, label_entry, status_entry, stock_entry, supplier_entry)
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
        supplier_entry = self.supplier_product.get()
        if not (id_entry and name_entry and label_entry and status_entry and stock_entry and supplier_entry):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exists(id_entry):
            messagebox.showerror('Error', "Id already exists.")
        else:
            try:
                stock_value = int(stock_entry)
                database.insert_product(id_entry, name_entry, label_entry, status_entry, stock_entry, supplier_entry)
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
        self.supplier_product.set("Supplier")

    def add_to_treeview(self):
        products = database.fetch_products()
        self.tree.delete(*self.tree.get_children())
        for i in products:
            self.tree.insert('', END, values=i)


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

        frame = customtkinter.CTkFrame(self, width= 400, height = 400)
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

        self.add_button = customtkinter.CTkButton(self, command=self.insert_supplier, text="Add")
        self.add_button.place(x=240, y=340)

        self.update_button = customtkinter.CTkButton(self, command=self.update_supplier, text="Update")
        self.update_button.place(x=410, y=340)

        self.delete_button = customtkinter.CTkButton(self, command=self.delete_supplier, text="Delete")
        self.delete_button.place(x=240, y=400)

        self.clearbutton = customtkinter.CTkButton(self, command=lambda:self.clear_supplier(True), text="Clear")
        self.clearbutton.place(x=410, y=400)

        self.tabview = customtkinter.CTkTabview(self, width=250)

        self.style = ttk.Style(self)

        self.style.theme_use('clam')
        self.style.configure('Treeview', font=custom_font2, foreground='#fff', background='#0A0B0C', fieldbackground='#1B1B21', rowheight=50)
        self.style.map('Treeview', background=[('selected', '#AA04A7')])

        self.tree_supplier = ttk.Treeview(self, height=20)

        self.tree_supplier['columns'] = ('ID', 'Name', 'Invoice No.', 'Contact', 'Description')

        self.tree_supplier.column('#0', width=0, stretch=tk.NO)
        self.tree_supplier.column('ID', anchor=tk.CENTER, width=220)
        self.tree_supplier.column('Name', anchor=tk.CENTER, width=220)
        self.tree_supplier.column('Invoice No.', anchor=tk.CENTER, width=220)
        self.tree_supplier.column('Contact', anchor=tk.CENTER, width=220)
        self.tree_supplier.column('Description', anchor=tk.CENTER, width=220)

        self.tree_supplier.heading('ID', text="Id")
        self.tree_supplier.heading('Name', text="Name")
        self.tree_supplier.heading('Invoice No.', text="Invoice No.")
        self.tree_supplier.heading('Contact', text="Contact")
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
            self.supplier_entry.insert(0, row[4])
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
            stock_entry = self.supplier_entry.get()
            database.update_supplier(id_entry, name_entry, label_entry, status_entry, stock_entry)
            self.add_to_treeview_supplier()
            self.clear_supplier()
            # self.create_chart()
            messagebox.showinfo('Success', 'Data has been updated')

    def insert_supplier(self):
        id_entry = self.supplierId.get()
        name_entry = self.supplierName.get()
        label_entry = self.invoiceNum.get()
        status_entry = self.contact.get()
        stock_entry = self.supplier_entry.get()
        if not (id_entry and name_entry and label_entry and status_entry and stock_entry):
            messagebox.showerror('Error', 'Enter all fields.')
        elif database.id_exists(id_entry):
            messagebox.showerror('Error', "Id already exists.")
        else:
            try:
                database.insert_supplier(id_entry, name_entry, label_entry, status_entry, stock_entry)
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
        self.supplier_entry.delete(0,END)
        self.supplier_entry.configure(placeholder_text = "Description")


    def add_to_treeview_supplier(self):
        products = database.fetch_supplier()
        self.tree_supplier.delete(*self.tree_supplier.get_children())
        for i in products:
            self.tree_supplier.insert('', END, values=i)



if __name__ == "__main__":
    app = App()
    app.home()
    app.mainloop()