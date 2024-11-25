import os
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import json


def analyze_spatial_relationships(detections, image_width, image_height):
    """
    Analyzes spatial relationships between detected objects.
    """
    relationships = {}
    for i, (class_a, bbox_a) in enumerate(detections):
        desc = f"{class_a} is located"
        x1_a, y1_a, x2_a, y2_a = bbox_a

        # Relational context analysis
        if x1_a < 0.1 * image_width:
            desc += " near the left edge"
        elif x2_a > 0.9 * image_width:
            desc += " near the right edge"

        if y1_a < 0.1 * image_height:
            desc += " near the top edge"
        elif y2_a > 0.9 * image_height:
            desc += " near the bottom edge"

        # Compare with other objects
        for j, (class_b, bbox_b) in enumerate(detections):
            if i == j:
                continue
            x1_b, y1_b, x2_b, y2_b = bbox_b

            if x2_a < x1_b:
                desc += f", to the left of {class_b}"
            elif x1_a > x2_b:
                desc += f", to the right of {class_b}"
            elif y2_a < y1_b:
                desc += f", above {class_b}"
            elif y1_a > y2_b:
                desc += f", below {class_b}"

        relationships[class_a] = desc
    return relationships


# BLIP Scene Context Generator
def generate_scene_description(image_path):
    """
    Uses BLIP to generate a scene description.
    """
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Load and process image
    from PIL import Image
    image = Image.open(image_path).convert("RGB")
    inputs = processor(image, return_tensors="pt").to(device)

    # Generate caption
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return caption

def parse_yolo_line(parts):
    """
    Parses a single YOLO output line into structured data.)
    """
    class_obj = parts[0]
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])

    x1 = x_center - (width / 2)
    y1 = y_center - (height / 2)
    x2 = x_center + (width / 2)
    y2 = y_center + (height / 2)

    return class_obj, (x1, y1), (x2, y2)


def main():
    yolo_outputs = [
        ["cat", 0.5, 0.5, 0.2, 0.2],
        ["table", 0.8, 0.8, 0.4, 0.2],
    ]
    image_width, image_height = 1920, 1080 
    detections = [parse_yolo_line(parts) for parts in yolo_outputs]
    relationships = analyze_spatial_relationships(detections, image_width, image_height)
    image_path = "path_to_image.jpg"  
    scene_description = generate_scene_description(image_path)
    print("YOLO Spatial Relationships:")
    print(json.dumps(relationships, indent=2))

    print("\nScene Description from BLIP:")
    print(scene_description)


if __name__ == "__main__":
    main()