import cv2
import os
from PIL import Image

folderName = "F:\Data\Office Images"

def convert_avif_to_jpg(input_path, output_path):
    try:
        # Open the AVIF image file
        image = Image.open(input_path)
        # Convert AVIF to RGB (required for JPG format)
        image = image.convert('RGB')
        # Save the image as JPG
        image.save(output_path, 'JPEG')
        print(f"Conversion successful! Saved as {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
# COnvert each image to jpg

for filename in os.listdir(folderName):
    if filename.endswith(".png"):
        print(filename)
        img = cv2.imread(os.path.join(folderName, filename))
        cv2.imwrite(os.path.join(folderName, filename.replace(".png", ".jpg")), img)
        os.remove(os.path.join(folderName, filename))
        print("Converted")
    elif filename.endswith(".webp"):
        print(filename)
        img = cv2.imread(os.path.join(folderName, filename))
        cv2.imwrite(os.path.join(folderName, filename.replace(".webp", ".jpg")), img)
        os.remove(os.path.join(folderName, filename))
        print("Converted")
    elif filename.endswith(".jpeg"):
        print(filename)
        img = cv2.imread(os.path.join(folderName, filename))
        cv2.imwrite(os.path.join(folderName, filename.replace(".jpeg", ".jpg")), img)
        os.remove(os.path.join(folderName, filename))
        print("Converted")
    elif filename.endswith(".avif"):
        # remove avif file from file system
        os.remove(os.path.join(folderName, filename))
    


