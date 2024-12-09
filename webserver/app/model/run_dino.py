# import numpy as np
# import cv2
# from io import BytesIO
from PIL import Image
import requests


dino_server_ip = '172.24.156.5'
dino_inf_endpoint = f'http://{dino_server_ip}:3999/ask_abadi'

dino_confidence_threshold = 0.30

# WARNING: Many things here seem brittle
#  I noticed that all the categories seemed offset at some point when things got
#  displayed on the website. It turns out that the category input format 
#  ('obj1 . obj2 . obj3 ...') was not deterministic, and I had a very hard time
#  finding out what categories actually corresponded to the numbers. I feel like
#  there should still be a better way to do this, but I don't know how. Be very
#  careful when changing things, take not when the inferences seem wrong.




# This is the full Coco list manually written. I have run into some issues where
#  DINO does not recognize some of the objects, causing all of the categories to
#  be offset, and have none of the inferences make sense.
# dino_obj_list = ['person', 
#                  'bicycle', 
#                  'car', 
#                  'motorcycle',
#                  'airplane',
#                  'bus',
#                  'train',
#                  'truck',
#                  'boat',
#                  'traffic light',
#                  'fire hydrant',
#                  'street sign',
#                  'stop sign',
#                  'parking meter',
#                  'bench',
#                  'bird',
#                  'cat',
#                  'dog',
#                  'horse',
#                  'sheep',
#                  'cow',
#                  'elephant',
#                  'bear',
#                  'zebra',
#                  'giraffe',
#                  'hat',
#                  'backpack',
#                  'umbrella',
#                  'shoe',
#                  'eye glasses',
#                  'handbag',
#                  'tie',
#                  'suitcase',
#                  'frisbee',
#                  'skis',
#                  'snowboard',
#                  'sports ball',
#                  'kite',
#                  'baseball bat',
#                  'baseball glove',
#                  'skateboard',
#                  'surfboard',
#                  'tennis racket',
#                  'bottle',
#                  'plate',
#                  'wine glass',
#                  'cup',
#                  'fork',
#                  'knife',
#                  'spoon',
#                  'bowl',
#                  'banana',
#                  'apple',
#                  'sandwich',
#                  'orange',
#                  'broccoli',
#                  'carrot',
#                  'hot dog',
#                  'pizza',
#                  'donut',
#                  'cake',
#                  'chair',
#                  'couch',
#                  'potted plant',
#                  'bed',
#                  'mirror',
#                  'dining table',
#                  'window',
#                  'desk',
#                  'toilet',
#                  'door',
#                  'tv',
#                  'laptop',
#                  'mouse',
#                  'remote',
#                  'keyboard',
#                  'cell phone',
#                  'microwave',
#                  'oven',
#                  'toaster',
#                  'sink',
#                  'refrigerator',
#                  'blender',
#                  'book',
#                  'clock',
#                  'vase',
#                  'scissors',
#                  'teddy bear',
#                  'hair drier',
#                  'toothbrush',
#                  'hair brush']

# READ ABOVE!!! 
# If inferences don't make sense, check to see if DINO server is recognizing the 
#  words in its 'noun_phrases'
# Be careful when changing this!!!
dino_obj_list = ['hat',
                 'marker'
                 'backpack',
                 'umbrella',
                 'shoe',
                 'eye glasses',
                 'handbag',
                 'suitcase',
                 'bottle',
                 'plate',
                 'cup',
                 'fork',
                 'knife',
                 'spoon',
                 'bowl',
                 'chair',
                 'bed',
                 'mirror',
                 'dining table',
                 'window',
                 'desk',
                 'door',
                 'tv',
                 'laptop',
                 'mouse',
                 'remote',
                 'keyboard',
                 'cell phone',
                 'book',
                 'clock',
                 'hair brush',
                 'person', 
                 'bicycle',
                 'pencil',
                 'watch'
                 'bench',
                 'wallet']

def format_texts_lists(texts_lists):
    texts = ""
    for text in texts_lists:
        texts = texts + text + " . "
    return texts

def do_infs(img_handle, texts_lists):
    # print(format_texts_lists(texts_lists))

    files = {"file": img_handle}
    data = {"texts": format_texts_lists(texts_lists)}
    
    response = requests.post(dino_inf_endpoint, files=files, data=data)

    if response.status_code == 200:
        # request was successful
        return response.json()
    else:
        return None


def bbox_to_yolo(bbox, image_height, image_width):
    """
    Convert a bounding box from [x1, y1, x2, y2] format to YOLO format.

    Parameters:
        bbox (list or tuple): Bounding box in [x1, y1, x2, y2] format.
        image_width (int): Width of the image in pixels.
        image_height (int): Height of the image in pixels.

    Returns:
        tuple: Bounding box in YOLO format (x_center, y_center, width, height),
               where values are normalized to the range [0, 1].
    """
    x1, y1, x2, y2 = bbox

    # Calculate the center of the bounding box
    x_center = (x1 + x2) / 2
    y_center = (y1 + y2) / 2

    # Calculate the width and height of the bounding box
    box_width = x2 - x1
    box_height = y2 - y1

    # Normalize coordinates to the range [0, 1]
    x_center /= image_width
    y_center /= image_height
    box_width /= image_width
    box_height /= image_height

    return (x_center, y_center, box_width, box_height)


def parse_infs(infs, height, width):
    (infs, noun_phrases) = infs
    # ========Structure:========
    # predictions:
    #   scores, labels, bboxes
    # visualizations
    #   useless

    preds = infs['predictions']
    preds = preds[0]

    labels = preds['labels']
    bboxes = preds['bboxes']

    objs = []

    for idx, val in enumerate(preds['scores']):
        if val > dino_confidence_threshold:
            label = noun_phrases[labels[idx]]

            bbox = bboxes[idx]
            # print(f"{label}  {bbox}")
            (x_center, y_center, box_width, box_height) = bbox_to_yolo(bbox, height, width)

            objs.append((label, x_center, y_center, box_width, box_height))
    

    return objs

def run_yolo(f):
    image = Image.open(f)
    width, height = image.size

    f.seek(0)

    infs = do_infs(f,dino_obj_list)
    # print(infs)

    if infs == None:
        return None
    
    parsed_infs = parse_infs(infs, height, width)

    return parsed_infs

