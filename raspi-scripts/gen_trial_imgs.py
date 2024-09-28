import os
import sys
from picamzero import Camera
import time


dataset_path_str = "./temp_images/lil_dataset"
secs_per_img = 3 # note: cannot do <2.5s, camera takes too long to take photo
total_time_mins = 2
total_imgs = (total_time_mins * 60) // secs_per_img



# Ensure script always executes from the same places
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

# Make a new directory for the upcoming dataset
counter = 0
while(True):
    dataset_path = f"{dataset_path_str}_{counter}"
    if not os.path.exists(dataset_path):
        print(f"new dataset path: {dataset_path}")
        os.makedirs(dataset_path)
        break
    else:
        counter += 1

cam = Camera()

for i in range(total_imgs):
    start_time = time.time()

    img_name = f"img_{start_time:.0f}.jpg"
    img_path = os.path.join(dataset_path, img_name)
    
    cam.take_photo(img_path)
    elapsed_time = time.time() - start_time

    print(f"Took photo {img_path} in {elapsed_time:.2f} seconds")
    # Adjust sleep time based on the time taken to take the photo
    time.sleep(max(0, secs_per_img - elapsed_time))