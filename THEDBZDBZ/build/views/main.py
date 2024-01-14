from .root import Root
from .LoginPage import Login
from .SignUp import SignUp
from .dashboard import dashboard
from.accountDetails import accountDetails
from .Products import Products
from .variants import Variants
from .orders import Orders
from .createOrder import createOrder
from .customers import customers
from .supply import supply
from .searchSupplier import searchSupplier
from .orderSupply import orderSupply


class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}

        self._add_frame(SignUp, "signup")
        self._add_frame(Login, "login")
        self._add_frame(dashboard,"dashboard")
        self._add_frame(accountDetails,'accountDetails')
        self._add_frame(Products,'products')
        self._add_frame(Variants,'variants')
        self._add_frame(Orders,"orders")
        self._add_frame(createOrder,"createOrder")
        self._add_frame(customers,"customers")
        self._add_frame(supply, "supply")
        self._add_frame(searchSupplier,"searchSupplier")
        self._add_frame(orderSupply,"orderSupply")
    
     
  

    def _add_frame(self, Frame, name):
        self.frames[name] = Frame(self.root)
        self.frames[name].grid(row=0, column=0, sticky="nsew")
    

    def switch(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def start_mainloop(self):
        self.root.mainloop()