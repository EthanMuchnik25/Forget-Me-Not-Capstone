import os
import cv2

# Path to your images and labels folders
images_folder = 'C:\\Users\\muchn\\society20\\train\\images'
labels_folder = 'C:\\Users\muchn\society20\\train\\labels'
output_folder = 'C:\\Users\muchn\society20\\'

# Function to draw bounding boxes
def draw_bounding_boxes(image_path, label_path, output_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    with open(label_path, 'r') as label_file:
        lines = label_file.readlines()

        for line in lines:
            class_id, x_center, y_center, box_width, box_height = map(float, line.strip().split())

            # Convert YOLO format to bounding box coordinates
            x1 = int((x_center - box_width / 2) * width)
            y1 = int((y_center - box_height / 2) * height)
            x2 = int((x_center + box_width / 2) * width)
            y2 = int((y_center + box_height / 2) * height)

            # Draw rectangle on the image
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f'Class: {int(class_id)}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(output_path, image)

# Loop through images and corresponding labels
for filename in os.listdir(images_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(images_folder, filename)
        label_path = os.path.join(labels_folder, filename.replace('.jpg', '.txt').replace('.png', '.txt'))
        output_path = os.path.join(output_folder, filename)

        # Only process if corresponding label file exists
        if os.path.exists(label_path):
            draw_bounding_boxes(image_path, label_path, output_path)

print("Bounding boxes drawn and saved to output folder.")