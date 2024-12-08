import os
import sys

def count_files_in_folder(folder_path):
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
    return file_count

# Specify the folder path you want to count files in
folder_path = sys.argv[1]
print(f"Total number of files: {count_files_in_folder(folder_path)}")
