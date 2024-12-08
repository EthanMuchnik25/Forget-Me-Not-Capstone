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

from PreprocessData import downLoadData, filterCoco, CopyFiles, addDataset, addPotentiallyAugmented, saveRelevantData, loadArgparse

def validate(model = "yolo11n.yaml", args = None):

    # Load the YOLOv11 model
    print("model is: ", model)
    model = YOLO(model=model, task="detect")
    # Perform object detection
    metrics = model.val(data=os.path.join(args.dataStorageDirectory, "data.yaml"), batch=32, imgsz=640, rect=True, half=True, warmup_bias_lr=0.0, project=args.model, name=args.saveFolderName)
    

    # output the map50 for each class
    # print(metrics)
    # print(metrics.results_dict)
    # print(metrics.maps)
    # print(metrics.names)

    # write metrics to a file called metrics.txt
    print("path is: ", os.path.join(args.model, args.saveFolderName , "metrics.txt"))
    with open(os.path.join(args.model, str(metrics.save_dir.name) , "metrics.txt"), "w") as f:
        f.write(str(metrics.results_dict))
        f.write("\n")
        for key in metrics.names:
            f.write(str(metrics.names[key]) + " : " + str(metrics.maps[key]) + "\n")

    # Create a file called modelfile.txt and write the model path to it
    print("path is: ", os.path.join(args.model, args.saveFolderName , "modelfile.txt"))
    with open(os.path.join(args.model, str(metrics.save_dir.name) , "modelfile.txt"), "w") as f:
        f.write(os.path.join(args.model, args.name, "weights", "best.pt"))

    

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
    parser.add_argument('-n', '--name', type =str, nargs='?', const="OfficialSaveFolder", default="OfficialSaveFolder")
    parser.add_argument('-svn', '--saveFolderName', type =str, nargs='?', const="OfficialValFolder", default="OfficialValFolder")

    newRoundArgs = parser.parse_args()
    args = loadArgparse(newRoundArgs)
    args.model = newRoundArgs.model
    args.certainAlloc = True
    args.validate = True
    args.name = args.saveFolderName
    args.saveFolderName = newRoundArgs.saveFolderName

    if args.downloadData:
        downLoadData(args.initialDataStorageDirectory, args.middleDataStorageDirectory, args.split, args.maxSamples, args)
    if args.filterCoco:
        # convertLabelValues()
        filterCoco(args.middleDataStorageDirectory, args)
    if args.copyFiles:
        CopyFiles(args.dataStorageDirectory, args.middleDataStorageDirectory, args)

    if args.add:
        addPotentiallyAugmented(args.dataStorageDirectory, args.addDatasetPath, args)
    
    if args.validate:
        if args.model == False:
            model = "yolo11l.pt"
        else:
            model = "/app/{}/{}/weights/best.pt".format(args.model,args.name)
        print("args.savFolderName is: ", args.saveFolderName)
        validate(model = model, args = args)
