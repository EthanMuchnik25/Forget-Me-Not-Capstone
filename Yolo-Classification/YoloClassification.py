import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
# from transformers import pipeline


def runifmain():
    # Load the YOLOv8 model
    model = YOLO('../YoloTrainingRes/Yolo11X-200-epoch-results/weights/best.pt')

    # Perform object detection
    results = model('datasets/Images/Monitors.jpg')

    # Access the first image result (if you're processing multiple images, iterate over them)
    result = results[0]

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
    model = YOLO('yolov4.pt', 

    # perform object detection
    results = model('image.jpg')

    # display the image with detections
    results.show()




if __name__ == "__main__":
    runifmain()