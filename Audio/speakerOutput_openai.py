import openai

# Need to setup our OpenAI API key
openai.api_key = "your_openai_api_key"

def query_vision_model(image_path, query):
    """
    Query OpenAI's vision model for object location.
    """
    try:
        with open(image_path, "rb") as image_file:
            response = openai.Image.create_edit(
                image=image_file,
                instructions=query
            )
        return response
    except Exception as e:
        print(f"Error querying OpenAI vision model: {e}")
        return None
    

def get_relationships(objects):
    relationships = []
    for obj1 in objects:
        for obj2 in objects:
            if obj1 == obj2:
                continue
            
            # TODO: replace with ImgObject class information 
            obj1_bottom = obj1['box'][1] + obj1['box'][3] 
            obj2_top = obj2['box'][1]  
            obj1_center_x = obj1['box'][0] + obj1['box'][2] // 2
            obj2_center_x = obj2['box'][0] + obj2['box'][2] // 2
            
            if abs(obj1_bottom - obj2_top) < 20 and abs(obj1_center_x - obj2_center_x) < 50:
                relationships.append(f"{obj1['label']} is on the {obj2['label']}")

            # "Near" relationship
            distance_x = abs(obj1_center_x - obj2_center_x)
            distance_y = abs(obj1['box'][1] - obj2['box'][1])
            if distance_x < 100 and distance_y < 50:
                relationships.append(f"{obj1['label']} is near the {obj2['label']}")

    return relationships

if __name__ == "__main__":
    image_path = "path_to_your_image.jpg"
    query = "Find the location of the object labeled 'x'"
    response = query_vision_model(image_path, query)
    if response:
        print("Model Response:", response)


