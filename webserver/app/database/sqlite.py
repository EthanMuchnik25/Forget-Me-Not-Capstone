
import sqlite3
import os
from datetime import datetime
from typing import Optional
from app.database.types_db import ImgObject
from io import BytesIO

# Database and image directory setup
temp_dir = "./app/database/sqlite_db/"
temp_imgs_dir = "./app/database/sqlite_db/"
db_store_file_path = os.path.join(temp_dir, "object_tracking.db")
os.makedirs(temp_dir, exist_ok=True)

# ------------------ Helper Function for Connections ------------------
def get_db_connection():
    """Opens a new database connection."""
    conn = sqlite3.connect(db_store_file_path)
    conn.row_factory = sqlite3.Row  
    return conn

def get_table_name_for_user(username: str) -> str:
    """Generate a unique table name for each user."""
    return f"object_tracking_{username}"

# ------------------ Database Setup Functions ------------------
def setup_user_table(username: str):
    """Create a unique table for each new user."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        table_name = get_table_name_for_user(username)
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                object_name TEXT NOT NULL,
                p1 REAL NOT NULL,
                p2 REAL NOT NULL,
                img_url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

# ------------------ User Management Functions ------------------
def db_register_user(uname: str, pw_hash: str) -> bool:
    """Register a new user and create their unique table."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE uname = ?", (uname,))
        if cur.fetchone() is not None:
            return False  # User already exists

        cur.execute("INSERT INTO users (uname, pw_hash) VALUES (?, ?)", (uname, pw_hash))
        conn.commit()

        # Setup a unique table for the new user
        setup_user_table(uname)
        user_dir = os.path.join(temp_imgs_dir, uname)
        os.makedirs(user_dir, exist_ok=True)
        os.chmod(user_dir, 0o777)
        print(f"User {uname} registered successfully.")
        return True

def db_delete_user(uname: str) -> bool:
    """Delete a user and their image directory if it exists."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE uname = ?", (uname,))
        if cur.fetchone() is None:
            return False  # User does not exist

        cur.execute("DELETE FROM users WHERE uname = ?", (uname,))
        conn.commit()

        table_name = get_table_name_for_user(uname)
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

        user_dir = os.path.join(temp_imgs_dir, uname)
        if os.path.isdir(user_dir):
            import shutil
            shutil.rmtree(user_dir)
        return True

def db_get_user_pw(uname: str) -> Optional[str]:
    """Retrieve the password hash for a specified user from the database."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT pw_hash FROM users WHERE uname = ?", (uname,))
        result = cur.fetchone()
        return result["pw_hash"] if result else None

# ------------------ Image Storage and Retrieval Functions ------------------

def db_write_line(user: str, output_pkt: ImgObject) -> bool:
    """Insert a record into the user's unique table for tracking an object."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        table_name = get_table_name_for_user(user)
        created_at = datetime.fromtimestamp(output_pkt.time).isoformat()
        img_url = os.path.join("app", "database", "sqlite_db", user, output_pkt.img_url)
        p1_str = f"{output_pkt.p1[0]},{output_pkt.p1[1]}"
        p2_str = f"{output_pkt.p2[0]},{output_pkt.p2[1]}"

        # Insert the new object record into the user's table
        cur.execute(f'''
            INSERT INTO {table_name} (object_name, p1, p2, img_url, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (output_pkt.object_name, p1_str, p2_str, img_url, created_at))

        conn.commit()
        return True

def db_save_image(user: str, f, name: str) -> bool:
    """Save an image and metadata in the user's unique table."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE uname = ?", (user,))
        if cur.fetchone() is None:
            return False  # User not found

        # Save image to user directory
        user_dir = os.path.join(temp_imgs_dir, user)
        os.makedirs(user_dir, exist_ok=True)
        os.chmod(user_dir, 0o777)
        img_path = os.path.join(user_dir, name)
        f.save(img_path)
        os.chmod(img_path, 0o777)

        return True

