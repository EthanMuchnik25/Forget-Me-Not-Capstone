
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import requests

# Set image path in main

ip = '172.24.156.5'

threshold = 0.30

# TODO should these be config vars?
font_scale = 1
font_thickness = 5
rect_line_thickness = 7


def draw_box(img_handle, obj):
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




# only accepts jpgs
# additional dots in url not supported
def box_and_save(img_path, boxes):
    box_img = None
    with open(img_path, "rb") as img:
        box_img = draw_box(img, boxes)
    
    box_img = Image.open(box_img)

    path_sections = img_path.split('.')
    new_img_path = path_sections[0] + "2." + path_sections[1]
    box_img.save(new_img_path)
    return new_img_path





def make_req(img_path, texts_list):
    url = f'http://{ip}:4000/ask_abadi'
    texts = ""
    for text in texts_list:
        texts = texts + text + " . "
    texts_data = {"texts": texts}
    files = {'file': open(img_path, 'rb')}  # Open the file in binary mode
    data = {'texts': str(texts_data)}
    response = requests.post(url, files=files, data=data)
    files['file'].close()

    if response.status_code == 200:
        print("Request was successful!")
        # print("Response JSON:", response.json())  # If the response is JSON, print it
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)



def make_box(object_name, p1, p2):
    # p1 and p2 should be point pairs, corners of the photo
    class SampleBox:
        pass
    sample_box = SampleBox()
    setattr(sample_box,"user","jaehyun2")
    setattr(sample_box,"object_name",object_name)
    setattr(sample_box,"p1",p1)
    setattr(sample_box,"p2",p2)
    setattr(sample_box,"img_url","1730587826.126515.jpg")
    setattr(sample_box,"time",1730587828.9640784)
    return sample_box


def parse_infs(infs, text_list, height, width):
    # predictions:
    #   scores, labels, bboxes
    # visualizations
    #   useless

    preds = infs['predictions']
    preds = preds[0]

    labels = preds['labels']
    bboxes = preds['bboxes']

    objs = []

    for idx, val in enumerate(preds['scores']):
        if val > threshold:
            print(val)
            label = text_list[labels[idx]]

            bbox = bboxes[idx]
            x1 = bbox[0] / width
            y1 = bbox[1] / height
            x2 = bbox[2] / width
            y2 = bbox[3] / height

            new_box = make_box(label, (x1, y1), (x2, y2))
            objs.append(new_box)
            
    return objs




if __name__ == "__main__":
    class SampleBox:
        pass
    sample_box = make_box("person",[0.606652706861496, 0.0008360445499420166],[0.9991019070148468, 0.9973882138729095])

    img_path = "2testimg.jpg"
    text_list = ["bench", "car", "person"]
    infs = make_req(img_path, text_list)
    if infs == None:
        raise Exception("Inference failed")
    
    with open(img_path, "rb") as img:
        nparr = np.frombuffer(img.read(), np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        height, width, _ = img_np.shape

    boxes = parse_infs(infs, text_list, height, width)

    new_img_path = img_path
    for box in boxes:
        new_img_path = box_and_save(new_img_path, box)
