import fiftyone as fo
import fiftyone.zoo as foz
import os
import random
import argparse
import json
import yaml
import shutil

import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics import settings



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

def downLoadData(initialDataStorageDirectory, middleDataStorageDirectory):
    
    name = "coco-2017"
    settings['datasets_dir'] = initialDataStorageDirectory
    dataset = foz.load_zoo_dataset(name, label_types="detections", split="validation")

    dataset.export(
        export_dir= middleDataStorageDirectory,
        dataset_type=fo.types.YOLOv5Dataset,  # Specify the export format
        label_field="ground_truth",           # Specify the field containing labels (if applicable)
    )

def filterCoco(middleDataStorageDirectory):

    # import CategoriesNum.txt file
    with open('categoriesNum.txt', 'r') as f:
        categories = f.readlines()
        categories = [int(x.strip()) for x in categories]   


    sourceFolder = middleDataStorageDirectory + "/{}/val/"
    # Make a list of all nums from 0 to 80 not present in CategoriesNum.txt
    notInList = [x for x in range(0, 81) if x not in categories]   

    # Go through the list of all label files in the "F:\Data\\Intermediary\\labels\\val\\"

    labelsList = os.listdir(sourceFolder.format("labels"))

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
                if lines[i] in notInList:
                    shouldDelete = True
                    break

        if shouldDelete:
            os.remove(sourceFolder.format("labels") + labelFile)
            os.remove(sourceFolder.format("images") + labelFile.replace(".txt", ".jpg"))

def CopyFiles(dataStorageDirectory, middleDataStorageDirectory):
    # Take 70% of files in the "F:\Data\\not-initial\\images\\val" folder and move them to the "F:\Data\\Final\\train\images" folder
    trainValTestFolders = ["train", "val", "test"]
    imagesLabels = ["images", "labels"]
    for folder in trainValTestFolders:
        for imageLabel in imagesLabels:
            os.makedirs(os.path.join(dataStorageDirectory, folder, imageLabel), exist_ok=True)

    # os.makedirs(train_folder.format("images"), exist_ok=True)
    # os.makedirs(val_folder.format("images"), exist_ok=True)
    # os.makedirs(test_folder.format("images"), exist_ok=True)

    # os.makedirs(train_folder.format("labels"), exist_ok=True)
    # os.makedirs(val_folder.format("labels"), exist_ok=True)
    # os.makedirs(test_folder.format("labels"), exist_ok=True)

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

    # change each filename in files to be .jpg instead of .txt
    "F:\Data\Intermediary\labels\val\000000000139.txt"

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

def modifyFiles(folder, modAmmount):
    # Get all the files in the folder
    import os
    files = os.listdir(folder)

    # Modify each file
    for file in files:
        modifyFile(os.path.join(folder, file), modAmmount)

def addDatasetToBiggerDataset(originalDatasetPath, addDatasetPath):
    testPath = os.path.join(addDatasetPath, "test/{}")
    trainPath = os.path.join(addDatasetPath, "train/{}")
    valPath = os.path.join(addDatasetPath, "val/{}")

    listPaths = [testPath, trainPath, valPath]
    
    print(addDatasetPath)
    dataYamlPath = os.path.join(addDatasetPath, "data.yaml")
    print(dataYamlPath)
    print("helldoasfasdf asdfasdf")

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

    if type(data['names']) == list:
        # get length of originalData['names']
        length = len(originalData['names'])
        # add length to each element in data['names'] after converting to dict
        data['names'] = {length + i: data['names'][i] for i in range(len(data['names']))}
        
    for key in data['names']:
        for path in listPaths:
            modifyFiles(path.format("labels"), str(ncOriginal))
        

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


    

def train(dataStorageDirectory):

    settings['datasets_dir'] = dataStorageDirectory

    # Load the YOLOv8 model
    model = YOLO('YoloModels/yolo11l.pt')

    # Perform object detection
    model.train(data=os.path.join(dataStorageDirectory, "data.yaml"), imgsz=640, epochs=10)
        

# based on arg of -d, -c, -t you either run download data, copyfiles and train, copyfiles and train or train

if __name__ == "__main__":
    
    # settings['datasets_dir'] = "F:\Data\\datasets\\"
    # print(settings)
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--initialDataStorageDirectory', type =str, default="/app/initial-download")
    parser.add_argument('-ms', '--middleDataStorageDirectory', type =str, default="/app/Intermediary") 
    parser.add_argument('-ds', '--dataStorageDirectory', type =str, default="/app/datasets/Final")
    parser.add_argument('-dd', '--dockerDataPath',nargs='?', const=False, default=False)
    parser.add_argument('-yp', '--yamlPath',nargs='?', const=False, default=False)

    parser.add_argument('-d', '--downloadData', action='store_true')
    parser.add_argument('-f', '--filterCoco', action='store_true')
    parser.add_argument('-dp', '--dockerPrep', nargs='?', const=True, default=False)
    parser.add_argument('-a', '--add', type=str, nargs='?', const="/app/datasets/Images/Detecting-Pencils-1/", default=None) 
    parser.add_argument('-c', '--copyFiles', action='store_true')
    parser.add_argument('-t', '--train', action='store_true')
    args = parser.parse_args()
    # if args.dataStorageDirectory:
    #     settings['datasets_dir'] = args.data_storage_directory

    # train_folder = settings['datasets_dir'][:9] + 'Final\\train\\{}\\'
    # val_folder = settings['datasets_dir'][:9] + 'Final\\val\\{}\\'
    # test_folder = settings['datasets_dir'][:9] + 'Final\\test\\{}\\'


    if args.downloadData:
        downLoadData(args.initialDataStorageDirectory, args.middleDataStorageDirectory)
    if args.filterCoco:
        # convertLabelValues()
        filterCoco(args.middleDataStorageDirectory)
    if args.copyFiles:
        CopyFiles(args.dataStorageDirectory, args.middleDataStorageDirectory)
    if args.dockerPrep:
        dockerPrep(args.dockerPrep)
    if args.add:
        print("yoo wassup this is your boi sk")
        print(args.add)
        addDatasetToBiggerDataset(args.dataStorageDirectory, args.add)
    if args.train:
        train(args.dataStorageDirectory)







