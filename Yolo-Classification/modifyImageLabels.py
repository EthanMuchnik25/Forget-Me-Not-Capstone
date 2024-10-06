folderName = "F:\Data\Office Images"
import os

# Make it so each image in folder is labelled sequantially Office-1, Office-2, Office-3 etc assuming all images are already jpgs

i = 1
for filename in os.listdir(folderName):
    if filename.endswith(".jpg"):
        print(filename)
        os.rename(os.path.join(folderName, filename), os.path.join(folderName, f"Office-{i}.jpg"))
        i += 1
        print("Converted")
    else:
        print("Not a jpg file")
