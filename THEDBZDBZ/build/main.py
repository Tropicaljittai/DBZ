import tkinter as tk

from tkinter import ttk

from pages.LoginPage import Login
from pages.SignUp import SignUp
from pages.dashboard import dashboard



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Your Application Title")
        self.geometry("1440x778")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SignUp,Login):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Login")

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()

