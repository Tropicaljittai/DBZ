import tkinter as tk
from tkinter import ttk
import locale
import matplotlib.pyplot as plt



from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["dashboard"]
        self._bind()

    
        self.model.auth.add_event_listener("dashboardChanged", self.dashboardChanged_listener)

    def _bind(self):
   
        self.frame.logOutBtn.config(command=self.model.auth.logout)
        self.frame.userIcon_Btn.config(command=self.go_to_details)
        self.frame.customerBtn.config(command=self.go_to_cust)
        self.frame.productsBtn.config(command=self.go_to_products)

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

    


 
        # Rest of your code for plotting the chart


    def dashboardChanged_listener(self, data=None):
        current_user = self.model.auth.current_user
        if current_user:
            CompanyName = current_user["CompanyName"]
            locale.setlocale(locale.LC_ALL, 'en_ID.UTF-8')

            Balance = self.model.auth.latestFinancialInfo["Balance"]
            revenue = self.model.auth.latestFinancialInfo["Revenue"]
            budget = self.model.auth.latestFinancialInfo["Budget"]
            expense = self.model.auth.latestFinancialInfo["Expenses"]
            theBalance = locale.currency(Balance, grouping=True)
            profit = revenue/expense *100

            if expense != 0:
                profit_percentage = ((revenue - expense) / expense) * 100
            else:
                profit_percentage = 0  # Avoid division by zero
        
            self.frame.greeting.config(text=f"Welcome, {CompanyName}")
            self.frame.userIcon_Btn.place(x=1343.0, y=13.0, width=54.0, height=45.0)
            self.frame.Balance.config(text=theBalance)
            self.frame.revenue.config(text=locale.currency(revenue, grouping=True))
            self.frame.budget.config(text=locale.currency(budget, grouping=True))
            self.frame.profit.config(text=f"{round(profit_percentage,1)}%")

           
 
        else:
            self.frame.greeting.config(text="")
            self.frame.Balance.config(text="")
            self.frame.revenue.config(text="")
            self.frame.budget.config(text="")
            self.frame.profit.config(text="")


  
  
