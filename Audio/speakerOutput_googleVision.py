import os
# from google.cloud import vision
import io
from google.auth import credentials  # Keep only necessary imports

# def query_google_vision_model(image_path, object_name):
#     """
#     Queries Google Vision API to find the location of an object in an image.
    
#     :param image_path: Path to the image file.
#     :param object_name: The object to locate in the image.
#     :return: Location description of the object or an appropriate response.
#     """
#     try:
#         api_key = os.getenv("GOOGLE_API_KEY")

#         # Instantiate the Image Annotator client with the API key
#         client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})

#         # Load the image file into memory
#         with open(image_path, "rb") as image_file:
#             content = image_file.read()

#         # Create an image instance
#         image = vision.Image(content=content)

#         # Send the image to the Vision API for object localization
#         response = client.object_localization(image=image)

#         # Handle errors if they exist
#         if response.error.message:
#             raise Exception(f"Error: {response.error.message}")

#         # Iterate through the detected objects and find the object of interest
#         for object_ in response.localized_object_annotations:
#             if object_.name.lower() == object_name.lower():
#                 # Return bounding box coordinates and object name
#                 location_info = {
#                     "object": object_.name,
#                     "confidence": object_.score,
#                     "bounding_box": object_.bounding_poly
#                 }
#                 return location_info
        
#         return f"Object '{object_name}' not found in the image."

#     except Exception as e:
#         return f"An error occurred: {str(e)}"



# def test_query(image_path):
#     """
#     Queries Google Vision API to detect all objects in an image.
    
#     :param image_path: Path to the image file.
#     :return: List of detected objects with their confidence and bounding box coordinates.
#     """
#     try:
#         # Set the API key (you can set it as an environment variable or hardcode it)
#         api_key = os.getenv("GOOGLE_API_KEY")

#         # Instantiate the Image Annotator client with the API key
#         client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})

#         # Load the image file into memory
#         with open(image_path, "rb") as image_file:
#             content = image_file.read()

#         # Create an image instance
#         image = vision.Image(content=content)

#         # Send the image to the Vision API for object localization
#         response = client.object_localization(image=image)

#         # Handle errors if they exist
#         if response.error.message:
#             raise Exception(f"Error: {response.error.message}")

#         # List to hold all detected objects
#         detected_objects = []

#         # Iterate through the detected objects
#         for object_ in response.localized_object_annotations:
#             detected_objects.append({
#                 "object": object_.name,
#                 "confidence": object_.score,
#                 "bounding_box": object_.bounding_poly
#             })
        
#         return detected_objects

#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# if __name__ == "__main__":
#     image_path = "/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"  # Replace with the path to your image
#     object_name = "pen"  # The object you're looking for in the image
    
#     # location_description = query_google_vision_model(image_path, object_name)
    
#     # if isinstance(location_description, dict):
#     #     print(f"Object '{location_description['object']}' found with confidence {location_description['confidence'] * 100}%")
#     #     print(f"Bounding box coordinates: {location_description['bounding_box']}")
#     # else:
#     #     print(location_description)

#     detected_objects = test_query(image_path)
    
#     if isinstance(detected_objects, list) and detected_objects:
#         print(f"Detected objects in the image:")
#         for obj in detected_objects:
#             print(f"Object: {obj['object']}")
#             print(f"Confidence: {obj['confidence'] * 100:.2f}%")
#             print(f"Bounding box coordinates: {obj['bounding_box']}")
#             print("-" * 50)
#     else:
#         print(detected_objects)

import os
from google.cloud import vision

def detect_objects_in_image(image_path):
    """Detect objects in the image using Google Cloud Vision API with an API Key."""
    api_key = os.getenv("GOOGLE_API_KEY")
    client = vision.ImageAnnotatorClient(client_options={"api_key": api_key})

    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    if response.error.message:
        raise Exception(f"Error with Vision API: {response.error.message}")

    return objects

def generate_location_description(objects, object_name):
    """Generate a location description for the detected objects."""
    descriptions = []
    
    for obj in objects:
        if object_name.lower() in obj.name.lower():
            vertices = obj.bounding_poly.normalized_vertices
            top_left = (vertices[0].x, vertices[0].y)
            top_right = (vertices[1].x, vertices[1].y)
            bottom_right = (vertices[2].x, vertices[2].y)
            bottom_left = (vertices[3].x, vertices[3].y)

            location = "unknown location"
            if top_left[1] < 0.2:
                location = "at the top of the image, possibly on a shelf or wall"
            elif bottom_left[1] > 0.8:
                location = "at the bottom of the image, possibly on a desk or floor"
            elif top_left[0] < 0.5:
                location = "on the left side of the image"
            else:
                location = "on the right side of the image"
            
            description = f"The {object_name} is detected at {location}."
            descriptions.append(description)
    
    return descriptions

if __name__ == "__main__":
    image_path = "/Users/swatianshu/Documents/Fall 2024/18500/Forget-Me-Not-Capstone/Audio/testimgs/study.png"  # Replace with your image path
    object_name = "keyboard"  # Replace with the object you want to locate
    
    try:
        objects = detect_objects_in_image(image_path)
        descriptions = generate_location_description(objects, object_name)

        print("Detected objects and their locations:")
        for desc in descriptions:
            print(desc)
    except Exception as e:
        print(f"An error occurred: {str(e)}")