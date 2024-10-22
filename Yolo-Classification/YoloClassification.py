import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
# from transformers import pipeline


def runifmain():
    # Load the YOLOv8 model
    model = YOLO("C:\\Users\\muchn\\train47\\weights\\best.pt")
    # model = YOLO("C:\\Users\\muchn\\Documents\\Classes\\18500\\Forget-Me-Not-Capstone\\Yolo-Classification\\YoloTrainingRes\\50epochLargeTrainMinorAugRoboflowBothPencilDatasets-NotBadProbCouldUseNoDefaultPencilDataset\\weights\\best.pt")
    
    #change the default path to dataset.yaml
    

    model.to('cpu')

    # Perform object detection
    # C:\\Users\\muchn\\Documents\\Classes\\18500\\Forget-Me-Not-Capstone\\Yolo-Classification\\YoloTrainingRes\\50epochLargeTrainMinorAugRoboflowBothPencilDatasets-NotBadProbCouldUseNoDefaultPencilDataset\\weights\\best.pt
    results = model('C:\\Users\\muchn\\Documents\\Classes\\18500\\Forget-Me-Not-Capstone\\Yolo-Classification\\datasets\\Images\\Detecting-Pencils-2\\test\\images\\Office-44_jpg.rf.e73e6f403da5fb79594d3810831f1873.jpg'    )
    # print(result.boxes.map50)
    # Access the first image result (if you're processing multiple images, iterate over them)
    result = results[0]
    

    # access the labels from the result
    # print(result.labels)

    # Display the image with detections
    result.show()

    # Save photo
    # result.save('datasets/Images/monitor2.png')


def runifmain2():
    # Load model directly
    pipe = pipeline("object-detection", model="jozhang97/deta-swin-large")   

    # Perform object detection
    results = pipe("image.jpg")
    
    # Display the image with detections
    print(results)
    img = cv2.imread("image.jpg")
    for obj in results:
        # print(result)
        # for obj in result:
            print(obj)
            x1, y1, x2, y2 = obj['box'].values()
            # x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            print(x1, y1, x2, y2)
            print("types", type(x1), type(y1), type(x2), type(y2))

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, obj['label'], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("image", img)
    cv2.waitKey(0)

def runifmain3():
     # get yolov4 model
    model = YOLO('yolov4.pt')

    # perform object detection
    results = model('image.jpg')

    # display the image with detections
    results.show()




if __name__ == "__main__":
    runifmain() 