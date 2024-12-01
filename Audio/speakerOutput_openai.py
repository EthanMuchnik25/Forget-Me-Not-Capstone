# import os
# from google.cloud import vision

# def detect_objects_in_image(image_path):
#     """Detect objects in the image using Google Cloud Vision API with an API Key."""
    
#     # Set the API key in the environment
#     api_key = os.getenv("GOOGLE_API_KEY")
    
#     # Create a client with the API key (via AnonymousCredentials)
#     client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})
    
#     # Prepare the image
#     with open(image_path, "rb") as image_file:
#         content = image_file.read()
    
#     image = vision.Image(content=content)

#     # Detect object annotations
#     response = client.object_localization(image=image)
#     objects = response.localized_object_annotations

#     if response.error.message:
#         raise Exception(f"Error with Vision API: {response.error.message}")

#     return objects

# def generate_location_description(objects, object_name):
#     """Generate a location description for the detected objects."""
#     descriptions = []
    
#     for obj in objects:
#         if object_name.lower() in obj.name.lower():
#             # Extract bounding box coordinates
#             vertices = obj.bounding_poly.normalized_vertices
#             top_left = (vertices[0].x, vertices[0].y)
#             top_right = (vertices[1].x, vertices[1].y)
#             bottom_right = (vertices[2].x, vertices[2].y)
#             bottom_left = (vertices[3].x, vertices[3].y)

#             # Inference based on position in image (simple rules)
#             location = "unknown location"
#             if top_left[1] < 0.2:
#                 location = "at the top of the image, possibly on a shelf or wall"
#             elif bottom_left[1] > 0.8:
#                 location = "at the bottom of the image, possibly on a desk or floor"
#             elif top_left[0] < 0.5:
#                 location = "on the left side of the image"
#             else:
#                 location = "on the right side of the image"
            
#             description = f"The {object_name} is detected at {location}."
#             descriptions.append(description)
    
#     return descriptions

# if __name__ == "__main__":
#     image_path = "/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"  # Replace with your image path
#     object_name = "keyboard"  # Replace with the object you want to locate
    
#     try:
#         objects = detect_objects_in_image(image_path)
#         descriptions = generate_location_description(objects, object_name)

#         print("Detected objects and their locations:")
#         for desc in descriptions:
#             print(desc)
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


# import openai
# import os
# import base64

# # Set your OpenAI API key
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_openai_image_description(image_path):
#     """
#     Query OpenAI API with an image and return the description of the objects in the image.
    
#     :param image_path: Path to the image file.
#     :return: Description of the objects in the image.
#     """
#     try:
#         # Open the image and convert it to base64
#         with open(image_path, "rb") as image_file:
#             # Convert image to base64
#             encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

#         # Send base64 image to the OpenAI API
#         response = openai.Image.create(
#             prompt="Describe the objects and their locations in the image.",
#             image=encoded_image,
#             n=1
#         )

#         # Assuming OpenAI returns a description or list of objects (depending on the model's capabilities)
#         description = response['data'][0]['text'] if 'text' in response['data'][0] else "No description returned."
#         return description

#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# def list_objects_from_description(description):
#     """
#     Parse the description to extract object names (naive implementation).
    
#     :param description: Text description from OpenAI API.
#     :return: List of objects found in the image.
#     """
#     objects = []
#     for line in description.split('\n'):
#         if line.strip():
#             objects.append(line.strip())
#     return objects

# if __name__ == "__main__":
#     image_path = "/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"  # Replace with your image path
    
#     try:
#         description = get_openai_image_description(image_path)
#         print("Description of objects detected in the image:")
#         print(description)
        
#         # If you want to list out the objects from the description
#         objects = list_objects_from_description(description)
#         print("\nExtracted objects from the description:")
#         for obj in objects:
#             print(obj)
            
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")


import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_openai_vision_model(image_url, object_name):
    """
    Queries the OpenAI Vision model to find the location of an object in an image.
    
    :param image_url: URL of the image hosted on Imgur.
    :param object_name: The object to locate in the image.
    :return: Location description of the object or an appropriate response.
    """
    try:
        response = openai.Image.create_edit(
            image=image_url,
            prompt=f"Where is the {object_name} located in this image?",
            n=1,
            size="1024x1024",  
        )

        # Extract the response and return the location description
        location_info = response.get("choices", [])[0].get("text", "").strip()
        return location_info if location_info else "No location information provided."

    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    image_url = "https://imgur.com/3HJndiR" 
    object_name = "keyboard"  # Replace with the object you want to locate
    
    location_description = query_openai_vision_model(image_url, object_name)
    print(f"Location of the '{object_name}': {location_description}")



# import openai
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.Image.create(
#     model="gpt-4",  # This model ID could change
#     images=["/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"],  
#     prompt="Where is the mug located?",  # Example prompt
# )

# print(response)