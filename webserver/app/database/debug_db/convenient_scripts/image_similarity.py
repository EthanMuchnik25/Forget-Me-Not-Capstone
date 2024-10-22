# Calculates similartiy of images compared to each other in one directory
# ngl this is very slow
# I wanted to eventually delete duplicate images but this is more work than it's
#  worth

# NOTE: This doesn't really fulfill my goal and so I have not added the relevant
#  libraries to the requirements.txt. The libraries are:
#  pip3 install pillow scikit-image numpy
#  Feel free to install them on your local version if curious

import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray

directory = "../../debug_db_store/prev/old_imgs"

def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            img_path = os.path.join(directory, filename)
            images.append((Image.open(img_path), filename))
    return images

def compute_similarity_matrix(images):
    num_images = len(images)
    similarity_matrix = np.zeros((num_images, num_images))

    for i in range(num_images):
        img1, _ = images[i]
        img1_gray = rgb2gray(np.array(img1))

        for j in range(num_images):
            img2, _ = images[j]
            print(i,j)

            if img1.size != img2.size:
                # Set similarity to 0 if dimensions are different
                similarity_matrix[i, j] = 0
            elif i != j:
                # Convert to grayscale and compute SSIM
                img2_gray = rgb2gray(np.array(img2))
                # Calculate the data range for SSIM
                data_range = img1_gray.max() - img1_gray.min()  # Both images should have the same range
                # Compute SSIM
                similarity_matrix[i, j] = ssim(img1_gray, img2_gray, data_range=data_range)

    return similarity_matrix

def main(directory):
    images = load_images_from_directory(directory)
    if not images:
        print("No JPEG images found in the specified directory.")
        return
        
    similarity_matrix = compute_similarity_matrix(images)
    
    # Displaying the similarity matrix
    print("Similarity Matrix:")
    print(similarity_matrix)
    
    # Optionally save the matrix to a file
    np.savetxt("similarity_matrix.csv", similarity_matrix, delimiter=",")
    print("Similarity matrix saved to 'similarity_matrix.csv'.")

if __name__ == "__main__":
    main(directory)
