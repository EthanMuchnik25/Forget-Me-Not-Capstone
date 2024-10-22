from typing import Optional
import os
import atexit
import json
import time
if __name__ == '__main__':
    import types_db as types
else:
    import app.database.types_db as types
from werkzeug.datastructures import FileStorage

if __name__ == '__main__':
    temp_imgs_dir =  "./debug_db_store/users/"
    creds_file_path =     "./debug_db_store/credentials/creds.json"
    blacklist_file_path = "./debug_db_store/expired_tokens/bl.json"
else:
    temp_imgs_dir = "./app/database/debug_db_store/users/"
    creds_file_path = "./app/database/debug_db_store/credentials/creds.json"
    blacklist_file_path = "./app/database/debug_db_store/expired_tokens/bl.json"

os.makedirs(temp_imgs_dir, exist_ok=True)

db = {}

users = {}

blacklist = {}

try:
    for root, dirs, files in os.walk(temp_imgs_dir):
        for dir in dirs:
            # Reload user database
            curr_dir_db_path = os.path.join(root, dir, "database.json")
            if os.path.exists(curr_dir_db_path):
                with open(curr_dir_db_path, "r") as file:
                    l = json.load(file)
                    db[dir] = []
                    for item in l:
                        db[dir].append(types.ImgObject(**item))
            else:
                db[dir] = []
    
    if os.path.exists(creds_file_path):
        with open(creds_file_path, "r") as file:
            users = json.load(file)

    if os.path.exists(blacklist_file_path):
        with open(blacklist_file_path, "r") as file:
            blacklist = json.load(file)
    t = time.time()
    # Clean up irrelevant values and cast to float
    blacklist = {key: float(value) for key, value in blacklist.items() if float(value) >= t}


    # TODO remove old code
    # # Reload old database
    # if os.path.exists(db_store_file_path):
    #     with open(db_store_file_path, "r") as file:
    #         l = json.load(file)
    #         for item in l:
    #             db.append(ImgObject(**item))
except Exception as e:
    print(f"Reloading databse failed, something probably changed: {e}")


# Save current database
def cleanup():
    for key in db:
        user_dir = os.path.join(temp_imgs_dir, key)
        os.makedirs(user_dir, exist_ok=True)
        os.chmod(user_dir, 0o777)

        db_store_file_path = os.path.join(user_dir, "database.json")
        with open(db_store_file_path, "w") as file:
            json.dump(db[key], file, default=types.ImgObject.to_dict)
        os.chmod(db_store_file_path, 0o777)

    os.makedirs(os.path.dirname(creds_file_path), exist_ok=True)
    with open(creds_file_path, "w") as file:
        json.dump(users, file)
    os.chmod(creds_file_path, 0o777)

    t = time.time()
    # Clean up irrelevant values
    global blacklist
    blacklist = {key: value for key, value in blacklist.items() if value >= t}

    os.makedirs(os.path.dirname(creds_file_path), exist_ok=True)
    with open(blacklist_file_path, "w") as file:
        json.dump(blacklist, file)
    os.chmod(blacklist_file_path, 0o777)

    # TODO remove old code
    # with open(db_store_file_path, "w") as file:
    #     json.dump(db, file, default=ImgObject.to_dict)

atexit.register(cleanup)


# TODO add some sort of user id to all fns. For not probably username
# =================== Real Functions ======================
def db_write_line(user, line : types.ImgObject):
    """Write an image object line to the database"""

    if user in db:
        db[user].append(line)
        return True
    else:
        return False


def db_save_image(user, f, name):
    """Save an image object photo"""

    if user not in db:
        return False
    
    user_dir = os.path.join(temp_imgs_dir, user)
    os.makedirs(user_dir,exist_ok=True)
    os.chmod(user_dir, 0o777)

    img_path = os.path.join(user_dir,name)
    f.save(img_path)
    os.chmod(img_path, 0o777)
    return True


def db_query_single(user, object, index) -> Optional[types.ImgObject]:
    """Query an object from the database"""
    if index < 0:
        return None
        
    if user not in db:
        return None

    for item in reversed(db[user]):
        if item.object_name == object:
            if index == 0:
                return item
            else:
                index -= 1
    return None

