import fiftyone as fo
import fiftyone.zoo as foz
import os
import random
import argparse
import json
import yaml
import shutil
import cv2
import numpy as np

import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics import settings
import albumentations as A



sourceFolder = ''
train_folder = ''
val_folder = ''
test_folder = ''

# sourceFolder = "F:\Data\\Intermediary\\{}\\val\\"
# train_folder = 'F:\Data\\Final\\train\\{}\\'
# val_folder = 'F:\Data\\Final\\val\\{}\\'
# test_folder = 'F:\Data\\Final\\test\\{}\\'
# 81 labels
# cocoLabelConversion = '[{"supercategory": "person","id": 1,"name": "person"},{"supercategory": "vehicle","id": 2,"name": "bicycle"},{"supercategory": "vehicle","id": 3,"name": "car"},{"supercategory": "vehicle","id": 4,"name": "motorcycle"},{"supercategory": "vehicle","id": 5,"name": "airplane"},{"supercategory": "vehicle","id": 6,"name": "bus"},{"supercategory": "vehicle","id": 7,"name": "train"},{"supercategory": "vehicle","id": 8,"name": "truck"},{"supercategory": "vehicle","id": 9,"name": "boat"},{"supercategory": "outdoor","id": 10,"name": "traffic light"},{"supercategory": "outdoor","id": 11,"name": "fire hydrant"},{"supercategory": "outdoor","id": 13,"name": "stop sign"},{"supercategory": "outdoor","id": 14,"name": "parking meter"},{"supercategory": "outdoor","id": 15,"name": "bench"},{"supercategory": "animal","id": 16,"name": "bird"},{"supercategory": "animal","id": 17,"name": "cat"},{"supercategory": "animal","id": 18,"name": "dog"},{"supercategory": "animal","id": 19,"name": "horse"},{"supercategory": "animal","id": 20,"name": "sheep"},{"supercategory": "animal","id": 21,"name": "cow"},{"supercategory": "animal","id": 22,"name": "elephant"},{"supercategory": "animal","id": 23,"name": "bear"},{"supercategory": "animal","id": 24,"name": "zebra"},{"supercategory": "animal","id": 25,"name": "giraffe"},{"supercategory": "accessory","id": 27,"name": "backpack"},{"supercategory": "accessory","id": 28,"name": "umbrella"},{"supercategory": "accessory","id": 31,"name": "handbag"},{"supercategory": "accessory","id": 32,"name": "tie"},{"supercategory": "accessory","id": 33,"name": "suitcase"},{"supercategory": "sports","id": 34,"name": "frisbee"},{"supercategory": "sports","id": 35,"name": "skis"},{"supercategory": "sports","id": 36,"name": "snowboard"},{"supercategory": "sports","id": 37,"name": "sports ball"},{"supercategory": "sports","id": 38,"name": "kite"},{"supercategory": "sports","id": 39,"name": "baseball bat"},{"supercategory": "sports","id": 40,"name": "baseball glove"},{"supercategory": "sports","id": 41,"name": "skateboard"},{"supercategory": "sports","id": 42,"name": "surfboard"},{"supercategory": "sports","id": 43,"name": "tennis racket"},{"supercategory": "kitchen","id": 44,"name": "bottle"},{"supercategory": "kitchen","id": 46,"name": "wine glass"},{"supercategory": "kitchen","id": 47,"name": "cup"},{"supercategory": "kitchen","id": 48,"name": "fork"},{"supercategory": "kitchen","id": 49,"name": "knife"},{"supercategory": "kitchen","id": 50,"name": "spoon"},{"supercategory": "kitchen","id": 51,"name": "bowl"},{"supercategory": "food","id": 52,"name": "banana"},{"supercategory": "food","id": 53,"name": "apple"},{"supercategory": "food","id": 54,"name": "sandwich"},{"supercategory": "food","id": 55,"name": "orange"},{"supercategory": "food","id": 56,"name": "broccoli"},{"supercategory": "food","id": 57,"name": "carrot"},{"supercategory": "food","id": 58,"name": "hot dog"},{"supercategory": "food","id": 59,"name": "pizza"},{"supercategory": "food","id": 60,"name": "donut"},{"supercategory": "food","id": 61,"name": "cake"},{"supercategory": "furniture","id": 62,"name": "chair"},{"supercategory": "furniture","id": 63,"name": "couch"},{"supercategory": "furniture","id": 64,"name": "potted plant"},{"supercategory": "furniture","id": 65,"name": "bed"},{"supercategory": "furniture","id": 67,"name": "dining table"},{"supercategory": "furniture","id": 70,"name": "toilet"},{"supercategory": "electronic","id": 72,"name": "tv"},{"supercategory": "electronic","id": 73,"name": "laptop"},{"supercategory": "electronic","id": 74,"name": "mouse"},{"supercategory": "electronic","id": 75,"name": "remote"},{"supercategory": "electronic","id": 76,"name": "keyboard"},{"supercategory": "electronic","id": 77,"name": "cell phone"},{"supercategory": "appliance","id": 78,"name": "microwave"},{"supercategory": "appliance","id": 79,"name": "oven"},{"supercategory": "appliance","id": 80,"name": "toaster"},{"supercategory": "appliance","id": 81,"name": "sink"},{"supercategory": "appliance","id": 82,"name": "refrigerator"},{"supercategory": "indoor","id": 84,"name": "book"},{"supercategory": "indoor","id": 85,"name": "clock"},{"supercategory": "indoor","id": 86,"name": "vase"},{"supercategory": "indoor","id": 87,"name": "scissors"},{"supercategory": "indoor","id": 88,"name": "teddy bear"},{"supercategory": "indoor","id": 89,"name": "hair drier"},{"supercategory": "indoor","id": 90,"name": "toothbrush"}]'

