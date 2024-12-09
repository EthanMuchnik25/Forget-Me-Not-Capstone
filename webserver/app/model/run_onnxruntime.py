import cv2
import onnxruntime as ort
import numpy as np

# Load the class names manually (since they were previously available from model.names in the ultralytics package)
# Update this list with the correct names for your model
class_names = [f"class_{a}" for a in range(10000)]

# Load the ONNX model using onnxruntime
model_path = "./app/model/binaries/yolo11l.onnx"
session = ort.InferenceSession(model_path)

def preprocess_image(image, input_size=(640, 640)):
    # Resize the image and normalize it
    image = cv2.resize(image, input_size)
    image = image / 255.0  # Normalize to 0-1
    image = image.transpose(2, 0, 1)  # Change shape to (C, H, W)
    image = np.expand_dims(image, axis=0).astype(np.float32)  # Add batch dimension and convert to float32
    return image

def postprocess_output(output, image_shape, input_size=(640, 640), conf_threshold=0.5):
    # Extract dimensions
    height, width = image_shape[:2]
    ret = []

    # The model output format depends on the model architecture; YOLO models often have a specific format
    for detection in output[0]:  # assuming batch size of 1
        confidence = detection[4]  # confidence of detection
        if confidence > conf_threshold:
            scores = detection[5:]
            cls = np.argmax(scores)  # Class with highest confidence
            cls_name = class_names[cls]

            # Extract bounding box in YOLO format (x_center, y_center, width, height normalized)
            x_center, y_center, box_width, box_height = detection[0:4]

            # Append detection to results
            ret.append((cls_name, x_center, y_center, box_width, box_height))
    return ret

def run_yolo(f):
    # Read and preprocess the image
    image = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
    input_image = preprocess_image(image)

    # Run inference
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    output = session.run([output_name], {input_name: input_image})[0]

    # Postprocess output
    results = postprocess_output(output, image.shape)

    # Return results as list of YOLO output tuples
    return results
