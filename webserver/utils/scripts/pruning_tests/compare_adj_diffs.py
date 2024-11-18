import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim


def extract_number(file_path):
    # Strip the path and extract the filename
    filename = file_path.split('/')[-1]  # Get the part after the last '/'
    number_str = filename[len('image_'):-len('.jpg')]  # Extract the number part
    return int(number_str)  # Return the number as an integer

def get_dataset_imgs_list(directory):
    img_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                img_list.append(file_path)
    img_list = sorted(img_list, key=extract_number)

    return img_list


def load_img(image1_path):
        # Open the images
    img1 = Image.open(image1_path).convert('RGB')

    return np.array(img1)

def mse(img1_arr, img2_arr):
    
    # Compute the Mean Squared Error (MSE)
    mse_value = np.sum((img1_arr - img2_arr) ** 2) / float(img1_arr.shape[0] * img1_arr.shape[1])
    return mse_value

def abs_diff(img1_arr, img2_arr):
    return np.sum(np.abs(img1_arr - img2_arr)) / float(img1_arr.shape[0] * img2_arr.shape[1])

def ssim_diff(img1_arr, img2_arr):
    # Compute the Structural Similarity Index (SSIM)
    ssim_value, _ = ssim(img1_arr, img2_arr, full=True, channel_axis=2)
    return ssim_value


def write_mse():
    diff_file = open("./uncommitted/mse_diffs.txt","w")
    img_list = get_dataset_imgs_list("../../imgs/dataset_0")

    prev_img = load_img(img_list[0])
    
    for curr_img_path in img_list[1:]:
        curr_img = load_img(curr_img_path)
        mse_curr = mse(prev_img, curr_img)
        del prev_img
        prev_img = curr_img
        
        diff_file.write(f"{curr_img_path} {mse_curr}\n")
        # print(f"{curr_img_path} {mse_curr}")

# This shit takes longer than a whole ass inference...
def write_ssim():
    diff_file = open("./uncommitted/ssim_diffs2.txt","w")
    img_list = get_dataset_imgs_list("../../imgs/dataset_0")

    prev_img = load_img(img_list[0])
    
    for curr_img_path in img_list[1:]:
        curr_img = load_img(curr_img_path)
        mse_curr = ssim_diff(prev_img, curr_img)
        del prev_img
        prev_img = curr_img
        
        diff_file.write(f"{curr_img_path} {mse_curr}\n")
        print(f"{curr_img_path} {mse_curr}")

def write_abs():
    diff_file = open("./uncommitted/abs_diffs.txt","w")
    img_list = get_dataset_imgs_list("../../imgs/dataset_0")

    prev_img = load_img(img_list[0])
    
    for curr_img_path in img_list[1:]:
        curr_img = load_img(curr_img_path)
        mse_curr = abs_diff(prev_img, curr_img)
        del prev_img
        prev_img = curr_img
        
        diff_file.write(f"{curr_img_path} {mse_curr}\n")
        # print(f"{curr_img_path} {mse_curr}")

def main():
    # write_mse()
    # write_ssim()
    write_abs()
    

if __name__ == "__main__":
    main()