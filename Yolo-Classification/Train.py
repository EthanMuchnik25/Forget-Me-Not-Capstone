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
import torch
print(torch.cuda.is_available())  # Should return True

from PreprocessData import downLoadData, filterCoco, CopyFiles, addDataset, addPotentiallyAugmented, saveRelevantData, getSaveDirName


def train(model = "yolo11n.yaml", saveDirName =None, args = None):
    # Load the YOLOv11 model
    print('model is : ' + model)
    model = YOLO(model=model, task="detect")

    # Perform object detection
    metrics = model.train(data=os.path.join(args.dataStorageDirectory, "data.yaml"), imgsz=640, epochs=args.epochs, resume=args.resume, batch=args.batch_size, project=saveDirName, name=args.saveFolderName)
    # print("model.trainer.validator.args is : " + str(model.trainer.validator.args))
    # model_val = YOLO(model=model.model.pt_path, task="detect")
    # model_val.val(data=os.path.join(args.dataStorageDirectory, "data.yaml"), batch=32, imgsz=640, rect=True, half=True, warmup_bias_lr=0.0)

    # write metrics to a file called metrics.txt
    with open(os.path.join(saveDirName, str(metrics.save_dir.name), "metrics.txt"), "w") as f:
        f.write(str(metrics.results_dict))
        f.write("\n")
        for key in metrics.names:
            f.write(str(metrics.names[key]) + " : " + str(metrics.maps[key]) + "\n")
    

    if not os.path.exists(saveDirName):
        os.makedirs(saveDirName)

    # move everything in os.path.join(saveDirName, "trainFileLocations.txt") to os.path.join(saveDirName, str(metrics.save_dir.name), "trainFileLocations.txt")
    if os.path.exists(os.path.join(saveDirName, "trainFileLocations.txt")):
        shutil.move(os.path.join(saveDirName, "trainFileLocations.txt"), os.path.join(saveDirName, str(metrics.save_dir.name), "trainFileLocations.txt"))
    if os.path.exists(os.path.join(saveDirName, "valFileLocations.txt")):
        shutil.move(os.path.join(saveDirName, "valFileLocations.txt"), os.path.join(saveDirName, str(metrics.save_dir.name), "valFileLocations.txt"))
    if os.path.exists(os.path.join(saveDirName, "testFileLocations.txt")):
        shutil.move(os.path.join(saveDirName, "testFileLocations.txt"), os.path.join(saveDirName, str(metrics.save_dir.name), "testFileLocations.txt"))
    
    with open(os.path.join(saveDirName, str(metrics.save_dir.name), "AlreadyCompleted"), "w") as f:
        f.write("")

    

    # if os.path.exists(train_folder.format("images")):
    #     with open(os.path.join(saveDirName, str(metrics.save_dir.name), "trainFileLocations.txt"), "w") as f:
    #         for file in os.listdir(train_folder.format("images")):
    #             f.write(os.path.join(train_folder.format("images"), file) + "\n")
    
    # # Create a file called valFileLocations in the -dr directory
    # if os.path.exists(val_folder.format("images")):
    #     with open(os.path.join(saveDirName, str(metrics.save_dir.name), "valFileLocations.txt"), "w") as f:
    #         for file in os.listdir(val_folder.format("images")):
    #             f.write(os.path.join(val_folder.format("images"), file) + "\n")

    # # Create a file called testFileLocations in the -dr directory
    # if os.path.exists(test_folder.format("images")):
    #     with open(os.path.join(saveDirName, str(metrics.save_dir.name), "testFileLocations.txt"), "w") as f:
    #         for file in os.listdir(test_folder.format("images")):
    #             f.write(os.path.join(test_folder.format("images"), file) + "\n")

    with open(os.path.join(saveDirName, str(metrics.save_dir.name), "pythonScriptArgs.txt"), "w") as f:
        yaml.dump(vars(args), f)

def validate(dataStorageDirectory, model = "yolo11n.yaml"):
    
    print("data storage directory is : " + dataStorageDirectory)

    settings['datasets_dir'] = dataStorageDirectory

    if args.dataWhileRunningDirectory == None:
        saveDirName = args.model
    else:
        saveDirName = args.dataWhileRunningDirectory

        # Load the YOLOv11 model
    model = YOLO(model=model, task="detect")
    print("model.trainer.validator.args is : " + str(model.trainer.validator.args))
    # Perform object detection
    metrics = model.val(data=os.path.join(args.dataStorageDirectory, "data.yaml"), imgsz=640, batch=32, project=saveDirName, name="OfficialValFolder")
    
    print(metrics.box.maps)



