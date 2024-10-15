import cv2
from ultralytics import YOLO
import numpy as np



def run_yolo(f):

    model = YOLO("yolo11n.pt")
    
    #change the default path to dataset.yaml
    class_names = model.names
    # print(class_names)

    model.to('cpu')

    # Perform object detection
    image = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
    
    results = model(image)
        # print(result.boxes.map50)
    # Access the first image result (if you're processing multiple images, iterate over them)
    for result in results:
        for box in result.boxes:
            cls = int(box.cls)  # Class ID of the detected object

            # convert cls id to class name
            cls_name = class_names[cls]


            x_center, y_center, width, height = box.xywhn[0]  # Normalized x_center, y_center, width, height

            # Print the result in YOLO label file format: class_id x_center y_center width height (all normalized)
            print(f'{cls_name} {x_center} {y_center} {width} {height}')

    # access the labels from the result
    # print(result.labels)

    # Display the image with detections
    result.show()

    
    # f is a file handle to the image you want to run yolo on
    
    # [write the code to run the yolo here]

    # This code should return a file path to the yolo text file output


if __name__ == "__main__":
    with open("./binaries/testimg3.jpg", 'rb') as image_file:

        run_yolo(image_file)