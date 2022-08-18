from tkinter import *
from PIL import ImageTk, Image
import tkinter.scrolledtext as scrolledtext

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
win.geometry("1000x400")

frame1 = Frame(win, width=350, height=200)
frame1.pack()
frame1.place(anchor=W, relx=0.5, rely=0.5)

# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("demo_image.png"))

# Create a Label Widget to display the Image
clevr_image = Label(frame1, image = img)
clevr_image.pack()

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

# Constrain Box
# Theory frame
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


win.mainloop()