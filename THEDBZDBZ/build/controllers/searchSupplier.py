class searchSupplierController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["searchSupplier"]
        self.frame.tree.bind("<ButtonRelease-1>", lambda event: self.on_treeview_click(event))
        # self._bind()
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
       

    def populate_treeview(self):
        try:
            suppliers_data = self.model.database.getAll_suppliers()

            if suppliers_data is not None:
                self.frame.tree.delete(*self.frame.tree.get_children())

                for data in suppliers_data:
                    supplier_info = self.model.database.getSupplierData(data)

                    if supplier_info is not None:
                        print(f"Supplier Info: {supplier_info}")

                        # Handle None values and provide default values or placeholders
                        values = (
                            supplier_info.get('CompanyName', ''),
                            supplier_info.get('Contact', ''),  # Use empty string if 'Contact' is None
                            supplier_info.get('EmailAddress', ''),
                            supplier_info.get('Address', ''),
                            supplier_info.get('Description', '') 
                        )

                        print(f"Inserting values: {values}")

                        self.frame.tree.insert('', "end", values=values)
                    else:
                        print("Supplier Info is None")
            else:
                print("Suppliers Data is None")
        except Exception as e:
            print(f"Error in populate_treeview: {e}")

    def on_treeview_click(self, event):

        selected = self.frame.tree.item(self.frame.tree.selection())
        email = selected['values'][2] if selected['values'] else None
        self.model.auth.selectSupplier(email)
        self.view.switch("orderSupply")





