import app.database.types_db as types
from typing import Optional
import os
import atexit
import json
from app.database.types_db import ImgObject

img_ctr = 0
temp_imgs_dir = "./app/database/debug_imgs/"
db_store_file_path = temp_imgs_dir + "database.json"
os.makedirs(temp_imgs_dir, exist_ok=True)

db = []

# Reload old database
if os.path.exists(db_store_file_path):
    with open(db_store_file_path, "r") as file:
        l = json.load(file)
        for item in l:
            db.append(ImgObject(**item))

# Save current database
def cleanup():
    with open(db_store_file_path, "w") as file:
        json.dump(db, file, default=ImgObject.to_dict)

atexit.register(cleanup)
# I think this works...


# =================== Real Functions ======================
def db_write_line(line : types.ImgObject):
    """Write an image object line to the database"""
    db.append(line)


def db_save_image(f, name):
    """Save an image object photo"""
    f.save(temp_imgs_dir + name)


def db_query_single(object, index) -> Optional[types.ImgObject]:
    """Query an object from the database"""
    if index < 0:
        return None

    for item in reversed(db):
        if item.object_name == object:
            if index == 0:
                return item
            else:
                index -= 1
    return None

# I don't exactly know what sort of things s3 and sqlite implementation will
#  return but I imagine they will be file-like
def db_get_image(name):
    """Get an image from a filename"""
    try:
        return open(temp_imgs_dir + name, "rb")
    except (FileNotFoundError, PermissionError):
        return None