def db_query_single(user: str, object_name: str, index: int) -> Optional[ImgObject]:
    """Query an object from the database by user name and object name."""
    if index < 0:
        return None

    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            SELECT object_name, p1, p2, img_url, created_at
            FROM {table_name}
            WHERE object_name = ?
            ORDER BY id DESC
        ''', (object_name,))
        
        results = cur.fetchall()
        if len(results) > index:
            row = results[index]
            object_name, p1, p2, img_url, created_at = row
            return ImgObject(user, object_name, (p1), (p2), img_url, created_at)
    
    return None

def db_get_image(user: str, img_url: str) -> Optional[bytes]:
    """Retrieve an image based on user and image URL from their unique table."""
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            table_name = get_table_name_for_user(user)
            cur.execute(f"SELECT img_url FROM {table_name} WHERE img_url = ?", (img_url,))
            if cur.fetchone() is None:
                return None  

            with open(img_url, "rb") as img_file:
                img_data = img_file.read()
                return BytesIO(img_data)
            
    except (FileNotFoundError, PermissionError):
        return None

def create_user_table_if_not_exists(user: str):
    """Create a user-specific table if it does not exist."""
    table_name = get_table_name_for_user(user)
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                object_name TEXT NOT NULL,
                p1 REAL NOT NULL,
                p2 REAL NOT NULL,
                img_url TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

def delete_record(user: str, object_name: str):
    """Delete a specific record from the user's unique table."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        table_name = get_table_name_for_user(user)
        cur.execute(f'''
            DELETE FROM {table_name}
            WHERE object_name = ?
        ''', (object_name,))
        conn.commit()
        print(f"Record(s) deleted for user: {user}, object: {object_name}")

# ------------------ Token Blacklist Functions ------------------

def db_add_token_blacklist(token_id: str, exp: int) -> bool:
    """Add a token to the blacklist with its expiration timestamp."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO blacklist (token_id, exp) VALUES (?, ?)", (token_id, exp))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def db_check_token_blacklist(token_id: str) -> bool:
    """Check if a token is in the blacklist."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM blacklist WHERE token_id = ?", (token_id,))
        return cur.fetchone() is not None
    

# ------------------ Debugging Functions ------------------

def list_all_tables():
    """Retrieve and print all table names in the current SQLite database."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        for table in tables:
            print(table[0])  # Each table name is in a tuple (name,)
    return [table[0] for table in tables] 




# ------------------ DO NOT DELETE ------------------
# Has implementation of extra functionality that i want to include

# import sqlite3
# from typing import Optional
# import os
# import atexit
# from datetime import datetime
# from app.database.types_db import ImgObject, ImgObjectQuery

# # Directory for storing database and images
# temp_dir = "./app/database/sqlite_db/"
# temp_imgs_dir = "./app/database/sqlite_db/"
# db_store_file_path = os.path.join(temp_dir, "object_tracking.db")
# os.makedirs(temp_dir, exist_ok=True)

# # Connect to SQLite database
# conn = sqlite3.connect(db_store_file_path)
# cur = conn.cursor()

# # Create tables if they don't exist
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS object_tracking (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user TEXT NOT NULL,
#         object_name TEXT NOT NULL,
#         p1 REAL NOT NULL,
#         p2 REAL NOT NULL,
#         img_url TEXT NOT NULL,
#         created_at TEXT NOT NULL
#     )
# ''')

# cur.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         uname TEXT UNIQUE NOT NULL,
#         pw_hash TEXT NOT NULL
#     )
# ''')

# cur.execute('''
#     CREATE TABLE IF NOT EXISTS blacklist (
#         token_id TEXT PRIMARY KEY,
#         exp INTEGER NOT NULL
#     )
# ''')

# conn.commit()

# # Cleanup function to ensure database connection is closed properly
# def cleanup():
#     conn.commit()
#     cur.close()
#     conn.close()

# atexit.register(cleanup)

# # =================== Database Interaction Functions ======================


