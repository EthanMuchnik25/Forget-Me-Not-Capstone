# import matplotlib.pyplot as plt
# from ultralytics import YOLO

# # Load the YOLOv8 model
# model = YOLO('YoloModels/yolov10b.pt')

# # Perform object detection
# model.train(data="data.yaml", epochs=25, imgsz=640, batch=8)

from ultralytics import settings

print(settings)
