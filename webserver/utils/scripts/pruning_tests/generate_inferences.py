import cv2
from ultralytics import YOLO
import numpy as np
import os
import pickle


# modularity would have been nice

# instead, we copy paste


model = YOLO("./uncommitted/yolo11l.pt")


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


    # This code now returns a list of yolo output tuples
    return ret

def extract_number(file_path):
    # Strip the path and extract the filename
    filename = file_path.split('/')[-1]  # Get the part after the last '/'
    number_str = filename[len('image_'):-len('.jpg')]  # Extract the number part
    return int(number_str)  # Return the number as an integer

def get_dataset_imgs_list(directory):
    img_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                img_list.append(file_path)
    img_list = sorted(img_list, key=extract_number)

    return img_list



def main():
    img_list = get_dataset_imgs_list("../../imgs/dataset_0")
    # print(img_list)

    img_inferences = []
    for img_path in img_list:
        with open(img_path, "rb") as img_handle:
            # inferences is a list of obj,coord
            inferences = run_yolo(img_handle)
            # print(inferences)
            img_inferences.append((img_path, inferences))

    with open("uncommitted/inferences.pkl", "wb") as f:
        pickle.dump(img_inferences, f)

    # # to load
    # with open("uncommitted/inferences.pkl", "rb") as f:
    #     for  inf in pickle.load(f):
    #         print(inf)






if __name__ == "__main__":
    main()
