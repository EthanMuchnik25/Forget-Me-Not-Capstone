from app.config import Config
import numpy as np
import cv2
from io import BytesIO

# Import database
if Config.DATABASE_VER == "RDS":
    # TODO make all imports import the same fn name
    from app.database.rds import query_db
elif Config.DATABASE_VER == "SQLITE":
    from app.database.sqlite import db_query_single, db_get_image
    # raise NotImplementedError
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db.debug_db import db_get_image
else:
    raise NotImplementedError


# TODO should these be config vars?
font_scale = 1
font_thickness = 5
rect_line_thickness = 7
def draw_boxes(img_handle, obj):
    nparr = np.frombuffer(img_handle.read(), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    height, width, _ = img.shape

    
    x1 = int(obj.p1[0] * width)
    y1 = int(obj.p1[1] * height)
    x2 = int(obj.p2[0] * width)
    y2 = int(obj.p2[1] * height)
    
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), rect_line_thickness)
    cv2.putText(img, f'Class: {obj.object_name}', (x1, y1 - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 0, 0), 
                font_thickness)    

    # Encode the image back to a byte array
    _, img_encoded = cv2.imencode('.jpg', img)  # You can choose the format
    img_bytes = BytesIO(img_encoded.tobytes())  # Convert to BytesIO for file-like access

    # Reset the cursor to the start of the BytesIO object
    img_bytes.seek(0)

    return img_bytes

def fs_get_room_img(user, db_ret):
    # NOTE: May be none
    img = db_get_image(user, db_ret.img_url)
    # print ("img:", user, db_ret.img_url)
    if img == None:
        return None

    box_img = draw_boxes(img, db_ret)

    img.close()

    return box_img

    
    