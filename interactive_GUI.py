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
win.geometry("1000x500")
model = load_model(os.getcwd(), config = InferenceConfig(), model_path = "./trained_model/mask_rcnn_clevr_0030_allclasses.h5")
        
def run_induce():
    ilp_induce(dataset, prolog)
    theory = translate_theory(dataset='hans')
    insert_theory_box(win, theory=theory)

# get user-defined image number
def select_img_and_run(win):
    def run_inference():
        inputValue=Textbox.get("1.0","end-1c")
        image_filename = f"GUI_interface/demo_images/image_{inputValue}.png"

        # Display the image
        loaded_img = Image.open(image_filename)
        resized_image= loaded_img.resize((400,250), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized_image)
        insert_image(win, img)


        # Load the image and run inference
        image = skimage.io.imread(image_filename)
        image = image[:,:,:3]
        results = model.detect([image], verbose=0)
        r = results[0]

        # formalise mrcnn output
        shape_categories, material_categories, color_categories,\
        size_categories, class_names = define_object_types()
        img_objects = ([class_names[r['class_ids'][i]] for i in range(len(r['class_ids']))])
        rois = r['rois'].tolist()

        # generate all possible objects (can be moved to outside the function)
        attribute_dict = {'color': list(color_categories.keys()), 'material': list(material_categories.keys()),
                        'size': list(size_categories.keys()), 'shape': list(shape_categories.keys())}
        full_oblist = get_all_objects(attribute_dict)

        # Add the mrcnn instance to the background knowledge file
        bk_file = open(f"aleph_input/{dataset}_aleph.bk",'a')
        bk_file.write("\n")

        # generate an example_id - maybe via the image number provided
        example_id = str(int(inputValue) + 200)

        # add image objects contained

        for object in img_objects:
            shape, material, color, size = object.split()

            # find the index id of the object recognised
            object_idx = full_oblist.index([shape, material, color, size])
            object_id = f'oid_{object_idx}'
            bk_file.write(f"contains({object_id}, example_{example_id}).\n")

        bk_file.close()

        pred, exp = single_instance_inference(dataset, example_id, prolog)

        # Convert to natural language 
        if exp:
            nl_exp = transform_clause(exp)
        else:
            nl_exp = exp

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
                        text = "Run Inference", command=run_inference)
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