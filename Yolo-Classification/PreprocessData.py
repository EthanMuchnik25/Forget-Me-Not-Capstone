import os
import shutil
import yaml
import fiftyone as fo
import fiftyone.zoo as foz
import random
import argparse

import os
import random
import yaml
import shutil
import cv2
import numpy as np

import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics import settings
import albumentations as A
import torch

def downLoadData(initialDataStorageDirectory, middleDataStorageDirectory, split, max_samples, args):
    if os.path.exists(middleDataStorageDirectory):
        shutil.rmtree(middleDataStorageDirectory)
    os.makedirs(middleDataStorageDirectory)

    if not args.useCOCO:
        max_samples = 0
        print("HELLO CHANGES MAX SAMPLES TO 0: " + str(max_samples))

    if split == "both":
        split = ["train", "validation"]
    else:
        split = [split]

    print(split)
    tmpLocs = []
    for spl in split:
        name = "coco-2017"
        settings['datasets_dir'] = initialDataStorageDirectory
        if max_samples is None:
            dataset = foz.load_zoo_dataset(name, label_types="detections", split=spl)
        else:
            print("max_samples: " + str(max_samples))
            dataset = foz.load_zoo_dataset(name, label_types="detections", split=spl, max_samples=max_samples)
        # delete and create
        tmp = middleDataStorageDirectory + "/{}/".format(spl)
        tmpLocs.append(tmp)
        dataset.export(
            export_dir= tmp,
            dataset_type=fo.types.YOLOv5Dataset,  # Specify the export format
            label_field="ground_truth",           # Specify the field containing labels (if applicable)
        )

        # if dataset.yaml exists, move it to data.yaml
        if os.path.exists(middleDataStorageDirectory + "/{}/dataset.yaml".format(spl)):
            os.rename(middleDataStorageDirectory + "/{}/dataset.yaml".format(spl), middleDataStorageDirectory + "/{}/data.yaml".format(spl))
        
        # load up data.yaml
        with open(middleDataStorageDirectory + "/{}/data.yaml".format(spl), 'r') as stream:
            
            # add nc
            data = yaml.safe_load(stream)
            data['nc'] = len(data['names'])
            with open(middleDataStorageDirectory + "/{}/data.yaml".format(spl), 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)

    # exit()
    for spl in tmpLocs[1:]:
        print("spl is : " + str(spl))
        print("tmpLocs[0] is : " + str(tmpLocs[0]))
        addDataset(tmpLocs[0], spl, args, False)

    
    
    for spl in [split[0]]:
        os.makedirs(middleDataStorageDirectory + "/images/val")
        os.makedirs(middleDataStorageDirectory + "/labels/val")

        # transfer each file in middleDataStorageDirectory/{}/images to middleDataStorageDirectory/images/val
        for file in os.listdir(middleDataStorageDirectory + "/{}/images/val/".format(spl)):
            if os.path.exists(middleDataStorageDirectory + "/{}/labels/val/".format(spl) + file.replace(".jpg", ".txt")) and os.path.exists(middleDataStorageDirectory + "/{}/images/val/".format(spl) + file):
                shutil.move(middleDataStorageDirectory + "/{}/images/val/".format(spl) + file, middleDataStorageDirectory + "/images/val")
                shutil.move(middleDataStorageDirectory + "/{}/labels/val/".format(spl) + file.replace(".jpg", ".txt"), middleDataStorageDirectory + "/labels/val")
        
    # remove the empty folders
    # for spl in split:
    #     shutil.rmtree(middleDataStorageDirectory + "/{}/".format(spl))
        
    # copy over dataset.yaml from split[0] to middleDataStorageDirectory
    shutil.copyfile(middleDataStorageDirectory + "/{}/data.yaml".format(split[0]), middleDataStorageDirectory + "/data.yaml")


