from tkinter import *
from PIL import ImageTk, Image
import tkinter.scrolledtext as scrolledtext
from inference import *

# Create an instance of tkinter window and define geometry

def create_window(title = 'ILP CLEVR-HANS'):
    '''Currently not functionable'''
    win = Tk()
    win.title(title)
    win.geometry("1000x600")
    return win

def insert_image(win, img):
    frame1 = Frame(win, width=375, height=200)
    frame1.pack()
    frame1.place(anchor=W, relx=0.52, rely=0.45)

    clevr_image = Label(frame1, image = img)
    clevr_image.image = img # need to save reference to the image
    clevr_image.pack()

def insert_pred_box(win, prediction, explanation):
    # Theory frame
    frame2 = Frame(win, width=350, height=150)
    frame2.pack()
    frame2.place(anchor=E, relx=0.40, rely=0.47)

    # create a label widget to display text
    exp_label = Label(frame2, text = "Prediction and explanation")
    exp_label.pack()
    Textbox = scrolledtext.ScrolledText(frame2, height = 5, width = 52)
    Textbox.pack()

    # insert theory text
    text_input = f'Prediction: {prediction} \n\nExplanation: {explanation} \n'

    Textbox.insert(END, text_input)

def insert_constraint_box(win, dataset):

    def process_constraint():
        inputValue=Textbox.get("1.0","end-1c")
        add_constraint(dataset, constraint_predicate=inputValue)
        Textbox.delete("1.0", END)

    frame3 = Frame(win, width=350, height=200)
    frame3.pack()
    frame3.place(anchor=E, relx=0.40, rely=0.8)

    # create a label widget to display text
    exp_label = Label(frame3, text = "Constraint")
    exp_label.pack()
    Textbox = scrolledtext.ScrolledText(frame3, height = 5, width = 52)
    Textbox.pack()

    # insert palceholder text
    Textbox.insert(END, "Insert constraint here.")
    
    # add drop down menu
    options = ["Must not occur in explanation",\
        "Must occur in explanation"]
    sv = options[0]          #<-- setting sv to default item
    
    def _get(cur):         #<-- function to run
        sv = cur

    menu= StringVar()
    menu.set("Select A Constraint")
    drop= OptionMenu(frame3, menu,command = _get, *options)
    drop.pack()

    # Add button
    printButton = Button(frame3,
                        text = "Submit Constraint", command=process_constraint)
    printButton.pack()

def insertion_test(win):

    def printInput():
        inp = inputtxt.get(1.0, "end-1c")
        lbl.config(text = "Provided Input: "+inp)
    
    frame = Frame(win, width=350, height=200)

    # TextBox Creation
    inputtxt = Text(frame,
                    height = 5,
                    width = 20)
    
    inputtxt.pack()
    
    # Button Creation
    printButton = Button(frame,
                            text = "Print", 
                            command = printInput)
    printButton.pack()
    
    # Label Creation
    lbl = Label(frame, text = "")
    lbl.pack()
    frame.mainloop()

def insert_theory_box(win, theory):
    
    # Theory frame
    frame = Frame(win, width=350, height=200)
    frame.pack()
    frame.place(anchor=E, relx=0.40, rely=0.2)

    # create a label widget to display text
    theory_label = Label(frame, text = "Current Theory")
    theory_label.pack()
    Textbox = scrolledtext.ScrolledText(frame, height = 5, width = 52)
    Textbox.pack()
    # insert theory text
    Textbox.insert(END, theory)

def insert_placeholder_box(win):
    rect = Canvas(win, width=400, height=250)
    rect.create_rectangle(10, 10, 400, 250)
    rect.create_text(200,125, text='Select Image')
    rect.pack()
    rect.place(anchor=W, relx=0.52, rely=0.45)

