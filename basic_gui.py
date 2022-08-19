from tkinter import *
from PIL import ImageTk, Image
from GUI_interface.gui_utils import *
from inference import *

win = Tk()
title = 'ILP CLEVR-HANS'
win.title(title)
win.geometry("1000x400")

image_filename = "GUI_interface/demo_image.png"
img = ImageTk.PhotoImage(Image.open(image_filename))


insert_image(win, img)

# get initial prediction
dataset = 'hans'
prolog = Prolog()
ilp_induce(dataset, prolog)
pred, explanation = single_instance_inference(dataset=dataset, example_number=3, prolog=prolog)

insert_pred_box(win, prediction=pred, explanation=explanation)


insert_constraint_box(win)


win.mainloop()