def filterCoco(middleDataStorageDirectory, args):
    print("in filterCoco")
    # import CategoriesNum.txt file
    # with open('categoriesNum.txt', 'r') as f:
    #     categories = f.readlines()
    #     categories = [int(x.strip()) for x in categories]   
    if args.reducedImages:
        categories = 'categoriesSmaller.txt'
    else:
        categories = 'categories.txt'
    
    with open(categories, 'r') as f:
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
    with open(middleDataStorageDirectory + "/data.yaml", 'r') as stream:
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
    with open(middleDataStorageDirectory + "/data.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        data['names'] = categories

        print("len(data['names']) : " + str(len(data['names'])))
    # Write the new data to the dataset.yaml file
    with open(middleDataStorageDirectory + "/data.yaml", 'w') as f:
        print("dumping")
        yaml.dump(data, f)


def allocateTrainValTestRandomly(sourceFolder):

    # shuffle files

    files = os.listdir(sourceFolder.format("images"))

    # Set a random seed
    random.seed(42)

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

    return trainFiles, valFiles, testFiles, trainFilesLabel, valFilesLabel, testFilesLabel

def allocateTrainValTestRandomly(sourceFolder):

    # shuffle files

    files = os.listdir(sourceFolder.format("images"))

    # Set a random seed
    random.seed(42)

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

    return trainFiles, valFiles, testFiles, trainFilesLabel, valFilesLabel, testFilesLabel

def allocateFromDataRepo(dataRepo):

    # Create list of train files from file names in trainFileLocations.txt in dataRepo

    with open(os.path.join(dataRepo, "trainFileLocations.txt"), 'r') as f:
        trainFiles = f.readlines()

    trainFiles = [x.strip() for x in trainFiles]

    trainFilesLabel = [x.replace(".jpg", ".txt") for x in trainFiles]

    with open(os.path.join(dataRepo, "valFileLocations.txt"), 'r') as f:
        valFiles = f.readlines()

    valFiles = [x.strip() for x in valFiles]

    valFilesLabel = [x.replace(".jpg", ".txt") for x in valFiles]

    with open(os.path.join(dataRepo, "testFileLocations.txt"), 'r') as f:
        testFiles = f.readlines()

    testFiles = [x.strip() for x in testFiles]

    testFilesLabel = [x.replace(".jpg", ".txt") for x in testFiles]

    return trainFiles, valFiles, testFiles, trainFilesLabel, valFilesLabel, testFilesLabel


def CopyFiles(dataStorageDirectory, middleDataStorageDirectory, args):
    # delete and create dataStorageDirectory
    print("Am inside of copy")
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
    if args.certainAlloc == False:
        trainFiles, valFiles, testFiles, trainFilesLabel, valFilesLabel, testFilesLabel = allocateTrainValTestRandomly(sourceFolder)
    elif args.certainAlloc == True:
        caVal = os.path.join(args.model, args.name)
        # caVal = args.model
        print("caVal is : " + caVal)
        trainFiles, valFiles, testFiles, trainFilesLabel, valFilesLabel, testFilesLabel = allocateFromDataRepo(caVal)
    

        

    # move files to train, val, test folders
    train_folder = dataStorageDirectory + "/train/{}/"
    val_folder = dataStorageDirectory + "/val/{}/"
    test_folder = dataStorageDirectory + "/test/{}/"

    # print("file0 is : " + trainFiles[0])

    for file in trainFiles:
        file = os.path.basename(file)
        # check the file is present in source folder

        if os.path.exists(os.path.join(sourceFolder.format("images"), file)):
            os.rename(sourceFolder.format("images") + file, train_folder.format("images") + file)
            print("file found: " + sourceFolder.format("images") + file)
        else:
            print("File not found: " + sourceFolder.format("images") + file)

    print("did the thing")

    for file in valFiles:
        file = os.path.basename(file)
        if os.path.exists(sourceFolder.format("images") + file):
            os.rename(sourceFolder.format("images") + file, val_folder.format("images") + file)
        else:
            print("File not found: " + sourceFolder.format("images") + file)

    for file in testFiles:
        file = os.path.basename(file)
        if os.path.exists(sourceFolder.format("images") + file):
            os.rename(sourceFolder.format("images") + file, test_folder.format("images") + file)
        else:
            print("File not found: " + sourceFolder.format("images") + file)

    for file in trainFilesLabel:
        file = os.path.basename(file)
        if os.path.exists(sourceFolder.format("labels") + file):
            os.rename(sourceFolder.format("labels") + file, train_folder.format("labels") + file)
        else:
            print("File not found: " + sourceFolder.format("labels") + file)

    for file in valFilesLabel:   
        file = os.path.basename(file)
        if os.path.exists(sourceFolder.format("labels") + file):
            os.rename(sourceFolder.format("labels") + file, val_folder.format("labels") + file)
        else:
            print("File not found: " + sourceFolder.format("labels") + file)

    for file in testFilesLabel:
        file = os.path.basename(file)
        if os.path.exists(sourceFolder.format("labels") + file):
            os.rename(sourceFolder.format("labels") + file, test_folder.format("labels") + file)
        else:
            print("File not found: " + sourceFolder.format("labels") + file)

    # copy over dataset.yaml file to data.yaml
    shutil.copy(middleDataStorageDirectory + "/data.yaml", dataStorageDirectory + "/data.yaml")

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

def augmentData(modDirectory, addDirectory, args):

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
        # A.PadIfNeeded(min_height=600, min_width=600, border_mode=cv2.BORDER_REFLECT),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.1),
        A.RandomRotate90(p=0.5),
        A.RandomResizedCrop(height=416, width=416, scale=(0.8, 1.0), p=0.5),
        A.OneOf([
            A.MotionBlur(p=0.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.GaussianBlur(blur_limit=3, p=0.1),
        ], p=0.5),
        A.ColorJitter(p=0.3, hue=(-0.1, 0.1), contrast=(0.9, 1.1), saturation=(0.9, 1.1)),
        A.RandomBrightnessContrast(p=0.3, brightness_limit=0.1, contrast_limit=0.1),
        A.GaussNoise(p=0.2),
        A.RandomScale(scale_limit=0.2, p=0.5),
        # A.Affine(scale=(0.9, 1.1), translate_percent=0.1, rotate=15, shear=10, p=0.5, cval=0, mode=cv2.BORDER_REFLECT),
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
            n_augmentations_per_image = args.augAmmount

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
                # cv2.imwrite(os.path.join(aug_images_dir, image_name), image)
                # # write original label from label_path to by copied to augmented folder
                # shutil.copy(label_path, os.path.join(aug_labels_dir, image_name.replace('.jpg', '.txt')))

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
                    augImgWidth = augmented['image'].shape[1]
                    augImgHeight = augmented['image'].shape[0]

                    shouldContinue = False

                    # ensure transformations are not out of bounds
                    for bbox in augmented['bboxes'][:]:
                        # every value should be normalized and within boyunds and continue otherwise
                        # if the entire bounding box is out of bounds
                        if bbox[0] < 0 and bbox[1] < 0 or bbox[2] < 0 and bbox[3] < 0 or bbox[0] > augImgWidth and bbox[1] > augImgHeight or bbox[2] > augImgWidth and bbox[3] > augImgHeight:
                            augmented['bboxes'].remove(bbox)
                            continue

                        elif bbox[0] < 0 or bbox[1] < 0 or bbox[2] < 0 or bbox[3] < 0 or bbox[0] > augImgWidth or bbox[1] > augImgHeight or bbox[2] > augImgWidth or bbox[3] > augImgHeight:
                            # clip out of bounds values
                            originalHeight = bbox[3] - bbox[1]
                            originalWidth = bbox[2] - bbox[0]
                            bbox[0] = max(0, min(bbox[0], augImgWidth))
                            bbox[1] = max(0, min(bbox[1], augImgHeight))
                            bbox[2] = max(0, min(bbox[2], augImgWidth))
                            bbox[3] = max(0, min(bbox[3], augImgHeight))

                            # calculate new height and width
                            newHeight = bbox[3] - bbox[1]
                            newWidth = bbox[2] - bbox[0]

                            # if new area is less than 70% of original area, continue
                            if newHeight * newWidth < 0.7 * originalHeight * originalWidth:
                                augmented['bboxes'].remove(bbox)
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
                    save_yolo_labels(aug_label_path, aug_boxes, augImgWidth, augImgHeight)

                    print(f"Saved: {aug_image_name} and {aug_label_name}")

    print("Augmentation complete!")

def addDataset(originalDatasetPath,specificAddDatasetPath, args, modified = True):
    # Create list of paths for test, train, and valid
    listPaths = []
    
    # for list of dirs in addDatasetPath
    for d in os.listdir(specificAddDatasetPath):
        # check if it is a dir
        if os.path.isdir(os.path.join(specificAddDatasetPath, d)):
            listPaths.append(os.path.join(specificAddDatasetPath, d) + "/")
    print("List of paths is : ")
    print(listPaths)    

    dataYamlPath = os.path.join(specificAddDatasetPath, "data.yaml")

    print("checkpoint")
    print("data yaml path is : " + dataYamlPath)
    print("listpaths is : " + str(listPaths))

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
    # print(data)
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
        # print(data['names'][i])
        # print(originalData['names'])
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
        print("hello in modify files for loop")
        for i in os.listdir(path):
            folder = os.path.join(path, i) + "/"
            print("the folder in modify files is : " + folder)
            print("truthe value of os.path.isdir(i) is : " + str(os.path.isdir(folder)))
            print("truth value of 'labels' in folder is : " + str("labels" in folder))
            if os.path.isdir(folder) and "labels" in folder:
                print("modifying files in:" + folder)
                modifyFiles(folder, conversionDict = conversionDict)

        #TODO should modify labels in data names. should utilize modify script

    # add key value pairs in data to originalData
    for key in data['names']:
        originalData['names'][key] = data['names'][key]

    #update nc in originalData  
    originalData['nc'] = len(originalData['names'])


    with open(originalDatasetPath + "/data.yaml", 'w') as f:
        yaml.dump(originalData, f)

    pathsTo = []
    for i in os.listdir(originalDatasetPath):
        if os.path.isdir(os.path.join(originalDatasetPath, i)):
            pathsTo.append(originalDatasetPath + "/" + i )
    print("Paths to is : " + str(pathsTo))
    # train_folder = originalDatasetPath + "/train/{}/"
    # val_folder = originalDatasetPath + "/val/{}/"
    # test_folder = originalDatasetPath + "/test/{}/"

    imagesLabels = [folder for folder in os.listdir(pathsTo[0]) if os.path.isdir(os.path.join(pathsTo[0], folder))]
    paths = listPaths
    # pathsTo = [test_folder, train_folder, val_folder]
    print("the paths are: ")
    print(paths)
    print("the paths to are: ")
    print(pathsTo)

    # sort the two lists
    imagesLabels.sort()
    paths.sort()
    pathsTo.sort()

    print("pathsto are:  + " + str(pathsTo))
    print("paths are:  + " + str(paths))

    print("the images labels are:  + " + str(imagesLabels))

    print("imageLabels are:  + " + str(imagesLabels))

    for i in range(len(paths)):
        for imageLabel in imagesLabels:
            imageLabelPath = os.path.join(paths[i], imageLabel)
            print(imageLabelPath)
            for file in os.listdir(imageLabelPath):
                # if "val" in pathsTo[i]:
                #     print("val in pathsTo[i]")
                # and args.dataStorageDirectory not in pathsTo[i]
                thePath = pathsTo[i] if not modified or ("val" not in pathsTo[i] and args.dataStorageDirectory not in pathsTo[i] )  else pathsTo[i].replace("val", "test")
                shutil.copy(os.path.join(imageLabelPath, file), os.path.join(thePath, imageLabel, file))


def addPotentiallyAugmented(originalDatasetPath, addDatasetPath, args):
    print("add dataset path is : " + addDatasetPath)
    modDirectory = []
    addDirectory = []
    directories = []
    if os.path.exists(args.modDirectory):
        directories = [d for d in os.listdir(args.modDirectory)]
        # remove all directories in args.modDirectory
        for directory in directories:
            shutil.rmtree(os.path.join(args.modDirectory, directory))



    folder_path = args.addDatasetPath
    print("folder path is : " + folder_path)
    directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    print("directories are : " + str(directories))

    for directory in directories:
        addDirectory.append(os.path.join(folder_path, directory))
        modDirectory.append(os.path.join(args.modDirectory, directory))
    
    print("args add after modifying: " + str(args.add))

    if args.modData:
        augmentData( modDirectory, addDirectory, args)
        for i in modDirectory:
            print("addDirectory is : " + str(addDirectory))
            addDataset(originalDatasetPath, i, args, True)
        for i in addDirectory:
            print("addDirectory is : " + str(addDirectory))
            addDataset(originalDatasetPath, i, args, False)
    else:
        for i in addDirectory:
            print("addDirectory is : " + str(addDirectory))
            addDataset(originalDatasetPath, i, args, False )


def getSaveDirName(args):
    settings['datasets_dir'] = args.dataStorageDirectory

    allFoldersToBeAdded = [ folder for folder in os.listdir(args.addDatasetPath) if os.path.isdir(os.path.join(args.addDatasetPath, folder)) and args.add ]
    print("all folders to be added are : " + str(allFoldersToBeAdded))
    folderString = "_".join(allFoldersToBeAdded) + "_" if allFoldersToBeAdded else ""

    certainAlloc = "True" if args.certainAlloc else "False"
    if args.dataWhileRunningDirectory == None:
        saveDirName = "" + args.model + "_epochs_" + str(args.epochs) + "_batch_" + str(args.batch_size) + "_resume_" + str(args.resume) + "_use_coco_" + str(args.useCOCO) + "_reduced_images_" + str(args.reducedImages) + "_split_" + str(args.split) + "_certain_alloc_" + str(certainAlloc) + "_add_folders_" + folderString + "_aug_ammount_" + str(args.augAmmount) + "_mxs_" + str(args.maxSamples)
    else:
        saveDirName = args.dataWhileRunningDirectory

    saveDirName = os.path.join("modelRuns", saveDirName)
    return saveDirName

def saveRelevantData(args, saveDirName):

    train_folder = os.path.join(args.dataStorageDirectory, "train/{}/")
    val_folder = os.path.join(args.dataStorageDirectory, "val/{}/")
    test_folder = os.path.join(args.dataStorageDirectory, "test/{}")

    if not os.path.exists(saveDirName):
        os.makedirs(saveDirName)

    # Create a file called trainFileLocations in the -dr directory
    if os.path.exists(train_folder.format("images")):
        with open(os.path.join(saveDirName, "trainFileLocations.txt"), "w") as f:
            for file in os.listdir(train_folder.format("images")):
                f.write(os.path.join(train_folder.format("images"), file) + "\n")
    
    # Create a file called valFileLocations in the -dr directory
    if os.path.exists(val_folder.format("images")):
        with open(os.path.join(saveDirName, "valFileLocations.txt"), "w") as f:
            for file in os.listdir(val_folder.format("images")):
                f.write(os.path.join(val_folder.format("images"), file) + "\n")

    # Create a file called testFileLocations in the -dr directory
    if os.path.exists(test_folder.format("images")):
        with open(os.path.join(saveDirName, "testFileLocations.txt"), "w") as f:
            for file in os.listdir(test_folder.format("images")):
                f.write(os.path.join(test_folder.format("images"), file) + "\n")
    
    return saveDirName

def loadArgparse(args):
    folder = args.model
    file = os.path.join(folder, args.name, "pythonScriptArgs.txt")

    with open(file, 'r') as f:
        args = yaml.safe_load(f)

    return argparse.Namespace(**args)