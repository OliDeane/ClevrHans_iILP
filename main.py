import os
import sys
import random
import math
import numpy as np
import skimage.io
import tensorflow as tf
import os
from tqdm import tqdm

from mrcnn import utils
from mrcnn import visualize
from mrcnn.visualize import display_images
import mrcnn.model as modellib
from mrcnn.model import log
from samples.clevr import clevr
import argparse


class InferenceConfig(clevr.ClevrConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = 0.80
    DETECTION_NMS_THRESHOLD = 0.20

def load_model(ROOT_DIR, config, model_path = './trained_model/mask_rcnn_clevr_0030_allclasses.h5'):

    # Create model object in inference mode.
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

    # Load weights trained on MS-COCO
    model.load_weights(model_path, by_name=True)
    
    return model

def define_object_types():

    shape_categories = {'cube': 1,
                            'sphere': 2,
                            'cylinder': 3}
    material_categories = {'rubber': 1,
                                'metal': 2}
    color_categories = {'gray': 1,
                                'blue': 2,
                                'brown': 3,
                                'yellow': 4,
                                'red': 5,
                                'green': 6,
                                'purple': 7,
                                'cyan': 8}
    size_categories = {'small': 1,
                            'large': 2}
    class_names = ['BG']

    for shape in shape_categories:
        for mat in material_categories:
            for col in color_categories:
                for size in size_categories:
                    class_name = shape + " " + mat + " " + col + " " + size
                    class_names.append(class_name)
    
    return shape_categories, material_categories, color_categories,\
        size_categories, class_names

def open_files(output_filename = 'hans_aleph'):

    output_directory = os.getcwd()

    os.makedirs(ROOT_DIR, exist_ok=True)

    os.makedirs(output_directory, exist_ok=True)

    b_file = open(output_directory + '/' + output_filename + '.b', 'w')
    f_file = open(output_directory + '/' + output_filename + '.f', 'w')
    n_file = open(output_directory + '/' + output_filename + '.n', 'w')
    bk_file = open(output_directory + '/' + output_filename + '.bk', 'w')

    return b_file, f_file, n_file, bk_file

def write_basic_preds(bk_file, color_categories, material_categories, size_categories, shape_categories):

    attribute_dict = {'color': list(color_categories.keys()), 'material': list(material_categories.keys()),
                        'size': list(size_categories.keys()), 'shape': list(shape_categories.keys())}

    for attribute in list(attribute_dict.keys()):
        bk_file.write(f":- discontiguous has_{attribute}/2.\n")
    bk_file.write(f":- discontiguous contains/2.\n")
    bk_file.write(f":- discontiguous right_of/3.\n")
    bk_file.write(f":- discontiguous left_of/3.\n")

    bk_file.write(f":- discontiguous in_front/3.\n")
    bk_file.write(f":- discontiguous behind/3.\n")
    bk_file.write(f":- discontiguous inline_X/3.\n")
    bk_file.write(f":- discontiguous inline_Y/3.\n")

    bk_file.write("\n")

    for category in list(attribute_dict.keys()):
        for attribute in attribute_dict[category]:
            bk_file.write(f"{category}({attribute}).\n")

    bk_file.write("\n")

    return attribute_dict

def get_all_objects(attribute_dict):
    full_oblist = []
    for shape in attribute_dict['shape']:
        for material in attribute_dict['material']:
            for color in attribute_dict['color']:
                for size in attribute_dict['size']:
                    full_oblist.append([shape, material, color, size])
    
    return full_oblist
    
def write_object_preds(bk_file, attribute_dict):

    full_oblist = []
    for shape in attribute_dict['shape']:
        for material in attribute_dict['material']:
            for color in attribute_dict['color']:
                for size in attribute_dict['size']:
                    full_oblist.append([shape, material, color, size])

    object_count = 0 
    for object in full_oblist:
        object_id = f'oid_{object_count}'
        shape, material, color, size = object
        bk_file.write(f"has_shape({object_id}, {shape}).\n")
        bk_file.write(f"has_material({object_id}, {material}).\n")
        bk_file.write(f"has_color({object_id}, {color}).\n")
        bk_file.write(f"has_size({object_id}, {size}).\n")
        bk_file.write(f"\n")
        object_count += 1
    
    return full_oblist

def write_img_facts(bk_file, full_oblist, oblist, centroids):

    example_count = 0
    for img_objects, img_centroids_x, img_centroids_y in zip(oblist, centroids['X'], centroids['Y']):
        bk_file.write("\n")
        example_id = f"example_{example_count}"

        for object in img_objects:
            shape, material, color, size = object.split()

            # find the index id of the object recognised
            object_idx = full_oblist.index([shape, material, color, size])
            object_id = f'oid_{object_idx}'
            bk_file.write(f"contains({object_id}, {example_id}).\n")
        
        rel_preds = get_relation_preds(img_centroids_x, img_centroids_y, full_oblist, example_count, img_objects)
        for pred in rel_preds:
            bk_file.write(pred)
        
        example_count += 1

def close_files(b_file, f_file, n_file, bk_file):
    b_file.close()
    bk_file.close()
    f_file.close()
    n_file.close()

def write_img_object_preds(oblist):
    '''Ignore for now.
    This write predicates for only the object that appear in the training set. NOT for all possible objects'''
    example_count = 0
    object_count = 0
    for img_objects in oblist:
        bk_file.write("\n")
        example_id = f"example_{example_count}"
        example_count += 1

        for object in img_objects:
            object_id = f'oid_{object_count}'
            shape, material, color, size = object.split()
            bk_file.write(f"has_shape({object_id}, {shape}).\n")
            bk_file.write(f"has_material({object_id}, {material}).\n")
            bk_file.write(f"has_color({object_id}, {color}).\n")
            bk_file.write(f"has_size({object_id}, {size}).\n")
            object_count += 1
        
        bk_file.write(f"contains({object_id}, {example_id}).\n")

def inference(IMAGE_DIR, model, class_names):

    file_names = sorted(next(os.walk(IMAGE_DIR))[2])

    if '.DS_Store' in file_names:
        file_names.remove(".DS_Store")

    oblist = []
    ilp_classes = []
    centroids = {'X':[], 'Y':[]}

    print('Detecting objects...')


    for filename in tqdm(file_names):
        image = skimage.io.imread(os.path.join(IMAGE_DIR, filename))
        image = image[:,:,:3]
        results = model.detect([image], verbose=0)
        r = results[0]
        oblist.append([class_names[r['class_ids'][i]] for i in range(len(r['class_ids']))])

        # get centroids
        rois = r['rois'].tolist()
        centroids['X'].append([(roi[1] + roi[3])/2 for roi in rois])
        centroids['Y'].append([(roi[0] + roi[2])/2 for roi in rois])

        ilp_classes.append(f'c{filename[19]}')
    
    return oblist, ilp_classes, centroids

def get_relation_preds(centroidsX, centroidsY, full_oblist, eg_num, img_objects):

    rel_preds = []
    for partner_idx in range(len(centroidsX)):
        for reference_idx in range(len(centroidsX)):

            if partner_idx==reference_idx:
                continue
            
            # ref_id = full_oblist.index(class_names[r['class_ids'][reference_idx]].split())
            # part_id = full_oblist.index(class_names[r['class_ids'][partner_idx]].split())

            ref_id = full_oblist.index(img_objects[reference_idx].split())
            part_id = full_oblist.index(img_objects[partner_idx].split())

            if centroidsX[partner_idx] > centroidsX[reference_idx]:
                x_relation = 'right_of'
            elif centroidsX[partner_idx] < centroidsX[reference_idx]:
                x_relation = 'left_of'
            elif centroidsX[partner_idx] == centroidsX[reference_idx]:
                x_relation = 'inline_X'
            
            if centroidsY[partner_idx] > centroidsY[reference_idx]:
                y_relation = 'in_front'            
            elif centroidsY[partner_idx] < centroidsY[reference_idx]:
                y_relation = 'behind'
            elif centroidsY[partner_idx] == centroidsY[reference_idx]:
                y_relation = 'inline_Y'

            
            rel_preds.append(f'{x_relation}(oid_{ref_id}, oid_{part_id}, example_{eg_num}).\n')
            rel_preds.append(f'{y_relation}(oid_{ref_id}, oid_{part_id}, example_{eg_num}).\n')

    return rel_preds

def write_ground_truths(ilp_classes, f_file, n_file):
    for id in range(0,len(ilp_classes)):
        if ilp_classes[id] == 'c2':
            f_file.write(f"true_class(example_{id}).\n")
        else:
            n_file.write(f"true_class(example_{id}).\n")

def write_aleph_settings(b_file, features = ['shape','material','color','size'], \
    id_column = "oid", output_filename = "hans_aleph"):

    # write settings for Aleph
    b_file.write(":- modeh(1, true_class(+example)).\n")
    b_file.write("\n")

    b_file.write(f":- modeb(*, contains(-{id_column}, +example)).\n")

    # modes
    for feature in features:
        b_file.write(f":- modeb(*, has_{feature}(+{id_column}, #{feature})).\n")

    b_file.write(f":- modeb(*, left_of(+{id_column}, +{id_column}, +example)).\n")
    b_file.write(f":- modeb(*, right_of(+{id_column}, +{id_column}, +example)).\n")

    b_file.write("\n")

    # determinations
    b_file.write(":- determination(true_class/1, contains/2).\n")

    for feature in features:
        b_file.write(f":- determination(true_class/1, has_{feature}/2).\n")
    b_file.write(f":- determination(true_class/1, left_of/3).\n")
    b_file.write(f":- determination(true_class/1, right_of/3).\n")

    # write relations


    b_file.write("\n")
    
    b_file.write(":- set(i,4).\n")
    b_file.write(":- set(verbosity,0).\n")
    b_file.write(":- set(minpos,3).\n")
    b_file.write(":- set(noise,10).\n")
    b_file.write(":- set(clauselength, 20).\n")
    b_file.write(f":- consult('{output_filename + '.bk'}').")

if __name__ == "__main__":

    parser = argparse.ArgumentParser("ibm_aleph")
    parser.add_argument("--model_path", "-MP", help="Path to pre-trained model", type=str, default='./trained_model/mask_rcnn_clevr_0030_allclasses.h5')
    parser.add_argument("--image_path", "-IP", help="Path to CLEVR-HANS images.", type=str, default= './temp_images')
    parser.add_argument("--colab_GPU", "-CGPU", help="State as true if running code on Google Colab (ensures use of colab GPU).", type=str, default= False)
    parser.add_argument("--output_filename", "-OF", help="Name of ALEPH input files.", type=str, default= 'hans_aleph')

    args = parser.parse_args()

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # supresses TF warnings

    ROOT_DIR = os.getcwd()

    print('Loading model...')
    config = InferenceConfig()
    model = load_model(ROOT_DIR, config, model_path = args.model_path)
    shape_categories, material_categories, color_categories,\
        size_categories, class_names = define_object_types()
    print("Done. Model loaded successfully.")

    if args.colab_GPU:
        with tf.device('/device:GPU:0'):
            oblist, ilp_classes, centroids = inference(args.image_path, model, class_names)
    else:
        oblist, ilp_classes, centroids = inference(args.image_path, model, class_names)

    b_file, f_file, n_file, bk_file = open_files(output_filename=args.output_filename)
    write_aleph_settings(b_file, output_filename=args.output_filename)
    attribute_dict = write_basic_preds(bk_file, color_categories, material_categories, size_categories, shape_categories)
    full_oblist = write_object_preds(bk_file, attribute_dict)

    write_img_facts(bk_file, full_oblist, oblist, centroids)
    write_ground_truths(ilp_classes, f_file, n_file)
    close_files(b_file, f_file, n_file, bk_file)
