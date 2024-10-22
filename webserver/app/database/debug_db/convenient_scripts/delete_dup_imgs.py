# NOTE: This script doesn't really work. For whatever reason it sems like images
#  get ever-so-slightly corrupted to the point they are no longer identical when
#  sending. I don't care enough to fix it.

# This script deletes any duplicate jpg images in a single directory. 
# If you accumulate a directory full of "sample images" from copy pasting the 
#  images from different accounts, there may be duplicates. This would help 
#  eliminate them.

import os
import hashlib

directory = "../../debug_db_store/prev/old_imgs"

def file_hash(file_path):
    """Generate a hash for a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def delete_duplicates(directory):
    """Delete duplicate JPG files in the specified directory."""
    seen_hashes = {}
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            file_path = os.path.join(directory, filename)
            file_hash_value = file_hash(file_path)
            if file_hash_value in seen_hashes:
                print(f"Deleting duplicate file: {file_path}")
                os.remove(file_path)
            else:
                seen_hashes[file_hash_value] = file_path

if __name__ == "__main__":
    delete_duplicates(directory)