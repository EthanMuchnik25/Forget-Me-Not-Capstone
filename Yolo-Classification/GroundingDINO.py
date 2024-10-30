import torch
from groundingdino.util.inference import load_model, load_image, predict, annotate
from PIL import Image
import cv2
import numpy as np

def setup_grounding_dino(model_config_path, model_checkpoint_path):
    """
    Setup Grounding DINO model
    """
    model = load_model(model_config_path, model_checkpoint_path)
    return model

def detect_objects(model, image_path, text_prompt, box_threshold=0.35, text_threshold=0.25):
    """
    Detect objects in an image using Grounding DINO
    """
    # Load image
    image_source, image = load_image(image_path)
    
    # Run inference
    boxes, logits, phrases = predict(
        model=model, 
        image=image, 
        caption=text_prompt, 
        box_threshold=box_threshold,
        text_threshold=text_threshold
    )
    
    return image_source, boxes, logits, phrases

def visualize_detections(image_source, boxes, logits, phrases):
    """
    Visualize detection results
    """
    # Convert boxes to integer coordinates
    boxes_int = boxes.round().int().cpu().numpy()
    
    # Create annotation image
    annotated_frame = image_source.copy()
    
    # Draw boxes and labels
    for box, logit, phrase in zip(boxes_int, logits, phrases):
        x1, y1, x2, y2 = box
        confidence = logit.item()
        
        # Draw rectangle
        cv2.rectangle(
            annotated_frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )
        
        # Add text label
        label = f"{phrase}: {confidence:.2f}"
        cv2.putText(
            annotated_frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            2
        )
    
    return annotated_frame

def main():
    # Model paths
    config_path = "GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    checkpoint_path = "groundingdino_swint_ogc.pth"
    
    # Load model
    model = setup_grounding_dino(config_path, checkpoint_path)
    
    # Example usage
    image_path = "path/to/your/image.jpg"
    text_prompt = "cat . dog . person"  # Objects to detect, separated by periods
    
    # Perform detection
    image_source, boxes, logits, phrases = detect_objects(
        model, 
        image_path, 
        text_prompt
    )
    
    # Visualize results
    annotated_image = visualize_detections(image_source, boxes, logits, phrases)
    
    # Save or display results
    cv2.imwrite("output.jpg", annotated_image)

if __name__ == "__main__":
    main()