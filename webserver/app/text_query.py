from app.config import Config
import json
import urllib.parse
from app.database.types_db import ImgObject
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from openai import OpenAI
import base64
from PIL import Image, ImageDraw, ImageFont
import mimetypes
from app.get_room_img import fs_get_room_img
from app.database.sqlite import db_get_image, db_get_all_unique_objects
from app.vectorstuffs import getMostSimilar, doRemoteInfs

import time


# import langchain

def openAIImage(path, object):
    client = OpenAI()

    #check type of path
    file_type, encoding = mimetypes.guess_type(path)
    print(f"File type: {file_type}", f"Encoding: {encoding}")


    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            a =  base64.b64encode(image_file.read()).decode('utf-8')
        

        return a

    # Path to your image
    


    image_path = path

    # Getting the base64 string
    base64_image = encode_image(image_path)

    print("the object is: ", object)
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"Can you describe near where the {object} is in this image. Do not mention the bounding box or all the background surrounding. Just mention the location of the {object} and what it is on/suspended by.",
            },
            {
            "type": "image_url",
            "image_url": {
                "url":  f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    )

    print(response.choices[0])
    return response.choices[0]



# Import database
if Config.DATABASE_VER == "RDS":
    # TODO BAD BAD BAD BAD Make good interface
    from app.database.rds import query_db
elif Config.DATABASE_VER == "SQLITE":
    from app.database.sqlite import db_query_single, db_query_range
elif Config.DATABASE_VER == "DEBUG":
    from app.database.debug_db.debug_db import db_query_single
else:
    raise NotImplementedError
def getResponseFromGPT(user, db_ret, query):
    import requests
    import shutil
    import os
    
    
    img = fs_get_room_img(user, db_ret)
    

    # convert bytesio to bytes
    img = img.read()

    
    # save data as img.jpg
    imgOutput = 'img.jpg'
    with open(imgOutput, 'wb') as file:
        file.write(img)


    # file_type = ma

    # convert the application.json to img.jpg


    responseQuery = openAIImage(imgOutput, query)
    #delete img.jpg
    os.remove(imgOutput)
    return responseQuery 

def create_img_url(db_ret):
    json_string = json.dumps(db_ret, default=ImgObject.to_dict)

    url_encoded = urllib.parse.quote(json_string)
    return f"/get_room_img?data={url_encoded}"

def handle_text_query(user, query, index=0):
    if query == 'swaglab':
        response = {
            'imgPath': f'/static/swaglab.jpg',
            'imageUrl': f'/static/swaglab.jpg',
            'success': True
        }   
        return response

    elif query == 'sign':
        response = {
            'imgPath': f'/87xuofmvnlud1.png',
            'imageUrl': 'https://i.redd.it/87xuofmvnlud1.png',
            'success': True
        }
        return response

    try:
        index = int(index)
    except ValueError as e:
        return {
            'success': False,
            'message': f"Index error: {e}"
        }
    
    if index < 0:
        return {
            'success': False,
            'message': "Negative photo index"
        }

    db_ret = db_query_single(user, query, index)
    if db_ret == None:
        return {
            'success': False,
            'message': "Object not found in database"
        }
        
    # TODO: See what other stuff is necessary in the future 
    # imgUrl = create_img_url(db_ret) 
    # response = openAIImage(imgUrl)
    return {
        'success': True,
        'imageUrl': create_img_url(db_ret),
        'imagePath': db_ret.img_url
    }


def openAIGetWord(query):
    chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

    query = query.lower()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "I need you to identify the object that is being looked for and only provide that word.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | chat
    print("query is", query)
    a = chain.invoke(
        [
            HumanMessage(
                content=query
            )
        ]
    )

    print(a.content)
    word = a.content
    
    # make word lowercase
    word = word.lower()
    print("and the word is", word)
    return word

# def findClosestWordEmbedding(word):



def handle_sentence_query(user, query, index=0, token=None):
    print("system time before sentence query")
    print("time: ", time.time()*1000)
    try:
        index = int(index)
    except ValueError as e:
        return {
            'success': False,
            'message': f"Index error: {e}"
        }
    
    if index < 0:
        return {
            'success': False,
            'message': "Negative photo index"
        }
    print("system time at sentence query")
    print("time: ", time.time()*1000)
    query = openAIGetWord(query)
    print("system time after sentence query")
    print("time: ", time.time()*1000)

    db_ret = db_query_single(user, query, index)
    vectorUsed = False
    if db_ret == None:
        print("object not found in database")
        print("user: ", user)
        getAllClasses = db_get_all_unique_objects(user)
        extractClasses = [i.object_name for i in getAllClasses]
        print("all classes: ", extractClasses)
        print("System time before getMostSimilar")
        print("time: ", time.time()*1000)
        
        # mostSimilar = getMostSimilar(query, extractClasses) 
        mostSimilar = doRemoteInfs(query, extractClasses)
        print("System time after getMostSimilar")
        print("time: ", time.time()*1000)
        print("most similar: ", mostSimilar)
        if mostSimilar == "None":
            print("System time after object not found")
            print("time: ", time.time()*1000)
            return {
                'success': False,
                'message': "Object not found in database."
            }

        else:
            vectorUsed = True
            print("most similar: ", mostSimilar)
            db_ret = db_query_single(user, mostSimilar, index)
            if db_ret == None:

                return {
                    'success': False,
                    'message': "Object not found in database but very weird"
                }
    else:
        print("object found in database")
    
    print("system time before openAI")
    print("time: ", time.time()*1000)
    response = getResponseFromGPT(user, db_ret, query)
    print("system time after openAI")
    print("time: ", time.time()*1000)
    print(response.message.content)

    response = response.message.content
    if vectorUsed:
        response = f"Object not found in database. However, the closest object to a {query} is a {mostSimilar}. {response}"
        
    # TODO: See what other stuff is necessary in the future 
    print("system time after sentence query")
    print("time: ", time.time()*1000)
    return {
        'success': True,
        'wordResponse': response,
        'imagePath': db_ret.img_url
    }    

def handle_text_range_query(user, query, low=0, high=0):
    try:
        low = int(low)
        high = int(high)
    except ValueError as e:
        return {
            'success': False,
            'message': f"Index error: {e}"
        }
    
    db_ret = db_query_range(user, query, low, high)
    if db_ret == None:
        return {
            'success': False,
            'message': "Object not found in database"
        }
    
    return {
        'success': True,
        'imageUrls': [create_img_url(line) for line in db_ret]
    }
    