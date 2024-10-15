from app.config import Config

# Import database
if Config.DATABASE_VER == "RDS":
    # TODO make all imports import the same fn name
    from app.database.rds import query_db
elif Config.DATABASE_VER == "SQLITE":
    raise NotImplementedError
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db import db_get_image
else:
    raise NotImplementedError


def fs_get_room_img(db_ret):
    # NOTE: May be none
    img = db_get_image(db_ret.img_url)

    # TODO in the future we would process the image here, with like bounding 
    #  boxes and whatever else

    return img

    
    