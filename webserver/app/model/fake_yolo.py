
fake_yolo_filename = "app/model/binaries/fake_yolo_output.txt"



# TODO probably rename
def run_yolo(f):
    print("Warning!! YOLO not implemented!")

    output = []
    with open(fake_yolo_filename, 'r') as file:
        data = file.read()
        
        for line in data.strip().split('\n'):
            parts = line.split()
            output.append(parts)

    return output