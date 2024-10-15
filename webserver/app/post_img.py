from app.config import Config
from app.database.types_db import ImgObject
import time

# Import YOLO
if Config.YOLO_VER == "MOCK":
    from fakes.fake_yolo import run_yolo
else:
    # TODO swap this with the real yolo
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


def parse_yolo_line(line):
    # parsing logic
    # yolo output types:
    # class obj, x_center, y_center, width, height

    #splitting each line into individual coordinates 
    parts = line.split()
    class_obj = int(parts[0])
    x_center = float(parts[1])
    y_center = float(parts[2])
    width = float(parts[3])
    height = float(parts[4])
    x_coord = x_center + width/2 
    y_coord = y_center + height/2
    return (class_obj, (x_coord, y_coord))

# TODO not great name
def handle_img(f):

    img_time = time.time()
    image_path = str(img_time) + ".jpg"


    # TODO implement
    yolo_output_filename = run_yolo(f)

    with open(yolo_output_filename, 'r') as file:
        data = file.read()
        
        db_save_image(f, image_path)

        for line in data.strip().split('\n'):
            parsed_line = parse_yolo_line(line)

            user = "john_doe" #maybe removed depending on architecture 


            output_pkt = ImgObject(user, str(parsed_line[0]), parsed_line[1], image_path)
            db_write_line(output_pkt)




