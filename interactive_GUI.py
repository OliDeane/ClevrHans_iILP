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
win.geometry("1000x500")

def run_induce():
    ilp_induce(dataset, prolog)
    theory = translate_theory(dataset='hans')
    insert_theory_box(win, theory=theory)

# get user-defined image number
def select_img_and_run(win):
    def display_selected_image():
        inputValue=Textbox.get("1.0","end-1c")
        image_filename = f"GUI_interface/demo_images/image_{inputValue}.png"
        loaded_img = Image.open(image_filename)
        resized_image= loaded_img.resize((400,250), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(resized_image)
        #Resize the Image using resize method

        insert_image(win, img)
        pred, exp = single_instance_inference(dataset, inputValue, prolog)
        nl_exp = transform_clause(exp)
        print(nl_exp)
        insert_pred_box(win, prediction=pred, explanation=nl_exp)

    # Select image frame
    frame = Frame(win, width=350, height=50)
    frame.pack()
    frame.place(anchor=W, relx=0.60, rely=0.9)

    # create a label widget to display text
    exp_label = Label(frame, text = "Select Image")
    exp_label.pack()
    Textbox = Text(frame, height = 1, width = 32)
    Textbox.pack()

    # Add button for selecting an image
    imageButton = Button(frame,
                        text = "Run Inference", command=display_selected_image)
    imageButton.pack()


# learn model on button press
induceButton = Button(win,text = "Induce", command=run_induce)
induceButton.place(relx= .7, rely= .5, anchor= CENTER)
induceButton.pack()

insert_reset_button(win)
insert_placeholder_box(win)
select_img_and_run(win)
insert_theory_box(win, theory = 'Press INDUCE to generate a working theory...')
insert_pred_box(win, prediction='', explanation='')
insert_constraint_box(win, dataset)

win.mainloop()