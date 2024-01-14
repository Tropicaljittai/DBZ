# import tkinter as tk

# from tkinter import ttk

# from views.LoginPage import Login
# from views.SignUp import SignUp
# from views.dashboard import dashboard

# class MainApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         # title
#         self.title("Your Application Title")
#         self.geometry("1440x778")

#         # creating a frame and assigning it to container
#         container = tk.Frame(self)s
#         container.pack(side="top", fill="both", expand=True)

#         # configuring the location of the container using grid
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         # dictionary of frames
#         self.frames = {}
#         for F in (SignUp,Login):
#             frame = F(container, self)
#             self.frames[F.__name__] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame("Login"

#     def show_frame(self, cont):
#         # for frame in self.frames.values():
#         #     frame.grid_remove()
#         # frame = self.frames[page_name]
#         # frame.grid()
#         # frame.tkraise()

#         frame = self.frames[cont]
#         # raises the current frame to the top
#         frame.tkraise()

# if __name__ == "__main__":
#     app = MainApp()
#     app.mainloop()

from models.main import Model
from views.main import View
from controllers.main import Controller

def main():
    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.start()
   


if __name__ == "__main__":
    main()
    