# # turn cocoLabelConversion into JSON
# json_obj = json.loads(cocoLabelConversion)


# # intake data.yaml name 
# with open('/app/Intermediary/dataset.yaml', 'r') as stream:
#     try:
#         data = yaml.safe_load(stream)
#     except yaml.YAMLError as exc:
#         print(exc)

# # get data.yaml name
# data_name = data['names']

# # get numbered list of categories
# numberedList = {data_name[i]: i + 1 for i in range(len(data_name))}

# conversionFromJSONToYAML = {}

# for i in range(len(json_obj)):
#     # get name of that category
#     jsonObjName = json_obj[i]["name"]

#     # get id of that category
#     jsonObjID = json_obj[i]["id"]

#     # find that name
#     conversionFromJSONToYAML[int(jsonObjID)] = numberedList[jsonObjName]



# print(conversionFromJSONToYAML)

def downLoadData(initialDataStorageDirectory, middleDataStorageDirectory, split, max_samples):
    
    name = "coco-2017"
    settings['datasets_dir'] = initialDataStorageDirectory
    if max_samples is None:
        dataset = foz.load_zoo_dataset(name, label_types="detections", split=split)
    else:
        dataset = foz.load_zoo_dataset(name, label_types="detections", split=split, max_samples=max_samples)
    # delete and create
    if os.path.exists(middleDataStorageDirectory):
        shutil.rmtree(middleDataStorageDirectory)
    os.makedirs(middleDataStorageDirectory)

    dataset.export(
        export_dir= middleDataStorageDirectory,
        dataset_type=fo.types.YOLOv5Dataset,  # Specify the export format
        label_field="ground_truth",           # Specify the field containing labels (if applicable)
    )


