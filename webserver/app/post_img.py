from app.config import Config
from app.database.types_db import ImgObject
import time

# Import YOLO
if Config.YOLO_VER == "MOCK":
    from fakes.fake_yolo import run_yolo
elif Config.YOLO_VER == "V11":
    from app.model.run_yolo import run_yolo
else:
    raise NotImplementedError

# Import database
if Config.DATABASE_VER == "RDS":
    from app.database.rds import db_write_line
elif Config.DATABASE_VER == "SQLITE":
    raise NotImplementedError
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db import db_write_line, db_save_image
else:
    raise NotImplementedError


# TODO: weird code, vals keep getting casted between float and int... 
#  check run_yolo()
def parse_yolo_line(parts):
    # parsing logic
    # yolo output types:
    # class obj, x_center, y_center, box width, box height

    class_obj = parts[0]
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])
    x1 = x_center - width/2
    y1 = y_center - height/2
    x2 = x_center + width/2 
    y2 = y_center + height/2
    return (class_obj, (x1, y1), (x2, y2))

# TODO not great name
def handle_img(f):

    img_time = time.time()
    image_path = str(img_time) + ".jpg"

    yolo_output = run_yolo(f)
    print(yolo_output)
        
    f.seek(0)
    db_save_image(f, image_path)
    for line in yolo_output:
        parsed_line = parse_yolo_line(line)
        user = "john_doe" #maybe removed depending on architecture 
        output_pkt = ImgObject(user, str(parsed_line[0]), parsed_line[1], parsed_line[2], image_path)
        db_write_line(output_pkt)




