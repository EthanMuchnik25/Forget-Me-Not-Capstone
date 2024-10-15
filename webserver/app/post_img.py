from app.config import Config

# Import YOLO
if Config.YOLO_VER == "MOCK":
  from fakes.fake_yolo import run_yolo
else:
  # TODO swap this with the real yolo
  raise NotImplementedError

# Import database
if Config.DATABASE_VER == "RDS":
  # TODO BAD BAD BAD BAD Make good interface
  from app.database.rds import rds_database
elif Config.DATABASE_VER == "SQLITE":
  from app.database.sqlite import TODO
else:
  raise NotImplementedError


# TODO not great name
def handle_img(f):

    yolo_output_filename = run_yolo(f)
    with open(yolo_output_filename, 'r') as file:
        data = file.read()
        # parsing logic
        # yolo output types:
        # class obj, x_center, y_center, width, height
        parsed_output = []
        for line in data.strip().split('\n'):
            #splitting each line into individual coordinates 
            parts = line.split()
            class_obj = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            x_coord = x_center + width/2 
            y_coord = y_center + height/2 
            user = "john_doe" #maybe removed depending on architecture 
            image_path = "yolo_output_filename"  
            output_pkt = (user, class_obj, (x_coord, y_coord), image_path)
            # parsed_output.append(output_pkt)
            # return output_pkt #?? gotta test 
            rds_database(output_pkt)

# print(parsed_output)