def filterCoco(middleDataStorageDirectory):
    print("in filterCoco")
    # import CategoriesNum.txt file
    # with open('categoriesNum.txt', 'r') as f:
    #     categories = f.readlines()
    #     categories = [int(x.strip()) for x in categories]   
    
    with open('categories.txt', 'r') as f:
        categories = f.readlines()
        categories = [x for x in categories]
        # clearn up the list
        for i in range(len(categories)):
            categories[i] = categories[i].strip()


    sourceFolder = middleDataStorageDirectory + "/{}/val/"

    # Make a list of all nums from 0 to 80 not present in CategoriesNum.txt
    notInList = [x for x in range(0, 81) if x not in categories]   

    # Go through the list of all label files in the "F:\Data\\Intermediary\\labels\\val\\"

    labelsList = os.listdir(sourceFolder.format("labels"))

        # open up the dataset.yaml file
    with open(middleDataStorageDirectory + "/dataset.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        
        # create conversion dictionary of 

        # create conversion dictionary from categories variable to corresponding index in data['names']
        conversionDict = {}
        for i in range(len(data['names'])):
            # check if i is in data['names'] and if so get corresponding index
            if data['names'][i] in categories:
                conversionDict[i] = categories.index(data['names'][i])

    # Go through the list of all label files in the "F:\Data\\Intermediary\\labels\\val\\"

    # For each file, i want to get a list of the first word in the file before the first space on each line

    for labelFile in labelsList:

        with open(sourceFolder.format("labels") + labelFile, 'r') as f:

            lines = f.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].split()[0]

            lines = [int(x) for x in lines]

            # delete the label files and corresponding image files that are not in the CategoriesNum.txt
            shouldDelete = False
            for i in range(len(lines)):
                if lines[i] not in conversionDict.keys():
                    shouldDelete = True
                    break

        if shouldDelete:
            os.remove(sourceFolder.format("labels") + labelFile)
            os.remove(sourceFolder.format("images") + labelFile.replace(".txt", ".jpg"))

    # conversionDict = {categories[i]: i for i in range(len(categories))}
    # print(conversionDict)

    # Modify the label files sourceFolder.format("labels") to have the correct values
    modifyFiles(sourceFolder.format("labels"), conversionDict=conversionDict)

    # Open dataset.yaml file
    with open(middleDataStorageDirectory + "/dataset.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        data['names'] = categories

        print("len(data['names']) : " + str(len(data['names'])))
    # Write the new data to the dataset.yaml file
    with open(middleDataStorageDirectory + "/dataset.yaml", 'w') as f:
        print("dumping")
        yaml.dump(data, f)

def CopyFiles(dataStorageDirectory, middleDataStorageDirectory):
    # delete and create dataStorageDirectory
    if os.path.exists(dataStorageDirectory):
        shutil.rmtree(dataStorageDirectory)
    os.makedirs(dataStorageDirectory)   

    # Take 70% of files in the "F:\Data\\not-initial\\images\\val" folder and move them to the "F:\Data\\Final\\train\images" folder
    trainValTestFolders = ["train", "val", "test"]
    imagesLabels = ["images", "labels"]
    for folder in trainValTestFolders:
        for imageLabel in imagesLabels:
            os.makedirs(os.path.join(dataStorageDirectory, folder, imageLabel), exist_ok=True)

    # Remove all Image files in the "F:\Data\\Intermediary\\images\\val\\"" folder that are also not present in the "F:\Data\\Intermediary\\labels\\val\\" folder
    sourceFolder = middleDataStorageDirectory + "/{}/val/"
    labelsList = os.listdir(sourceFolder.format("labels"))
    imagesList = os.listdir(sourceFolder.format("images"))
    for imageFile in imagesList:
        labelFile = imageFile.replace(".jpg", ".txt")
        if labelFile not in labelsList:
            os.remove(sourceFolder.format("images") + imageFile)


    # shuffle files

    files = os.listdir(sourceFolder.format("images"))

    random.shuffle(files)

    filesLabel = files.copy()

    # change each filename in filesLabel to be .txt instead of .jpg
    for i in range(len(filesLabel)):
        filesLabel[i] = filesLabel[i].replace(".jpg", ".txt")

    trainSplit = int(len(files) * 0.7)

    valSplit = int(len(files) * 0.90)

    trainFiles = files[:trainSplit]

    valFiles = files[trainSplit:valSplit]

    testFiles = files[valSplit:]

    trainFilesLabel = filesLabel[:trainSplit]

    valFilesLabel = filesLabel[trainSplit:valSplit]

    testFilesLabel = filesLabel[valSplit:]


    # move files to train, val, test folders
    train_folder = dataStorageDirectory + "/train/{}/"
    val_folder = dataStorageDirectory + "/val/{}/"
    test_folder = dataStorageDirectory + "/test/{}/"

    for file in trainFiles:
        os.rename(sourceFolder.format("images") + file, train_folder.format("images") + file)

    print("did the thing")

    for file in valFiles:
        os.rename(sourceFolder.format("images") + file, val_folder.format("images") + file)

    for file in testFiles:
        os.rename(sourceFolder.format("images") + file, test_folder.format("images") + file)

    for file in trainFilesLabel:
        os.rename(sourceFolder.format("labels") + file, train_folder.format("labels") + file)

    for file in valFilesLabel:   
        os.rename(sourceFolder.format("labels") + file, val_folder.format("labels") + file)

    for file in testFilesLabel:
        os.rename(sourceFolder.format("labels") + file, test_folder.format("labels") + file)

    # copy over dataset.yaml file to data.yaml
    shutil.copy(middleDataStorageDirectory + "/dataset.yaml", dataStorageDirectory + "/data.yaml")

    # injest as yaml file
    with open(dataStorageDirectory + "/data.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        # delete path field
        del data['path']

        #change val filed to be val images folder
        data['val'] = dataStorageDirectory + "/val/images"
        
        # add train and test fields
        data['train'] = dataStorageDirectory + "/train/images"
        data['test'] = dataStorageDirectory + "/test/images"
        data['nc'] = len(data['names'])

        # convert names from list to dict
        data['names'] = {i: data['names'][i] for i in range(len(data['names']))}

    # write to data.yaml
    with open(dataStorageDirectory + "/data.yaml", 'w') as f:
        yaml.dump(data, f)

    print("file contents are now:" + str(data))

        

def dockerPrep(basePath):

    # Copy the all the files in settings['datasets_dir'] to this drive ../datasets
    src_folder = r'F:\\Data\\Final'
    dest_folder = r'C:\\Users\\muchn\Documents\\Classes\\18500\\Forget-Me-Not-Capstone\\Yolo-Classification\\datasets\\Final'
    # Check if the source folder exists
    if not os.path.exists(src_folder):
        print(f"Source folder {src_folder} does not exist.")
        return

    # Create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Copy all files and subdirectories from source to destination
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dest_path = os.path.join(dest_folder, item)

        # Check if it's a file or a directory
        if os.path.isdir(src_path):
            # Recursively copy directories
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        else:
            # Copy files
            shutil.copy2(src_path, dest_path)

    print(f"All files and directories from {src_folder} have been copied to {dest_folder}.")

    if basePath is True:
        settings['datasets_dir'] = "/app/datasets/"
    else:
       settings['datasets_dir'] = basePath

    

    global train_folder
    global val_folder
    global test_folder

    train_folder = settings['datasets_dir'][:5] + 'Final/train/{}/'
    val_folder = settings['datasets_dir'][:5] + 'Final/val/{}/'
    test_folder = settings['datasets_dir'][:5] + 'Final/test/{}/'

def convertLabelValues():
    
        # Go through the list of all label files in the "F:\Data\\Intermediary\\labels\\val\\" folder
    
        labelsList = os.listdir(sourceFolder.format("labels"))
    
        for labelFile in labelsList:
    
            # Open the file and read the lines
    
            with open(sourceFolder.format("labels") + labelFile, 'r') as f:
    
                lines = f.readlines()
    
                # For each line, get the first word and change it to the corresponding number in the data.yaml file
    
                for i in range(len(lines)):
                    lines[i] = lines[i].split()
                    lines[i][0] = conversionFromJSONToYAML[int(lines[i][0])]
                    lines[i] = " ".join(str(x) for x in lines[i])
    
            # Write the new lines to the file
    
            with open(sourceFolder.format("labels") + labelFile, 'w') as f:
    
                for line in lines:
                    f.write(line + "\n")


def modifyFile(myFile, modText):
    # Open the file
    file = open(myFile, "r")
    text = file.read()
    file.close()

    # Modify the "first few characters until the first space of each line"
    
    #for each line
    lines = text.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        #for each character in the line
        for j in range(len(line)):
            #if the character is a space
            if line[j] == " ":
                #modify the first character
                lines[i] = modText + line[j:]
                break
    # Join the lines back together
    text = "\n".join(lines)
    

    # Write the modified text back to the file
    file = open(myFile, "w")
    file.write(text)
    file.close()

def modifyFileUsingConversionDict(myFile, conversionDict):
    # Open the file
    file = open(myFile, "r")
    text = file.read()
    file.close()

    # Modify the "first few characters until the first space of each line"
    
    #for each line
    lines = text.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        #for each character in the line
        for j in range(len(line)):
            #if the character is a space
            if line[j] == " ":
                #modify the first character
                lines[i] = str(conversionDict[int(line[:j])]) + line[j:]
                break
    # Join the lines back together
    text = "\n".join(lines)
    

    # Write the modified text back to the file
    file = open(myFile, "w")
    file.write(text)
    file.close()

def modifyFiles(folder, modAmmount = None, conversionDict=None):
    # Get all the files in the folder
    files = os.listdir(folder)

    # Modify each file
    for file in files:
        if conversionDict is not None:
            modifyFileUsingConversionDict(os.path.join(folder, file), conversionDict)
        else:
            modifyFile(os.path.join(folder, file), modAmmount)

def augmentData(modDirectory, addDirectory):

    # remove mod directory and everything inside of it if it exists
    for dir in modDirectory:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    
    # exit()


    # Function to load YOLO format labels
    def load_yolo_labels(label_path, img_w, img_h):
        boxes = []
        gofwd = True
        with open(label_path, 'r') as f:
            for line in f.readlines():
                # print(line)

                # if there more then 5 words in the line, then it is not a label

                if len(line.split()) > 5:
                    gofwd = False
                    return boxes, gofwd

                class_id, x_center, y_center, width, height = map(float, line.strip().split())
                
                x_min = (x_center - width / 2) * img_w
                y_min = (y_center - height / 2) * img_h
                x_max = (x_center + width / 2) * img_w
                y_max = (y_center + height / 2) * img_h
                boxes.append([x_min, y_min, x_max, y_max, int(class_id)])
                
        return boxes, gofwd

    # Function to save YOLO format labels
    def save_yolo_labels(save_path, boxes, img_w, img_h):
        with open(save_path, 'w') as f:
            for box in boxes:
                class_id = int(box[4])
                x_center = (box[0] + box[2]) / 2 / img_w
                y_center = (box[1] + box[3]) / 2 / img_h
                width = (box[2] - box[0]) / img_w
                height = (box[3] - box[1]) / img_h
                if x_center - width / 2 < 0 or x_center + width / 2 > 1 or y_center - height / 2 < 0 or y_center + height / 2 > 1:
                    print(f"Invalid label: {save_path}")
                    print("bbox[0]: ", box[0], "bbox[1]: ", box[1], "bbox[2]: ", box[2], "bbox[3]: ", box[3])
                    print("img_w: ", img_w, "img_h: ", img_h)
                    exit()
                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

    # Augmentation pipeline
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.1),
        A.RandomRotate90(p=0.5),
        A.RandomResizedCrop(height=416, width=416, scale=(0.8, 1.0), p=0.5),
        A.OneOf([
            A.MotionBlur(p=0.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.GaussianBlur(blur_limit=3, p=0.1),
        ], p=0.5),
        A.ColorJitter(p=0.5),
        A.RandomBrightnessContrast(p=0.5),
        A.GaussNoise(p=0.2),
        A.RandomScale(scale_limit=0.2, p=0.5),
        A.Affine(scale=(0.9, 1.1), translate_percent=0.1, rotate=15, shear=10, p=0.5),
        A.Perspective(p=0.5),
        A.ToGray(p=0.1),
        A.ToFloat(max_value=255),
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['class_labels']))

    # get all the folders in the add dataset path
    print("add dataset path is : " + str(addDirectory))
    print("mod dataset path is : " + str(modDirectory))
    for i, folder in enumerate(addDirectory):


        # get all the files in the folder
        valPath = os.path.join(folder, 'valid')
        trainPath = os.path.join(folder, 'train')
        testPath = os.path.join(folder, 'test')

        valModPath = os.path.join(modDirectory[i], 'valid')
        trainModPath = os.path.join(modDirectory[i], 'train')
        testModPath = os.path.join(modDirectory[i], 'test')

        # Create the folders
        os.makedirs(valModPath, exist_ok=True)
        os.makedirs(trainModPath, exist_ok=True)
        os.makedirs(testModPath, exist_ok=True)

        # Create the val, train, and test folders
        valTrainTest = [valPath, trainPath, testPath]
        imageLabels =['images', 'labels']

        valModTrainTest = [valModPath, trainModPath, testModPath]



        # Directory paths
        images_dir = 'path_to_images'
        labels_dir = 'path_to_labels'
        aug_images_dir = 'augmented_images'
        aug_labels_dir = 'augmented_labels'

        # Copy over data.yaml file
        shutil.copy(os.path.join(folder, 'data.yaml'), os.path.join(modDirectory[i], 'data.yaml'))
        
        for i,path in enumerate(valTrainTest):
            images_dir = os.path.join(path, imageLabels[0])
            labels_dir = os.path.join(path, imageLabels[1])

            aug_images_dir = os.path.join(valModTrainTest[i], imageLabels[0])
            aug_labels_dir = os.path.join(valModTrainTest[i], imageLabels[1])


            # Create the folders
            os.makedirs(aug_images_dir, exist_ok=True)
            os.makedirs(aug_labels_dir, exist_ok=True)

            # Number of augmented versions per image
            n_augmentations_per_image = 5

            # Iterate through the images and labels
            for image_name in os.listdir(images_dir):
                if not image_name.endswith('.jpg'):  # Assuming .jpg images
                    continue
                

                # Load image and corresponding label
                image_path = os.path.join(images_dir, image_name)
                label_path = os.path.join(labels_dir, image_name.replace('.jpg', '.txt'))
                
                image = cv2.imread(image_path)

                img_h, img_w = image.shape[:2]
                boxes, gofwd = load_yolo_labels(label_path, img_w, img_h)
                cv2.imwrite(os.path.join(aug_images_dir, image_name), image)
                # write original label from label_path to by copied to augmented folder
                shutil.copy(label_path, os.path.join(aug_labels_dir, image_name.replace('.jpg', '.txt')))

                if gofwd is False:
                    # print("skipped image")
                    continue
                # print(boxes)

                # Prepare boxes and labels for Albumentations
                class_labels = [box[4] for box in boxes]
                bboxes = [box[:4] for box in boxes]  # Only take x_min, y_min, x_max, y_max

                # write original image/label to augmented folder


                for i in range(n_augmentations_per_image):
                    # Apply augmentations
                    augmented = transform(image=image, bboxes=bboxes, class_labels=class_labels)

                    shouldContinue = False

                    # ensure transformations are not out of bounds
                    for bbox in augmented['bboxes']:
                        # every value should be normalized and within boyunds and continue otherwise

                        if bbox[0] < 0 or bbox[1] < 0 or bbox[2] < 0 or bbox[3] < 0 or bbox[0] > img_w or bbox[1] > img_h or bbox[2] > img_w or bbox[3] > img_h:
                            if image_name == "Snipaste_2022-04-21_10-07-48_jpg.rf.18f22f1e3eab1f21a2dae5eb203f353d.jpg":
                                print("printing bounding box")

                                print("bbox[0]: ", bbox[0], "bbox[1]: ", bbox[1], "bbox[2]: ", bbox[2], "bbox[3]: ", bbox[3])
                                print(bbox)

                            shouldContinue = True
                            continue
                    
                    if shouldContinue:
                        continue

                    aug_image = augmented['image']

                    if aug_image.dtype != np.uint8:
                        aug_image = (aug_image * 255).astype(np.uint8)

                    aug_bboxes = augmented['bboxes']
                    aug_class_labels = augmented['class_labels']

                    # Convert and save augmented image and label
                    aug_image_name = f"{image_name.replace('.jpg', '')}_aug_{i}.jpg"
                    aug_label_name = f"{image_name.replace('.jpg', '')}_aug_{i}.txt"
                    
                    aug_image_path = os.path.join(aug_images_dir, aug_image_name)
                    aug_label_path = os.path.join(aug_labels_dir, aug_label_name)

                    cv2.imwrite(aug_image_path, aug_image)
                    aug_boxes = [list(bbox) + [cls] for bbox, cls in zip(aug_bboxes, aug_class_labels)]
                    save_yolo_labels(aug_label_path, aug_boxes, img_w, img_h)

                    print(f"Saved: {aug_image_name} and {aug_label_name}")

    print("Augmentation complete!")


