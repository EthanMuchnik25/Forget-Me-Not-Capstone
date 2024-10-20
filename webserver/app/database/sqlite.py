import sqlite3
from typing import Optional
import os
import atexit
from datetime import datetime
from app.database.types_db import ImgObject, ImgObjectQuery

# Setup
img_ctr = 0
# TODO this directory should only be for my debug database, feel free to make a 
#  new one for this. Also I am changing its name.
temp_imgs_dir = "./app/database/debug_imgs/"
db_store_file_path = temp_imgs_dir + "object_tracking.db"
os.makedirs(temp_imgs_dir, exist_ok=True)

# Connect to SQLite database
conn = sqlite3.connect(db_store_file_path)
cur = conn.cursor()

# Create table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS object_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        object_name TEXT NOT NULL,
        p1 REAL NOT NULL,
        p2 REAL NOT NULL,
        img_url TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
''')
conn.commit()

# Cleanup function to ensure database connection is closed properly
def cleanup():
    conn.commit()
    cur.close()
    conn.close()

atexit.register(cleanup)

# =================== Real Functions ======================

def db_write_line(line: ImgObject):
    """Write an image object line to the database"""
    cur.execute('''
        INSERT INTO object_tracking (user, object_name, p1, p2, img_url, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (line.user, line.object_name, line.p1[0], line.p1[1], line.img_url, line.created_at))
     # TODO: store as bounding box corrdinates 
    conn.commit()

def db_save_image(f, name):
    """Save an image object photo"""
    f.save(os.path.join(temp_imgs_dir, name))


def db_query_single(object_name: str, index: int) -> Optional[ImgObject]:
    """Query an object from the database by object name only"""
    if index < 0:
        return None

    # Query the correct columns: p1, p2
    cur.execute('''
        SELECT user, object_name, p1, p2, img_url, created_at
        FROM object_tracking
        WHERE object_name = ?
        ORDER BY id DESC
    ''', (object_name,))
    
    results = cur.fetchall()

    if len(results) > index:
        row = results[index]
        user, object_name, p1, p2, img_url, created_at = row
        # TODO: store as bounding box coordinates
        return ImgObject(user, object_name, p1, p2, img_url, created_at)
    
    return None

def db_get_image(name):
    """Get an image from a filename"""
    try:
        return open(os.path.join(temp_imgs_dir, name), "rb")
    except (FileNotFoundError, PermissionError):
        return None

def view_all_records():
    """Fetch and display all records from the object_tracking table."""
    cur.execute('SELECT * FROM object_tracking')
    rows = cur.fetchall()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found in the table.")



def delete_all_records():
    """Delete all records from the object_tracking table."""
    cur.execute('DELETE FROM object_tracking')
    conn.commit()
    print("All records have been deleted.")


def delete_record(user_name: str, object_name: str):
    """Delete a specific record from the object_tracking table."""
    cur.execute('''
        DELETE FROM object_tracking 
        WHERE user = ? AND object_name = ?
    ''', (user_name, object_name))
    conn.commit()
    print(f"Record(s) deleted for user: {user_name}, object: {object_name}")



# TODO: Querying based on username and object name 
# def db_query_single(input_pkt, index) -> Optional[ImgObject]:
#     """Query an object from the database by user name and object name"""
#     if index < 0:
#         return None

#     # Query the correct columns: p1, p2
#     cur.execute('''
#         SELECT user, object_name, p1, p2, img_url, created_at
#         FROM object_tracking
#         WHERE user = ? AND object_name = ?
#         ORDER BY id DESC
#     ''', (input_pkt.user, input_pkt.object_name))
    
#     results = cur.fetchall()

#     if len(results) > index:
#         row = results[index]
#         user, object_name, p1, p2, img_url, created_at = row
#         # TODO: store as bounding box corrdinates 
#         return ImgObject(user, object_name, (p1), (p2), img_url, created_at)
    
#     return None

###########################  Unit Testing  ####################################
# # Setup sample data
# print("Updating the db...")
# user = "john doe"
# class_obj = 5
# x_coord = 7.0
# y_coord = 7.0
# image_path = "static/swaglab.jpg"  # need to provide a valid path
# created_at = datetime.now()

# # Create an ImgObject to insert into the SQLite database
# output_pkt = ImgObject(user=user, 
#                        object_name=str(class_obj), 
#                        p1=(x_coord, y_coord), 
#                        p2=(x_coord, y_coord), 
#                        img_url=image_path, 
#                        created_at=created_at)

# db_write_line(output_pkt)

# # Query the object to check if it was inserted correctly
# print("Now, querying the db...")
# object_name = '5' 
# user_name = 'john doe'
# input_pkt = ImgObjectQuery(user_name,object_name)
# queried_object = db_query_single(input_pkt, 0)  

# # Check the result of the query
# if queried_object:
#     print(f"Queried Object: {queried_object}")
# else:
#     print("No object found in the database.")

# delete_all_records()
# view_all_records()
##############################################################################