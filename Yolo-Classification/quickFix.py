import os
import imageio

def quickFix(folderName):
    files = os.listdir(folderName)
    
    # Rename files
    for file in files:
        os.rename(os.path.join(folderName, file), os.path.join(folderName, "swati" + file))

    # Convert .jpg files to .png
    for filename in os.listdir(folderName):
        if filename.endswith(".jpg"):
            img_path = os.path.join(folderName, filename)
            try:
                img = imageio.imread(img_path)
                output_path = os.path.join(folderName, filename.replace(".jpg", ".png"))
                imageio.imwrite(output_path, img)
                print(f"Converted {img_path} to {output_path}")
            except Exception as e:
                print(f"Error: Unable to load image {img_path}. {e}")
    
    # Convert .jpeg files to .png
    for filename in os.listdir(folderName):
        if filename.endswith(".jpeg"):
            img_path = os.path.join(folderName, filename)
            try:
                img = imageio.imread(img_path)
                output_path = os.path.join(folderName, filename.replace(".jpeg", ".png"))
                imageio.imwrite(output_path, img)
                os.remove(img_path)
                print(f"Converted {img_path} to {output_path}")
            except Exception as e:
                print(f"Error: Unable to load image {img_path}. {e}")

# Example usage
quickFix("C:\\Users\\muchn\\Downloads\\Swati-Photos")