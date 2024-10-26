import torch
from transformers import AutoModelForObjectDetection, AutoProcessor
import cv2
import matplotlib.pyplot as plt

# Load the Grounding DINO model and processor
model = AutoModelForObjectDetection.from_pretrained("IDEA-Research/groundingdino")
processor = AutoProcessor.from_pretrained("IDEA-Research/groundingdino")

# use argparse to get image path
import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--image_path', type=str, default='/app/datasets/Images//Detecting-Pencils-2\\test\\images\\Office-18_jpg.rf.03c7ac1774f4f21c2212a10e63a8e493.jpg')
args = parser.parse_args()


# Load image
image_path = args.image_path
image = cv2.imread(image_path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define the prompt (what object you're grounding)
prompt = "a pencil"

# Preprocess the image and text prompt
inputs = processor(images=rgb_image, text=prompt, return_tensors="pt")

# Forward pass (object detection)
with torch.no_grad():
    outputs = model(**inputs)

# Post-process detection
logits = outputs.logits  # logits represent class scores
boxes = outputs.pred_boxes  # predicted bounding boxes

# Visualize the results
def visualize_boxes(image, boxes, prompt):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.imshow(image)
    for box in boxes:
        xmin, ymin, xmax, ymax = box.tolist()
        rect = plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                             fill=False, edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        ax.text(xmin, ymin, prompt, bbox=dict(facecolor='red', alpha=0.5), fontsize=12, color='white')
    plt.show()

# Convert from normalized coordinates to image coordinates
image_height, image_width = rgb_image.shape[:2]
boxes = boxes[0] * torch.tensor([image_width, image_height, image_width, image_height])

# Visualize results
visualize_boxes(rgb_image, boxes, prompt)
