# this has working induce. 
# see this link to see how to dsiplay image inrespose to button press:
# https://stackoverflow.com/questions/65656158/displaying-image-on-tkinter-button-click

from tkinter import *
from xml.sax.handler import DTDHandler
from PIL import ImageTk, Image
from GUI_interface.gui_utils import *
from inference import *
import matplotlib.pyplot as plt
prolog = Prolog()
dataset = 'hans'

win = Tk()
title = 'ILP CLEVR-HANS'
win.title(title)
win.geometry("1000x400")

# inputValue = 'demo'
# image_filename = f"GUI_interface/{inputValue}_image.png"
# img = ImageTk.PhotoImage(Image.open(image_filename))
# insert_image(win, img)

def run_induce():
    ilp_induce(dataset, prolog)
    theory = translate_theory(dataset='hans')
    insert_theory_box(win, theory=theory)

# get user-defined image number
def display_selected_image():
    inputValue=Textbox.get("1.0","end-1c")
    image_filename = f"GUI_interface/image_{inputValue}.png"
    img = ImageTk.PhotoImage(Image.open(image_filename))
    insert_image(win, img)
    pred, exp = single_instance_inference(dataset, inputValue, prolog)
    insert_pred_box(win, prediction=pred, explanation=exp)



# learn model on button press
induceButton = Button(win,text = "Induce", command=run_induce)
induceButton.place(relx= .7, rely= .5, anchor= CENTER)
induceButton.pack()

# Select image frame
frame = Frame(win, width=350, height=50)
frame.pack()
frame.place(anchor=W, relx=0.60, rely=0.5)

# create a label widget to display text
exp_label = Label(frame, text = "Select Image")
exp_label.pack()
Textbox = scrolledtext.ScrolledText(frame, height = 2, width = 32)
Textbox.pack()

# Add button for selected an image
imageButton = Button(frame,
                    text = "Run Inference", command=display_selected_image)
imageButton.pack()

# Display theory frame
insert_theory_box(win, theory = 'Press INDUCE to generate a working theory.')
insert_pred_box(win, prediction='', explanation='')
insert_constraint_box(win, dataset)


win.mainloop()