# I don't exactly know what sort of things s3 and sqlite implementation will
#  return but I imagine they will be file-like
def db_get_image(user, name):
    """Get an image from a filename"""
    try:
        if not user in db:
            return None
        
        user_dir = os.path.join(temp_imgs_dir, user)
        return open(os.path.join(user_dir, name), "rb")
    except (FileNotFoundError, PermissionError):
        return None
    

# ======== Authentication ========

# TODO these can all be tested in isolation, make sure we can store and restore
#  before using them to test other stuff
def db_register_user(uname, pw_hash):
    if uname not in users:
        users[uname] = pw_hash
        db[uname] = []
        
        user_dir = os.path.join(temp_imgs_dir, uname)
        os.makedirs(user_dir, exist_ok=True)
        os.chmod(user_dir, 0o777)


        return True
    else:
        return False

def db_delete_user(uname):
    return users.pop(uname, None)
# TODO not sure when we will call this atm
# TODO current behavior is don't delete data. Doesn't matter right now but could
# have security ramifications in the future. Make sure this is talked about

def db_get_user_pw(uname):
    return users.get(uname)

def db_add_token_blacklist(token_id, exp):
    blacklist[token_id] = exp

def db_check_token_blacklist(token_id):
    return token_id in blacklist
    # return blacklist.get(token_id) # TODO remove/change?



# =================== Local Testing ======================


def clear_dirs():
    global blacklist
    global users
    global db
    blacklist = {}
    users = {}
    db = {}
    import shutil
    if os.path.exists(temp_imgs_dir):
        shutil.rmtree(temp_imgs_dir)  # Remove the directory and all its contents
        os.makedirs(temp_imgs_dir) 
        os.chmod(temp_imgs_dir, 0o777)

    os.remove(creds_file_path)
    os.remove(blacklist_file_path)

if __name__ == '__main__':
    pass

    # # NOTE: Traces appear to work

    # # NOTE: be very careful with uncommenting this!!
    # clear_dirs()

    # print(f"time: {time.time()}")

    # # WARNING: This is not how these functions will typically be used (arg 
    # # types), but it does let me test functionality
    # usr1 = "name a"
    # usr3 = "name c"
    # print(f"pw a on restart: {db_get_user_pw(usr1)}")
    # print(f"bl 1 on restart: {db_check_token_blacklist('token id')}")
    # db_register_user(usr1, "12345")
    # db_register_user("name b", "54321")
    # db_register_user(usr3, "6789")
    # print(f"pw a on insert: {db_get_user_pw(usr1)}")
    # db_delete_user("name b")

    # db_add_token_blacklist("token id", 1729999999)
    # db_add_token_blacklist("token id 2", 1729999998)
    # print(f"bl 1 on insert: {db_check_token_blacklist('token id')}")


    # temp_img_name_1 = "samp_name.jpg"
    # temp_img_path_1 = "./debug_db_store/prev/baby/1728986829.7109988.jpg"
    # with open(temp_img_path_1, "rb") as file:
    #     f = FileStorage(stream=file,filename=temp_img_name_1)
    #     db_save_image(usr1, f, temp_img_name_1)
    # temp_imgobj = types.ImgObject(usr1, "person", (1.0,1.0), (1.0,1.0), temp_img_name_1, 1)
    # db_write_line(usr1, temp_imgobj)

    # with open(temp_img_path_1, "rb") as file:
    #     f = FileStorage(stream=file,filename=temp_img_name_1)
    #     db_save_image(usr3, f, temp_img_name_1)
    # temp_imgobj = types.ImgObject(usr3, "kite", (2.0,2.0), (2.0,2.0), temp_img_name_1, 1)
    # db_write_line(usr3, temp_imgobj)

    # print(f"Db query usr1: {db_query_single(usr1, 'person', 0)}")
    # print(f"Db query usr3: {db_query_single(usr3, 'kite', 0)}")

    # # Be very careful uncommenting this!
    # # clear_dirs()



