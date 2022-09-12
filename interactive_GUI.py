# this has working induce. 
# see this link to see how to dsiplay image inrespose to button press:
# https://stackoverflow.com/questions/65656158/displaying-image-on-tkinter-button-click

from tkinter import *
from xml.sax.handler import DTDHandler
from PIL import ImageTk, Image
from GUI_interface.gui_utils import *
from inference import *
from inference import *
from PIL import ImageTk, Image
from program_generation.norel_program import *
import skimage
import os

prolog = Prolog()
dataset = 'hans'

win = Tk()
title = 'ILP CLEVR-HANS'
win.title(title)
win.geometry("1050x500")

model = load_model(os.getcwd(), config = InferenceConfig(), model_path = "./trained_model/mask_rcnn_clevr_0030_allclasses.h5")
        
def run_induce():
    ilp_induce(dataset, prolog)
    theory = translate_theory(dataset='hans')
    insert_theory_box(win, theory=theory)

def load_image_for_inference(image_filename):
    # Load the image and run inference
    image = skimage.io.imread(image_filename)
    image = image[:,:,:3]
    results = model.detect([image], verbose=0)
    r = results[0]
    
    return r, image

def extract_image_objects(r):
    shape_categories, material_categories, color_categories,\
    size_categories, class_names = define_object_types()
    img_objects = ([class_names[r['class_ids'][i]] for i in range(len(r['class_ids']))])


    # generate all possible objects (can be moved to outside the function)
    attribute_dict = {'color': list(color_categories.keys()), 'material': list(material_categories.keys()),
                    'size': list(size_categories.keys()), 'shape': list(shape_categories.keys())}
    
    return img_objects, attribute_dict, class_names

def add_to_bk(img_objects, full_oblist, example_id, dataset='hans'):
    # Add the mrcnn instance to the background knowledge file
    bk_file = open(f"aleph_input/{dataset}_aleph.bk",'a')
    bk_file.write("\n")

    # add image objects contained

    for object in img_objects:
        shape, material, color, size = object.split()

        # find the index id of the object recognised
        object_idx = full_oblist.index([shape, material, color, size])
        object_id = f'oid_{object_idx}'
        bk_file.write(f"contains({object_id}, example_{example_id}).\n")

    bk_file.close()

def select_img_and_run(win):
    def display_mrcnn_image(image, boxes, masks, class_ids, class_names):
        image_filename = "GUI_interface/demo_images/mrcnn_output.png"
        generate_mrcnn_output(image, boxes, masks, class_ids, class_names,
                      mrcnn_filename = image_filename, figsize=(8, 8))

        loaded_img = Image.open(image_filename)
        resized_image= loaded_img.resize((400,250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized_image)
        insert_image(win, img)

    def run_inference():
        inputValue=Textbox.get("1.0","end-1c")
        image_filename = f"GUI_interface/demo_images/image_{inputValue}.png"

        r, image = load_image_for_inference(image_filename)

        # formalise mrcnn output
        img_objects, attribute_dict, class_names = extract_image_objects(r)
        full_oblist = get_all_objects(attribute_dict)

        # generate an example_id - maybe via the image number provided
        example_id = str(int(inputValue) + 200)
        add_to_bk(img_objects, full_oblist, example_id)
        pred, exp = single_instance_inference(dataset, example_id, prolog)

        # Convert to natural language 
        if exp:
            nl_exp = transform_clause(exp)
        else:
            nl_exp = exp

        insert_pred_box(win, prediction=pred, explanation=nl_exp)

        display_mrcnn_image(image, r['rois'], r['masks'], r['class_ids'], class_names)

    def display_image():
        inputValue=Textbox.get("1.0","end-1c")
        image_filename = f"GUI_interface/demo_images/image_{inputValue}.png"

        # Display the image
        loaded_img = Image.open(image_filename)
        resized_image= loaded_img.resize((400,250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized_image)
        insert_image(win, img)

    # Select image frame
    frame = Frame(win, width=350, height=50)
    frame.pack()
    frame.place(anchor=W, relx=0.60, rely=0.85)

    # create a label widget to display text
    exp_label = Label(frame)
    exp_label.pack()
    Textbox = Text(frame, height = 1, width = 32)
    Textbox.insert(END, "Insert Image Number")
    Textbox.pack()

    # Add button for selecting an image
    imageButton = Button(frame,
                        text = "Display Image", command=display_image)
    imageButton.pack()


    # Add button for running inference
    inferenceButton = Button(frame,
                        text = "Run Inference", command=run_inference)
    inferenceButton.pack()

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