# based on arg of -d, -c, -t you either run download data, copyfiles and train, copyfiles and train or train


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--initialDataStorageDirectory', type =str, default="/app/initial-download")
    parser.add_argument('-ms', '--middleDataStorageDirectory', type =str, default="/app/Intermediary") 
    parser.add_argument('-ds', '--dataStorageDirectory', type =str, default="/app/datasets/Final")
    parser.add_argument('-dr', '--dataWhileRunningDirectory', type=str, default=None)
    parser.add_argument('-modd', '--modDirectory', type=str, default="/app/datasets/Augmentation")
    parser.add_argument('-ad', '--addDatasetPath', type=str, default="/app/datasets/Images/")
    parser.add_argument('-dd', '--dockerDataPath',nargs='?', const=False, default=False)
    parser.add_argument('-yp', '--yamlPath',nargs='?', const=False, default=False)
    parser.add_argument('-mxs', '--maxSamples', type =int, nargs='?', const=None, default=None)
    parser.add_argument('-m', '--model', type =str, nargs='?', default=False)
    parser.add_argument('-d', '--downloadData', action='store_true')
    parser.add_argument('-f', '--filterCoco', action='store_true')
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-b', '--batch_size', type =int, nargs='?', const=32, default=32)
    parser.add_argument('-aa', '--augAmmount', type =int, nargs='?', const=5, default=5)
    parser.add_argument('-c', '--copyFiles', action='store_true')
    parser.add_argument('-md', '--modData', action='store_true')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-r', '--resume', action='store_true')
    parser.add_argument('-s', '--split',  type =str, nargs='?', const="validation",default="validation")
    parser.add_argument('-e', '--epochs',  type =int, nargs='?', const=400, default=400)
    parser.add_argument('-v', '--validate', action='store_true')
    parser.add_argument('-ca', '--certainAlloc', action='store_true')
    parser.add_argument('-uc', '--useCOCO', action='store_true')
    parser.add_argument('-red', '--reducedImages', action='store_true')
    parser.add_argument('-svn', '--saveFolderName', type =str, nargs='?', const="OfficialSaveFolder", default="OfficialSaveFolder")

    args = parser.parse_args()

    # exit and give an error if -ds already exists
    if args.dataWhileRunningDirectory != None and os.path.exists(args.dataWhileRunningDirectory):
        print("Error: --dataWhileRunningDirectory already exists")
        exit()
    
    augmentFinalFolder = args.modDirectory if args.modData else args.addDatasetPath

    saveDirName = getSaveDirName(args)

    #Check if AlreadyCompleted exists
    if os.path.exists(os.path.join(saveDirName,args.saveFolderName, "AlreadyCompleted")):
        print("AlreadyCompleted exists, exiting")
        exit()

    if args.downloadData:
        downLoadData(args.initialDataStorageDirectory, args.middleDataStorageDirectory, args.split, args.maxSamples, args)
    if args.filterCoco:
        # convertLabelValues()
        filterCoco(args.middleDataStorageDirectory, args)
    if args.copyFiles:
        CopyFiles(args.dataStorageDirectory, args.middleDataStorageDirectory, args)
        saveDirName = saveRelevantData(args, saveDirName)

    if args.add:
        print("potentiall adding")
        addPotentiallyAugmented(args.dataStorageDirectory, args.addDatasetPath, args)
    if args.validate:
        if args.model == False:
            model = "yolo11l.pt"
        else:
            model = "/app/{}/{}/weights/best.pt".format(args.model,args.name)

        validate(args.dataStorageDirectory, model = model)

    if args.train:
        if args.resume and args.model:
            model = "/app/{}/{}/weights/best.pt".format(args.model,args.name)
        elif args.resume and not args.model:
            model ="/app/runs/detect/train/weights/last.pt"
        elif not args.resume and args.model:
           model =  args.model
        elif not args.resume and not args.model:
          model =  "yolo11n.yaml"
        
        train(model, saveDirName ,args)
