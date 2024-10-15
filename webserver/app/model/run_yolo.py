import cv2
from ultralytics import YOLO
import numpy as np



def run_yolo(f):

    model = YOLO("yolo11n.pt")
    
    #change the default path to dataset.yaml
    

    model.to('cpu')

    # Perform object detection
    image = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
    
    results = model(image)
        # print(result.boxes.map50)
    # Access the first image result (if you're processing multiple images, iterate over them)
    for result in results:
        for box in result.boxes:
            # print out cls label and bbox coords
            print(box.cls, box.xyxy)
    

    # access the labels from the result
    # print(result.labels)

    # Display the image with detections
    result.show()

    
    # f is a file handle to the image you want to run yolo on
    
    # [write the code to run the yolo here]

    # This code should return a file path to the yolo text file output


if __name__ == "__main__":
    with open("./binaries/swaglab.jpg", 'rb') as image_file:

        run_yolo(image_file)