from tkinter import *
from PIL import ImageTk, Image
import tkinter.scrolledtext as scrolledtext

# Create an instance of tkinter window and define geometry
win = Tk()
win.title('ILP CLEVR-HANS')
win.geometry("1000x400")

image_filename = "demo_image.png"
img = ImageTk.PhotoImage(Image.open(image_filename))

def insert_image(win, img):
    frame1 = Frame(win, width=350, height=200)
    frame1.pack()
    frame1.place(anchor=W, relx=0.5, rely=0.5)

    clevr_image = Label(frame1, image = img)
    clevr_image.pack()

def insert_pred_box(win):
    # Theory frame
    frame2 = Frame(win, width=350, height=200)
    frame2.pack()
    frame2.place(anchor=E, relx=0.40, rely=0.2)

    # create a label widget to display text
    exp_label = Label(frame2, text = "Prediction and explanation")
    exp_label.pack()
    Textbox = scrolledtext.ScrolledText(frame2, height = 5, width = 52)
    Textbox.pack()

    # insert theory text
    Fact = """This is a demo explanation.\nTesting capabilities.
    \nThis is a demo explanation.\nTesting capabilities.\n
    This is a demo explanation.\nTesting capabilities.\n
    This is a demo explanation.\nTesting capabilities"""
    Textbox.insert(END, Fact)

def insert_constraint_box(win):
    frame3 = Frame(win, width=350, height=200)
    frame3.pack()
    frame3.place(anchor=E, relx=0.40, rely=0.6)

    # create a label widget to display text
    exp_label = Label(frame3, text = "Constraint")
    exp_label.pack()
    Textbox = scrolledtext.ScrolledText(frame3, height = 5, width = 52)
    Textbox.pack()

    # insert theory text
    Fact = """Insert constraint here."""
    Textbox.insert(END, Fact)

insert_image(win, img)
insert_pred_box(win)
insert_constraint_box(win)


win.mainloop()