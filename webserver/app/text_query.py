from app.config import Config
import json
import urllib.parse
from app.database.types_db import ImgObject

# Import database
if Config.DATABASE_VER == "RDS":
    # TODO BAD BAD BAD BAD Make good interface
    from app.database.rds import query_db
elif Config.DATABASE_VER == "SQLITE":
    # raise NotImplementedError
    from app.database.sqlite import db_query_single, db_get_image, view_all_records
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db.debug_db import db_query_single, db_get_image
else:
    raise NotImplementedError


def create_img_url(db_ret):
    json_string = json.dumps(db_ret, default=ImgObject.to_dict)
    url_encoded = urllib.parse.quote(json_string)
    return f"/get_room_img?data={url_encoded}"

def handle_text_query(user, query, index=0):
    if query == 'swaglab':
        print("hi")
        response = {
            'imageUrl': '/static/swaglab.jpg',
            'success': True
        }   
        return response

    elif query == 'sign':
        response = {
            'imageUrl': 'https://i.redd.it/87xuofmvnlud1.png',
            'success': True
        }
        return response

    try:
        index = int(index)
    except ValueError as e:
        return {
            'success': False,
            'message': f"Index error: {e}"
        }
    
    if index < 0:
        return {
            'success': False,
            'message': "Negative photo index"
        }

    db_ret = db_query_single(user, query, index)
    if db_query_single == None:
        # view_all_records()
        return {
            'success': False,
            'message': "Object not found in database"
        }
        
    # TODO: See what other stuff is necessary in the future 
    # print("img_url:", create_img_url(db_ret))
    return {
        'success': True,
        'imageUrl': create_img_url(db_ret) 
        # 'imageUrl' : db_ret.img_url
    }
    
    