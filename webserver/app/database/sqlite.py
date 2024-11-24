
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
                weights REAL DEFAULT 0.0,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

# ------------------ User Management Functions ------------------
def db_register_user(uname: str, pw_hash: str) -> bool:
    """Register a new user and create their unique table."""
    create_users_table_if_not_exists()
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
        # TODO clean up
        # print(f"User {uname} registered successfully.")
        return True

def db_delete_user(uname: str) -> bool:
    """Delete a user and their image directory if it exists."""
    create_users_table_if_not_exists()
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
    
def update_record(user: str, object_name: str, new_p1: Optional[tuple] = None, new_p2: Optional[tuple] = None, new_img_url: Optional[str] = None):
    """Update specific fields of a record in the user's table."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        table_name = get_table_name_for_user(user)
        update_fields = []
        params = []

        if new_p1:
            update_fields.append("p1 = ?")
            params.append(f"{new_p1[0]},{new_p1[1]}")
        if new_p2:
            update_fields.append("p2 = ?")
            params.append(f"{new_p2[0]},{new_p2[1]}")
        if new_img_url:
            update_fields.append("img_url = ?")
            params.append(new_img_url)

        params.append(object_name)
        query = f'''
            UPDATE {table_name}
            SET {", ".join(update_fields)}
            WHERE object_name = ?
        '''
        cur.execute(query, tuple(params))
        conn.commit()

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
            INSERT INTO {table_name} (object_name, p1, p2, img_url, weights, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (output_pkt.object_name, p1_str, p2_str, img_url, output_pkt.weight, created_at))

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
            SELECT object_name, p1, p2, img_url, weights, created_at
            FROM {table_name}
            WHERE object_name = ?
            ORDER BY id DESC
        ''', (object_name,))
        results = cur.fetchall()
        if len(results) > index:
            row = results[index]
            object_name, p1, p2, img_url, weight, created_at = row
            p1 = tuple(map(float, p1.strip('[]').split(',')))
            p2 = tuple(map(float, p2.strip('[]').split(',')))
            return ImgObject(user, object_name, (p1), (p2), img_url, weight, created_at)
    
    return None

def db_query_range(user: str, object_name: str, low: int, high: int) -> Optional[list[ImgObject]]:
    """Query an object from the database by user name and object name."""

    if high< 0 or low <0 or high<low:
        return None

    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            SELECT object_name, p1, p2, img_url, weights, created_at
            FROM {table_name}
            WHERE object_name = ?
            ORDER BY id DESC
        ''', (object_name,))
        
    results = cur.fetchall()

    if low >= len(results):
        return None  
    high = min(high, len(results)) 

    img_objects = []
    for row in results[low:high]:
        object_name, p1, p2, img_url, weight, created_at = row
        p1 = tuple(map(float, p1.strip('[]').split(',')))
        p2 = tuple(map(float, p2.strip('[]').split(',')))
        img_object = ImgObject(user, object_name, p1, p2, img_url, weight, created_at)
        img_objects.append(img_object)
    
    return img_objects if img_objects else None

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

# ------------------ Further Functionality ------------------
def purge_old_records(user: str, cutoff_date: datetime):
    """Delete records older than a specified cutoff date."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        table_name = get_table_name_for_user(user)
        cutoff_date_str = cutoff_date.isoformat()
        cur.execute(f'''
            DELETE FROM {table_name}
            WHERE created_at < ?
        ''', (cutoff_date_str,))
        conn.commit()


def modify_row(user: str, object_name: str, **updates) -> bool:
    """
    Modify a row in the user's unique table.
    """
    if not updates:
        return False  
    
    #TODO: @Giancarlo: do you want this to create a new table and add entry if it doesnt exist? Or return false?
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)

    set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
    values = list(updates.values()) + [object_name]

    with get_db_connection() as conn:
        cur = conn.cursor()
      
        cur.execute(f"SELECT 1 FROM {table_name} WHERE object_name = ?", (object_name,))
        if cur.fetchone() is None:
            return False  
        
     
        cur.execute(f'''
            UPDATE {table_name}
            SET {set_clause}
            WHERE object_name = ?
        ''', values)
        conn.commit()
        return True
    
def delete_row(user: str, object_name: str) -> bool:
    """
    Delete a row in the user's table based on the object_name.
    """
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM {table_name} WHERE object_name = ?", (object_name,))
        if cur.fetchone() is None:
            return False 
        
        # Delete the row
        cur.execute(f"DELETE FROM {table_name} WHERE object_name = ?", (object_name,))
        conn.commit()
        return True
    
def find_lowest_weight_object(user: str) -> Optional[ImgObject]:
    """Finds the object with the lowest weight in the user's table."""
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            SELECT object_name, p1, p2, img_url, weights, created_at
            FROM {table_name}
            ORDER BY weights ASC
            LIMIT 1
        ''')
        
        row = cur.fetchone()
        if row:
            object_name, p1, p2, img_url, weight, created_at = row
            p1 = tuple(map(float, p1.strip('[]').split(',')))
            p2 = tuple(map(float, p2.strip('[]').split(',')))
            return ImgObject(user, object_name, p1, p2, img_url, weight, created_at)
    
    print(f"No entries found for user '{user}'.")
    return None


def get_lowest_weight_for_object(user: str, object_name: str) -> Optional[ImgObject]:
    """
    Returns the entry with the lowest weight for a specific user and object.
    """
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)
    
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            SELECT object_name, p1, p2, img_url, weights, created_at
            FROM {table_name}
            WHERE object_name = ?
            ORDER BY weights ASC
            LIMIT 1
        ''', (object_name,))
        
        row = cur.fetchone()
        if row:
            object_name, p1, p2, img_url, weight, created_at = row
            p1 = tuple(map(float, p1.strip('[]').split(',')))
            p2 = tuple(map(float, p2.strip('[]').split(',')))
            return ImgObject(user, object_name, p1, p2, img_url, weight, created_at)
        else:
            return None
# ------------------ Other Functions ------------------
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
                weights REAL DEFAULT 0.0,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_users_table_if_not_exists():
    """Create the users table if it does not exist."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uname TEXT NOT NULL UNIQUE,
                pw_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_blacklist_table_if_not_exists():
    """Create the blacklist table if it does not exist."""
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS blacklist (
                token_id TEXT PRIMARY KEY,
                exp INTEGER NOT NULL
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
    create_blacklist_table_if_not_exists()
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
    create_blacklist_table_if_not_exists()
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


def db_get_all_unique_objects(user: str) -> Optional[list]:
    """Retrieve all unique objects for a user from the database."""
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)

    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'''
            SELECT object_name, p1, p2, img_url, weights, created_at
            FROM {table_name}
            ORDER BY id DESC
        ''')
        
        results = cur.fetchall()
        unique_objects = {}
        
        for row in results:
            object_name, p1, p2, img_url, weight, created_at = row
            p1 = tuple(map(float, p1.strip('[]').split(',')))
            p2 = tuple(map(float, p2.strip('[]').split(',')))
            
            if object_name not in unique_objects:
                unique_objects[object_name] = ImgObject(user, object_name, p1, p2, img_url, weight, created_at)
        
        return list(unique_objects.values()) if unique_objects else None

def print_user_table(user: str):
    """Prints the entire table for a given user."""
    create_user_table_if_not_exists(user)
    table_name = get_table_name_for_user(user)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {table_name}')
        rows = cur.fetchall()
        
        if not rows:
            print(f"No entries found in table for user '{user}'.")
            return
        
        print(f"Table for user '{user}':")
        for row in rows:
            print(row)




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



