from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO("./binaries/yolo11l.pt")

    model.export(format="onnx")

else:
    raise Exception("This file was not intended to be run from anywhere else")