# # ------------------ Image Storage Function ------------------
# def db_write_line(line: ImgObject):
#     """Write an image object line to the database."""
#     cur.execute('''
#         INSERT INTO object_tracking (user, object_name, p1, p2, img_url, created_at)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (line.user, line.object_name, line.p1[0], line.p1[1], line.img_url, line.created_at))
#     conn.commit()

# def db_save_image(user: str, f, name: str, object_name: str, p1: tuple, p2: tuple) -> bool:
#     """Save an image object photo and store its metadata in the SQLite database."""
#     cur.execute("SELECT 1 FROM users WHERE uname = ?", (user,))
#     if cur.fetchone() is None:
#         return False  # User not found
    
#     user_dir = os.path.join(temp_imgs_dir, user)
#     os.makedirs(user_dir, exist_ok=True)
#     os.chmod(user_dir, 0o777)
    
#     img_path = os.path.join(user_dir, name)
#     f.save(img_path)
#     os.chmod(img_path, 0o777)
    
#     #TODO: Change but i dont think just the time is good enough for querying 
#     created_at = datetime.now().isoformat() 
#     img_url = img_path
    
#     cur.execute('''
#         INSERT INTO object_tracking (user, object_name, p1, p2, img_url, created_at)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (user, object_name, p1[0], p1[1], img_url, created_at))
#     conn.commit()
#     return True


# # ------------------ Image Retrieval Functions ------------------

# def db_query_single(user: str, object_name: str, index: int) -> Optional[ImgObject]:
#     """Query an object from the database by user name and object name"""
#     if index < 0:
#         return None
    
#     # Query the correct columns: p1, p2, and filter by user and object_name
#     cur.execute('''
#         SELECT user, object_name, p1, p2, img_url, created_at
#         FROM object_tracking
#         WHERE user = ? AND object_name = ?
#         ORDER BY id DESC
#     ''', (user, object_name))
    
#     results = cur.fetchall()
#     print("query: ", user, object_name, results)
#     view_all_records()

#     if len(results) > index:
#         row = results[index]
#         user, object_name, p1, p2, img_url, created_at = row
#         # TODO: store as bounding box coordinates
#         return ImgObject(user, object_name, p1, p2, img_url, created_at)
    
#     return None



# def db_get_image(user: str, img_url: str) -> Optional[bytes]:
#     """Retrieve an image based on user and image URL."""
#     try:
#         # Check if the user exists in the database
#         cur.execute("SELECT img_url FROM object_tracking WHERE user = ? AND img_url = ?", (user, img_url))
#         result = cur.fetchone()
#         # print ("get_image:", user, img_url, result)
#         if result is None:
#             return None  # No such image for this user
        
#         # Attempt to open the image file using the URL provided
#         with open(img_url, "rb") as img_file:
#             return img_file.read()  # Return the image data as bytes
#     except (FileNotFoundError, PermissionError):
#         return None
    


# def view_all_records():
#     """Fetch and display all records from the object_tracking table."""
#     cur.execute('SELECT * FROM object_tracking')
#     rows = cur.fetchall()
    
#     if rows:
#         for row in rows:
#             print(row)
#     else:
#         print("No records found in the table.")


# def delete_record(user_name: str, object_name: str):
#     """Delete a specific record from the object_tracking table."""
#     cur.execute('''
#         DELETE FROM object_tracking 
#         WHERE user = ? AND object_name = ?
#     ''', (user_name, object_name))
#     conn.commit()
#     print(f"Record(s) deleted for user: {user_name}, object: {object_name}")



# # User Authentication Functions

# def db_register_user(uname: str, pw_hash: str) -> bool:
#     """Register a new user and create their directory if they don't already exist."""
#     # Check if the username already exists
#     cur.execute("SELECT 1 FROM users WHERE uname = ?", (uname,))
#     user_exists = cur.fetchone()  # Save the result to a variable

#     if user_exists is not None:
#         print(f"User {uname} already exists.")
#         return False
    
