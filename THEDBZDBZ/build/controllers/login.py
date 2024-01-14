import tkinter as tk
class LogInController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["login"]
        self._bind()


    def _bind(self):
        # self.frame.login_btn.config(command=self.login)
        self.frame.signUpBtn.config(command=self.signup)
        self.frame.togglePassword.config(command=self.toggle_password)
        self.frame.signInBtn.config(command = self.login)


    def signup(self):
        self.view.switch("signup")


    def login(self):
        email= self.frame.emailEntry.get()
        password = self.frame.passwordEntry.get()
        data = {"email": email,"password":password}
        if self.model.auth.authenticate_user(data) == True:
            message = "Logged in"
            tk.messagebox.showinfo("success",message)
            user = self.model.database.getUser_fromEmail(email)
            self.model.auth.login(user)
            print(self.model.auth.is_logged_in)
            print(self.model.auth.current_user)
            print(self.model.auth.latestFinancialInfo)
        else:
            message = "Wrong email or password"
            tk.messagebox.showwarning("Error", message)
        
           


    def toggle_password(self):
        if self.frame.passwordEntry.cget('show') == '*':
            self.frame.passwordEntry.config(show='') 
        else:
            self.frame.passwordEntry.config(show='*')
    


            