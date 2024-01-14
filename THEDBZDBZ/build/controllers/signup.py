import tkinter as tk
import bcrypt
from models.database import Database


class SignUpController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["signup"]
        self._bind()

    def _bind(self):
        self.frame.backBtn.config(command=self.back)
        self.frame.togglePassBtn.config(command=self.toggle_password)
        self.frame.signUpBtn.config(command=self.createUser)
        
        
    def back(self):
        self.view.switch("login")

    def toggle_password(self):
        if self.frame.passwordEntry.cget('show') == '*':
            self.frame.passwordEntry.config(show='') 
        else:
            self.frame.passwordEntry.config(show='*')

    def hash_password(self,password):
            # Hash a password for the first time
            # (Using bcrypt, the salt is saved into the hash itself)
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed
    
    def check_entry(self, entries):
        for i in entries:
            entry_text = i.get()
            if not entry_text:
                return False
        return True

    def createUser(self):
        userEmail = self.frame.emailEntry
        userPassword = self.frame.passwordEntry
        companyName = self.frame.nameEntry
        address = self.frame.addressEntry
        businessType = self.frame.combobox

        entries = [userEmail, userPassword, companyName, address, businessType]

        if self.model.database.email_exists(userEmail.get()):
            message = "Email taken, please use another email or log in with an existing email"
            tk.messagebox.showwarning("Error", message)
            return
        else:
            if self.check_entry(entries):
                hashed_password = self.hash_password(userPassword.get())
                self.model.database.insert_user(
                    companyName.get(), hashed_password, businessType.get(), userEmail.get(), address.get()
                )
                message = "Account created succesfully!"
                tk.messagebox.showwarning("Signed Up!", message)
                
               
                user = self.model.database.getUser_fromEmail(userEmail.get())
                self.model.auth.login(user)
                print(self.model.auth.current_user)
            else:
                message = "Please fill in all the entries!!"
                tk.messagebox.showwarning("Error", message)



            
    
        

    
        
        
         
    
   

    



    # def login(self):
    #     self.view.switch("login")

    # def signup(self):
    #     data = {
    #         "fullname": self.frame.fullname_input.get(),
    #         "username": self.frame.username_input.get(),
    #         "password": self.frame.password_input.get(),
    #     }
    #     print(data)
    #     self.model.auth.login(data)