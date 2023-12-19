
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Franz\Documents\THEDBZDBZ\build\assets\frame6")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1440x778")
window.configure(bg = "#1E1E1E")


canvas = Canvas(
    window,
    bg = "#1E1E1E",
    height = 778,
    width = 1440,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    281.0,
    28.0,
    anchor="nw",
    text="New Order",
    fill="#F94444",
    font=("ArialRoundedMTBold", 20 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=1343.0,
    y=13.0,
    width=54.0,
    height=45.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=225.0,
    y=23.0,
    width=48.46808624267578,
    height=34.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    574.0,
    419.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    565.0,
    408.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    788.0,
    112.0,
    image=image_image_3
)

canvas.create_text(
    769.0,
    105.0,
    anchor="nw",
    text="Price",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    416.0,
    113.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    326.0,
    113.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    507.0,
    113.0,
    image=image_image_6
)

canvas.create_text(
    381.0,
    105.0,
    anchor="nw",
    text="Product",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

canvas.create_text(
    292.0,
    105.0,
    anchor="nw",
    text="Variant ID",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

canvas.create_text(
    486.0,
    105.0,
    anchor="nw",
    text="Variant",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    597.0,
    113.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    688.0,
    113.0,
    image=image_image_8
)

canvas.create_text(
    664.0,
    105.0,
    anchor="nw",
    text="Quantity",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

canvas.create_text(
    585.0,
    105.0,
    anchor="nw",
    text="Size",
    fill="#F84343",
    font=("ArialRoundedMTBold", 12 * -1)
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    405.0,
    731.0,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    1181.0,
    419.0,
    image=image_image_10
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=821.0,
    y=679.0,
    width=91.0,
    height=30.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=769.0,
    y=716.0,
    width=149.0,
    height=30.0
)

canvas.create_text(
    252.0,
    722.0,
    anchor="nw",
    text="Total Price:",
    fill="#F84343",
    font=("ArialRoundedMTBold", 15 * -1)
)

canvas.create_text(
    553.0,
    706.0,
    anchor="nw",
    text="Customer:",
    fill="#F84343",
    font=("ArialRoundedMTBold", 15 * -1)
)

canvas.create_text(
    962.0,
    95.0,
    anchor="nw",
    text="Your Catalogue",
    fill="#FFFFFF",
    font=("ArialRoundedMTBold", 15 * -1)
)

canvas.create_text(
    503.0,
    732.0,
    anchor="nw",
    text="Payment Method:",
    fill="#F84343",
    font=("ArialRoundedMTBold", 15 * -1)
)

canvas.create_rectangle(
    0.0,
    0.0,
    204.0,
    778.0,
    fill="#2D2D2D",
    outline="")

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=38.0,
    y=642.0,
    width=119.0,
    height=57.0
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    101.0,
    165.0,
    image=image_image_11
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=23.0,
    y=284.0,
    width=135.0,
    height=29.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=25.0,
    y=240.0,
    width=103.0,
    height=35.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=23.0,
    y=196.0,
    width=113.0,
    height=34.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=25.0,
    y=147.0,
    width=103.0,
    height=38.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=25.0,
    y=100.0,
    width=135.0,
    height=32.0
)

canvas.create_text(
    74.0,
    21.0,
    anchor="nw",
    text="DBZ",
    fill="#F94444",
    font=("ArialRoundedMTBold", 24 * -1)
)
window.resizable(False, False)
window.mainloop()
