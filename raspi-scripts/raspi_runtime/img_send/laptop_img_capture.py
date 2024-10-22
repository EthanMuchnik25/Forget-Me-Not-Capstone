import cv2
import atexit


def cleanup():
    # Release the camera
    cap.release()

    # Optionally, close all OpenCV windows
    cv2.destroyAllWindows()

atexit.register(cleanup)

# Open the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    raise Exception("Error: Could not open laptop camera")

temp_img_name = "imgs/temp_img.jpg"

def capture_image():
    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(temp_img_name, frame)
    else:
        print("Error: Could not read frame.")
    return temp_img_name

