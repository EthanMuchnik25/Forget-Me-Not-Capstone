# given a folder containing text files i want the first character  of each file to be changed from 0 to 9 and then a 1 added after it
modText = "80"

def modifyFile(myFile):
    # Open the file
    file = open(myFile, "r")
    text = file.read()
    file.close()

    # Modify the "first few characters until the first space of each line"
    
    #for each line
    lines = text.split("\n")
    for i in range(len(lines)):
        line = lines[i]
        #for each character in the line
        for j in range(len(line)):
            #if the character is a space
            if line[j] == " ":
                #modify the first character
                lines[i] = modText + line[j:]
                break
    # Join the lines back together
    text = "\n".join(lines)
    

    # Write the modified text back to the file
    file = open(myFile, "w")
    file.write(text)
    file.close()

def modifyFiles(folder):
    # Get all the files in the folder
    import os
    files = os.listdir(folder)

    # Modify each file
    for file in files:
        print(file)
        modifyFile(os.path.join(folder, file))

# Modify all the files in the folder
modifyFiles("./datasets/Images/Detecting-Pencils-1/train/labels/")