#     # Insert the new user
#     cur.execute("INSERT INTO users (uname, pw_hash) VALUES (?, ?)", (uname, pw_hash))
#     conn.commit()

#     # Create a directory for the user’s images
#     user_dir = os.path.join(temp_imgs_dir, uname)
#     os.makedirs(user_dir, exist_ok=True)
#     os.chmod(user_dir, 0o777)
#     print(f"User {uname} registered successfully.")
    
#     return True

# def db_delete_user(uname: str) -> bool:
#     """Delete a user from the database and remove their image directory if it exists."""
#     cur.execute("SELECT 1 FROM users WHERE uname = ?", (uname,))
#     if cur.fetchone() is None:
#         return False
    
#     cur.execute("DELETE FROM users WHERE uname = ?", (uname,))
#     conn.commit()
    
#     user_dir = os.path.join(temp_imgs_dir, uname)
#     if os.path.isdir(user_dir):
#         try:
#             os.rmdir(user_dir)
#         except OSError:
#             import shutil
#             shutil.rmtree(user_dir)
    
#     return True

# def db_get_user_pw(uname: str) -> Optional[str]:
#     """Retrieve the password hash for a specified user from the database."""
#     cur.execute("SELECT pw_hash FROM users WHERE uname = ?", (uname,))
#     result = cur.fetchone()
#     return result[0] if result else None

# # Token Blacklist Functions

# def db_add_token_blacklist(token_id: str, exp: int) -> bool:
#     """Add a token to the blacklist with its expiration timestamp."""
#     try:
#         cur.execute("INSERT INTO blacklist (token_id, exp) VALUES (?, ?)", (token_id, exp))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
    
# def db_check_token_blacklist(token_id: str) -> bool:
#     """Check if a token is in the blacklist."""
#     cur.execute("SELECT 1 FROM blacklist WHERE token_id = ?", (token_id,))
#     return cur.fetchone() is not None




# # TODO: Querying based on username and object name 
# # def db_query_single(input_pkt, index) -> Optional[ImgObject]:
# #     """Query an object from the database by user name and object name"""
# #     if index < 0:
# #         return None

# #     # Query the correct columns: p1, p2
# #     cur.execute('''
# #         SELECT user, object_name, p1, p2, img_url, created_at
# #         FROM object_tracking
# #         WHERE user = ? AND object_name = ?
# #         ORDER BY id DESC
# #     ''', (input_pkt.user, input_pkt.object_name))
    
# #     results = cur.fetchall()

# #     if len(results) > index:
# #         row = results[index]
# #         user, object_name, p1, p2, img_url, created_at = row
# #         # TODO: store as bounding box corrdinates 
# #         return ImgObject(user, object_name, (p1), (p2), img_url, created_at)
    
# #     return None

# ###########################  Unit Testing  ####################################
# # # Setup sample data
# # print("Updating the db...")
# # user = "john doe"
# # class_obj = 5
# # x_coord = 7.0
# # y_coord = 7.0
# # image_path = "static/swaglab.jpg"  # need to provide a valid path
# # created_at = datetime.now()

# # # Create an ImgObject to insert into the SQLite database
# # output_pkt = ImgObject(user=user, 
# #                        object_name=str(class_obj), 
# #                        p1=(x_coord, y_coord), 
# #                        p2=(x_coord, y_coord), 
# #                        img_url=image_path, 
# #                        created_at=created_at)

# # db_write_line(output_pkt)

# # # Query the object to check if it was inserted correctly
# # print("Now, querying the db...")
# # object_name = '5' 
# # user_name = 'john doe'
# # input_pkt = ImgObjectQuery(user_name,object_name)
# # queried_object = db_query_single(input_pkt, 0)  

# # # Check the result of the query
# # if queried_object:
# #     print(f"Queried Object: {queried_object}")
# # else:
# #     print("No object found in the database.")

# # delete_all_records()
# # view_all_records()
# ##############################################################################



