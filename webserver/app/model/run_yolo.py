import cv2
from ultralytics import YOLO
import numpy as np


# TODO run_yolo prints something every time it runs. Is there some way to shut it 
#  up? Would this work?
# import logging
# logging.getLogger('ultralytics').setLevel(logging.ERROR)

model = YOLO("./app/model/binaries/yolo11x.pt")

# TODO This seems extremely dubious for performance. Is the model loaded every 
#  time? Could this only be loaded upon initialization?
# TODO now it is loaded only upon initialization by moving the line above I 
#  think. Still more testing to be done.
def run_yolo(f):

    
    #change the default path to dataset.yaml
    class_names = model.names
    # print(class_names)

    # TODO is this right for when we have a gpu?
    model.to('cpu')

    # Perform object detection
    image = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
    
    results = model(image)
        # print(result.boxes.map50)

    ret = []

    # Access the first image result (if you're processing multiple images, iterate over them)
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)  # Class ID of the detected object

            # convert cls id to class name
            cls_name = class_names[cls]


            x_center, y_center, width, height = box.xywhn[0]  # Normalized x_center, y_center, width, height

            # Print the result in YOLO label file format: class_id x_center y_center width height (all normalized)
            # print(f'{cls_name} {x_center} {y_center} {width} {height}')
            ret.append((cls_name, x_center, y_center, width, height))

    # access the labels from the result
    # print(result.labels)

    # Display the image with detections
    # result.show()

    
    # Sample code draw boxes
    # # f.seek(0)
    # draw_boxes(f, ret)
    # f is a file handle to the image you want to run yolo on
    
    # [write the code to run the yolo here]

    # This code now returns a list of yolo output tuples
    return ret


if __name__ == "__main__":
    with open("./binaries/testimg3.jpg", 'rb') as image_file:

        run_yolo(image_file)