def addDatasetToBiggerDataset(originalDatasetPath, addDatasetPath):
    print("add dataset path is : " + addDatasetPath)
    testPath = os.path.join(addDatasetPath, "test/{}")
    trainPath = os.path.join(addDatasetPath, "train/{}")
    valPath = os.path.join(addDatasetPath, "valid/{}")

    listPaths = [testPath, trainPath, valPath]
    
    dataYamlPath = os.path.join(addDatasetPath, "data.yaml")

    # add names in add dataset to original dataset
    with open(dataYamlPath, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(originalDatasetPath + "/data.yaml", 'r') as stream:
        try:
            originalData = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    ncOriginal = originalData['nc']
    print(type(originalData['names']))
    print(data)
    print("data is : " + str(data))
    if type(data['names']) == list:
        # get length of originalData['names']
        length = len(originalData['names'])
        # add length to each element in data['names'] after converting to dict
        data['names'] = {i: data['names'][i] for i in range(len(data['names']))}
    conversionDict = {}
    newLabels = 0
    # print(data['names'][i])
    for i in data['names']:
        print(data['names'][i])
        if data['names'][i] in originalData['names'].values():
            conversionDict[i] = (next(k for k, v in originalData['names'].items() if v == data['names'][i]))
        else:
            conversionDict[i] = newLabels + ncOriginal
            newLabels += 1
    print("the conversion dict is: ")
    print(conversionDict)

    # dump data to data.yaml
    with open(dataYamlPath, 'w') as f:
        # convert data['names'] via the conversionDict
        tempDataNames = {}
        for key, value in data['names'].items():
            tempDataNames[conversionDict[key]] = value


        data['names'] = tempDataNames


        yaml.dump(data, f)


    for path in listPaths:
        modifyFiles(path.format("labels"), conversionDict=conversionDict)

        #TODO should modify labels in data names. should utilize modify script

    # add key value pairs in data to originalData
    for key in data['names']:
        originalData['names'][key] = data['names'][key]

    #update nc in originalData  
    originalData['nc'] = len(originalData['names'])


    with open(originalDatasetPath + "/data.yaml", 'w') as f:
        yaml.dump(originalData, f)


    train_folder = originalDatasetPath + "/train/{}/"
    val_folder = originalDatasetPath + "/val/{}/"
    test_folder = originalDatasetPath + "/test/{}/"

    imagesLabels = ["images", "labels"]
    paths = [testPath, trainPath, valPath]
    pathsTo = [test_folder, train_folder, val_folder]
    for i in range(len(paths)):
        for imageLabel in imagesLabels:
            imageLabelPath = paths[i].format(imageLabel)
            print(imageLabelPath)
            for file in os.listdir(imageLabelPath):
                shutil.copy(os.path.join(imageLabelPath, file), os.path.join(pathsTo[i].format(imageLabel), file))

def train(dataStorageDirectory, model = "yolo11n.yaml", epochs = 400, resume = False, batch_size = 32):

    settings['datasets_dir'] = dataStorageDirectory

    # Load the YOLOv11 model
    model = YOLO(model=model, task="detect")

    # Perform object detection
    model.train(data=os.path.join(dataStorageDirectory, "data.yaml"), imgsz=640, epochs=epochs, resume=resume, batch=batch_size)

def validate(dataStorageDirectory, model = "yolo11n.yaml"):

    settings['datasets_dir'] = dataStorageDirectory

    # Load the YOLOv11 model
    model = YOLO(model=model, task="detect")

    # Perform object detection
    metrics = model.val(data=os.path.join(dataStorageDirectory, "data.yaml"), imgsz=640, batch=8) 

    print(metrics.box.maps)

# based on arg of -d, -c, -t you either run download data, copyfiles and train, copyfiles and train or train

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--initialDataStorageDirectory', type =str, default="/app/initial-download")
    parser.add_argument('-ms', '--middleDataStorageDirectory', type =str, default="/app/Intermediary") 
    parser.add_argument('-ds', '--dataStorageDirectory', type =str, default="/app/datasets/Final")
    parser.add_argument('-modd', '--modDirectory', type=str, default="/app/datasets/Augmentation")
    parser.add_argument('-ad', '--addDatasetPath', type=str, default="/app/datasets/Images/")
    parser.add_argument('-dd', '--dockerDataPath',nargs='?', const=False, default=False)
    parser.add_argument('-yp', '--yamlPath',nargs='?', const=False, default=False)
    parser.add_argument('-mxs', '--maxSamples', type =int, nargs='?', const=None, default=None)
    parser.add_argument('-m', '--model', type =str, nargs='?', default=False)
    parser.add_argument('-d', '--downloadData', action='store_true')
    parser.add_argument('-f', '--filterCoco', action='store_true')
    parser.add_argument('-dp', '--dockerPrep', nargs='?', const=True, default=False)
    parser.add_argument('-a', '--add', type=str, nargs='*',  default=None)
    parser.add_argument('-b', '--batch_size', type =int, nargs='?', const=32, default=32)
    # parser.add_argument('-a', '--add', type=str, nargs='+', const="/app/datasets/Images/", default=None) 
    parser.add_argument('-c', '--copyFiles', action='store_true')
    parser.add_argument('-md', '--modData', action='store_true')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-r', '--resume', action='store_true')
    parser.add_argument('-lt', '--locallyTrained', action='store_true')
    parser.add_argument('-s', '--split',  type =str, nargs='?', const="validation",default="validation")
    parser.add_argument('-e', '--epochs',  type =int, nargs='?', const=400, default=400)
    parser.add_argument('-v', '--validate', action='store_true')
    args = parser.parse_args()
    modDirectory = []
    if args.add == []:
        # remove all directories within args.addDatasetPath
        # if the path exists 
        if os.path.exists(args.modDirectory):
            # list directories in args.modDirectory
            directories = [d for d in os.listdir(args.modDirectory)]
            # remove all directories in args.modDirectory
            for directory in directories:
                shutil.rmtree(os.path.join(args.modDirectory, directory))



        folder_path = args.addDatasetPath
        directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

        for directory in directories:
            args.add.append(os.path.join(folder_path, directory))
            modDirectory.append(os.path.join(args.modDirectory, directory))
        
        print("args add after modifying: " + str(args.add))
    if args.validate:
        if args.model == False:
            model = "yolo11x.pt"
        elif args.model == True and args.locallyTrained:
            model = args.model
        else:
            model = "/app/runs/detect/{}/weights/last.pt".format(args.model)
        validate(args.dataStorageDirectory, model = model)
    if args.downloadData:
        downLoadData(args.initialDataStorageDirectory, args.middleDataStorageDirectory, args.split, args.maxSamples)
    if args.filterCoco:
        # convertLabelValues()
        filterCoco(args.middleDataStorageDirectory)
    if args.copyFiles:
        CopyFiles(args.dataStorageDirectory, args.middleDataStorageDirectory)
    if args.dockerPrep:
        dockerPrep(args.dockerPrep)
    if args.modData:
        augmentData( modDirectory, args.add)
    if args.add:
        if args.modData:
            for i in modDirectory:
                addDatasetToBiggerDataset(args.dataStorageDirectory, i)
        else:
            for i in args.add:
                addDatasetToBiggerDataset(args.dataStorageDirectory, i)
    if args.train:
        if args.resume and args.model:
            model = "/app/runs/detect/{}/weights/last.pt".format(args.model)
        elif args.resume and not args.model:
            model ="/app/runs/detect/train/weights/last.pt"
        elif not args.resume and args.model:
           model =  args.model
        elif not args.resume and not args.model:
          model =  "yolo11n.yaml"
        
        train(args.dataStorageDirectory, model, args.epochs, args.resume, args.batch_size)