from app.config import Config
import json
import urllib.parse
from app.database.types_db import ImgObject

# Import database
if Config.DATABASE_VER == "RDS":
    # TODO BAD BAD BAD BAD Make good interface
    from app.database.rds import query_db
elif Config.DATABASE_VER == "SQLITE":
    from app.database.sqlite import db_query_single, db_query_range
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db.debug_db import db_query_single
else:
    raise NotImplementedError


def create_img_url(db_ret):
    json_string = json.dumps(db_ret, default=ImgObject.to_dict)
    url_encoded = urllib.parse.quote(json_string)
    return f"/get_room_img?data={url_encoded}"

def handle_text_query(user, query, index=0):
    if query == 'swaglab':
        response = {
            'imageUrl': f'/static/swaglab.jpg',
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
    if db_ret == None:
        return {
            'success': False,
            'message': "Object not found in database"
        }
        
    # TODO: See what other stuff is necessary in the future 
    return {
        'success': True,
        'imageUrl': create_img_url(db_ret) 
    }
    

def handle_text_range_query(user, query, low=0, high=0):
    try:
        low = int(low)
        high = int(high)
    except ValueError as e:
        return {
            'success': False,
            'message': f"Index error: {e}"
        }
    
    db_ret = db_query_range(user, query, low, high)
    if db_ret == None:
        return {
            'success': False,
            'message': "Object not found in database"
        }
    
    return {
        'success': True,
        'imageUrls': [create_img_url(line) for line in db_ret]
    }
    