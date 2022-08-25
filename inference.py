from pyswip import Prolog
from mrcnn.visualize import *

def clean_theory(theory):
    clean_theory = []
    for i in range(0,len(theory)-1):
        if ':-' not in theory[i+1]:
                rule = theory[i].strip().replace('\n', '') + ' ' + theory[i+1].strip().replace('\n', '')
                clean_theory.append(rule)
    
    return clean_theory

def merge_lines(clean_theory):
    # Tidy up to ensure all rules begin with head :- body
    full_theory = []
    if len(clean_theory) > 1:
        for i in range(0,len(clean_theory)-1):
            if ':-' not in clean_theory[i+1]:
                    rule = clean_theory[i] + ' ' + clean_theory[i+1]
                    full_theory.append(rule)
            elif ':-' in clean_theory[i]:
                full_theory.append(clean_theory[i])

    else:
        full_theory = clean_theory

    return list(set(full_theory))

def add_variable(full_theory):
    new_theory = []
    for rule in full_theory:
        head = 'true_class(A,EX) :-'
        body = rule.rpartition(':-')[2][:-1]

        new_body = body + ', Ex = ' + f'({body}).'
        new_clause = head + new_body

        new_theory.append(new_clause)
    
    return new_theory
    
def save_ruleset_to_prolog(dataset, filename, full_theory):
    file = open(filename, 'w')
    file.write(f':-consult("aleph_input/{dataset}_aleph.bk").\n')
    file.write("\n")

    for rule in full_theory:
        head = 'true_class(A,Ex) :-'
        body = rule.rpartition(':-')[2][:-1]

        file.write(head + "\n")
        file.write("    " + body + ",\n")
        file.write("    Ex = " + f"[{body.strip()}].\n")
        file.write("\n")

    file.close()        

def translate_theory(dataset, filename = 'working_theory.pl'):

    with open(f'{dataset}_theory.txt') as f:
        theory = f.readlines()
    
    theory = clean_theory(theory)
    theory = merge_lines(theory)
    save_ruleset_to_prolog(dataset, filename, theory)
    return theory

def single_instance_inference(dataset, example_number, prolog):
    # theory = translate_theory(dataset = dataset)
    prolog.consult("working_theory.pl")
    result = list(prolog.query(f"true_class(example_{example_number}, Explanation)"))

    # Extract prediction and explanation
    if len(result) == 0:
        pred = 'Negative Class'
        explanation = None
    elif len(result) == 1:
        pred = 'Positive Class'
        explanation = result[0]['Explanation']
    else: # need to fix this - why is some len 1 and others more?
        pred = 'Positive Class'
        explanation = result[0]['Explanation']

    return (pred, explanation)

def add_constraint(dataset, constraint_predicate):
    """Currently just removes a predicate from a theory"""
    output_directory = 'aleph_input'
    bk_file = open(output_directory + '/' + dataset + '_aleph.bk', 'a')
    bk_file.write(f"false :- hypothesis(_,Body,_), bodyList(Body, List), !, member({constraint_predicate}, List).\n\n")
    
    bk_file.close()

def ilp_induce(dataset, prolog):
    # generate initial ILP thoery and save to a file
    prolog.consult('aleph6.pl')
    list(prolog.query(f"read_all('aleph_input/{dataset}_aleph')."))
    list(prolog.query("induce."))
    list(prolog.query(f"write_rules('{dataset}_theory.txt')."))

def generate_mrcnn_output(image, boxes, masks, class_ids, class_names,
                      mrcnn_filename = 'mrcnn_output.png', scores=None, title="",
                      figsize=(36, 32), ax=None,
                      show_mask=True, show_bbox=True,
                      colors=None, captions=None):
    """
    boxes: [num_instance, (y1, x1, y2, x2, class_id)] in image coordinates.
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = boxes.shape[0]
    if not N:
        print("\n*** No instances to display *** \n")
    else:
        assert boxes.shape[0] == masks.shape[-1] == class_ids.shape[0]

    # If no axis is passed, create one and automatically call show()
    auto_show = False
    if not ax:
        fig, ax = plt.subplots(1, figsize=figsize)
        # auto_show = True

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(N):
        color = colors[i]

        # Bounding box
        if not np.any(boxes[i]):
            # Skip this instance. Has no bbox. Likely lost in image cropping.
            continue
        y1, x1, y2, x2 = boxes[i]
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2,
                                alpha=0.7, linestyle="dashed",
                                edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")

        # Mask
        mask = masks[:, :, i]
        if show_mask:
            masked_image = apply_mask(masked_image, mask, color)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros(
            (mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)

    ax.imshow(masked_image.astype(np.uint8))
    fig.savefig(mrcnn_filename)
