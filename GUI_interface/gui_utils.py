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
    frame1.place(anchor=W, relx=0.52, rely=0.47)

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

def transform_constraint(user_constraint):
    return 'has_' + user_constraint + '(_,_)'

def insert_constraint_box(win, dataset):

    def process_constraint():
        inputValue=Textbox.get("1.0","end-1c")
        user_constraint = transform_constraint(inputValue)
        add_constraint(dataset, constraint_predicate=user_constraint)
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
    rect.place(anchor=W, relx=0.52, rely=0.47)

def delete_existing_constraints(dataset='hans'):
    lines = []
    path = f'aleph_input/{dataset}_aleph.bk'
    with open(path, 'r') as fp:
        lines = fp.readlines()
    
    # write file
    with open(path, 'w') as fp:
        for line in lines:
            if line[0:5] != 'false' and line[0:10] != 'hypothesis':
                fp.write(line)

# Add a reset button
def insert_reset_button(win):
    resetButton = Button(win,text = "Reset", command=delete_existing_constraints)
    resetButton.place(relx= .1, rely= .5, anchor= E)
    resetButton.pack()

def transform_clause(og_clause):
    '''Transforms clause to natural language'''

    clause = list(set(og_clause))

    # find ALL THE first contains predicate
    contains_preds = [i for i in clause if 'contains' in i]
    nl_clause = ''
    for object_predicate in contains_preds:
        # add an "image contains an object X" sentence
        clause.remove(object_predicate)
        var = object_predicate.rpartition('contains(')[2].rpartition(', ')[0]
        nl_clause = nl_clause + f"Image contains an object {var}"

        # search for the elements in the clause containing that variable
        # for each element: add the attribute and the attribute value
        attribute_preds = [i for i in clause if var in i]
        for idx, predicate in enumerate(attribute_preds):
            attribute = predicate.rpartition('('+var)[0].rpartition('has_')[2]
            att_value = predicate.rpartition(var+', ')[2][:-1]

            if len(attribute_preds) > 1 and idx == 0:
                nl_clause = nl_clause + f" with {attribute} {att_value}"
            elif len(attribute_preds) == 1 and idx ==0:
                nl_clause = nl_clause + f" with {attribute} {att_value}. "
            elif idx+1 == len(attribute_preds) and idx > 0:
                nl_clause = nl_clause + f" and {attribute} {att_value}.\n"
            else:
                nl_clause = nl_clause + f" and {attribute} {att_value}"
            
    return nl_clause