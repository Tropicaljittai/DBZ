import tkinter as tk


class AccountDetails_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["accountDetails"]
        self._bind()

    def _bind(self):
        self.frame.backBtn.config(command = self.back)
        self.frame.updateBtn.config(command = self.update)
        self.frame.clearBtn.config(command= self.clear)



    def back(self):
        self.view.switch("dashboard")
        self.clear()
        self.update_view()
        
    

    def clear(self):
        entries = [self.frame.emailEntry,self.frame.nameEntry,
            self.frame.phoneEntry,
            self.frame.bankName_entry,
            self.frame.bankNum_entry,
            self.frame.accountHolder_entry,
            self.frame.descriptionEntry,
            self.frame.balanceEntry,
            self.frame.budgetEntry]
        
        for entry in entries:
            entry.delete(0, 'end')

            
    def update_view(self):
        self.frame.emailEntry.insert(0,self.model.auth.current_user["EmailAddress"])
        self.frame.nameEntry.insert(0,self.model.auth.current_user["CompanyName"])
        self.frame.phoneEntry.insert(0,str(self.model.auth.current_user["Contact"]))
        self.frame.bankName_entry.insert(0,str(self.model.auth.current_user["BankName"]))
        self.frame.bankNum_entry.insert(0,str(self.model.auth.current_user["BankNumber"]))
        self.frame.accountHolder_entry.insert(0,str(self.model.auth.current_user["AccountHolder"]))
        self.frame.descriptionEntry.insert(0, str(self.model.auth.current_user["Description"]))

        self.frame.balanceEntry.insert(0,self.model.auth.latestFinancialInfo["Balance"])
        self.frame.budgetEntry.insert(0, self.model.auth.latestFinancialInfo["Budget"])

        if self.model.auth.current_user["IsSupplier"] == 0:
            businessType = "Seller"
        else:
            businessType = "Supplier"
        self.frame.combobox.set(businessType)
        
        
        # Use safe_value for the specific keys you want to display 0


    def update(self):
        companyName = self.frame.nameEntry.get()
        email = self.frame.emailEntry.get()
        phone =  self.frame.phoneEntry.get()
        bankName = self.frame.bankName_entry.get()
        bankNum =  self.frame.bankNum_entry.get()
        accountHolder = self.frame.accountHolder_entry.get()
        description =  self.frame.descriptionEntry.get()
        Type = self.frame.combobox.get()
        if Type == "Supplier":
            IsSupplier = 1
        else:
            IsSupplier = 0
       
        self.model.database.updateUser_details(self.model.auth.current_user["UserID"],companyName,IsSupplier,email,phone ,bankName,bankNum, accountHolder,description)
        self.model.auth.current_user = self.model.database.getUser_fromEmail(email)

        if self.frame.balanceEntry.get() < self.frame.budgetEntry.get():
            message = "Budget cannot be more than your current balance"
            tk.messagebox.showwarning("Error", message)
        else:
            self.model.database.updateFinancial_details(self.model.auth.current_user["UserID"],self.frame.balanceEntry.get(),self.frame.budgetEntry.get())
            self.model.auth.updateDashboard()
            message = "Details Updated"
            tk.messagebox.showinfo("Success", message)

            self.back()

        
        




    
        

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
