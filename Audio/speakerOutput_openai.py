import openai
import os
from PIL import Image

openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_to_png(image_path):
    with Image.open(image_path) as img:
        new_image_path = image_path.rsplit('.', 1)[0] + '.png'
        img.save(new_image_path, 'PNG')
    return new_image_path

def resize_image(image_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        new_image_path = image_path.rsplit('.', 1)[0] + '_resized.png'
        img.save(new_image_path, 'PNG')
    return new_image_path

def check_image(image_path):
    if not image_path.lower().endswith('.png'):
        raise ValueError("Uploaded image must be a PNG format.")
    if os.path.getsize(image_path) > 4 * 1024 * 1024:
        raise ValueError("Uploaded image must be less than 4 MB.")
    return True

def query_openai_vision_model(image_path, object_name):
    try:
        # Ensure the image is in PNG format and under 4 MB
        # check_image(image_path)
        # print("check", check_image)
        
        if os.path.getsize(image_path) > 4 * 1024 * 1024:
            image_path = resize_image(image_path)
        if not image_path.lower().endswith('.png'):
            image_path = convert_to_png(image_path)
        
        with open(image_path, "rb") as image_file:
            response = openai.Image.create_edit(
                image=image_file,
                prompt=f"Where is the {object_name} located in this image?",
                n=1,  
                size="1024x1024",  
            )
        print("API Response:", response)


        if 'choices' in response and len(response['choices']) > 0:
            location_info = response['choices'][0].get("text", "").strip()
            return location_info if location_info else "No location information provided."
        else:
            return "No valid response from the API."

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    image_path = "/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"  
    object_name = "keyboard"  
    location_description = query_openai_vision_model(image_path, object_name)
    print(f"Location of the '{object_name}': {location_description}")