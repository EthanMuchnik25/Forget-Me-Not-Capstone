# import boto3 # aws sdk
# import os

# def lambda_handler(event: any, context: any):
#     user = event["user"]
#     visit_count: int = 0

#     #create a client 
#     dynamodb = boto3.resource("dynamodb")
#     table_name = os.environ["TABLE_NAME"]
#     table = dynamodb.Table(table_name)

#     response = table.get_item(Key={"user": user})
#     if "Item" in response: 
#         visit_count = response["Item"]["count"]

#     visit_count += 1

#     table.put_item(Item={"user": user, "count":visit_count})
    
#     message = "Hello " + user + "!" + f" visit count: {visit_count}"
#     return {"message" : message}

# if __name__ == "__main__":
#     os.environ["TABLE_NAME"] = "visit-count-table"
#     event = {"user" : "swati_local"}
#     print(lambda_handler(event, None))



import boto3
import os


def create_dynamodb_table():
    dynamodb = boto3.client('dynamodb')

    try:
        response = dynamodb.create_table(
            TableName='object-location-table',
            KeySchema=[
                {'AttributeName': 'object_name', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'object_name', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Table created successfully.")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")



# def lambda_handler(event: any, context: any):
    # object_name = event["object_name"]
    # location = event.get("location", None)  # Location is optional for query operations

    # # Create a DynamoDB client
    # dynamodb = boto3.resource("dynamodb")
    # table_name = os.environ["TABLE_NAME"]
    # table = dynamodb.Table(table_name)

    # if location:
    #     # Update or insert the object and its location
    #     table.put_item(Item={"object_name": object_name, "location": location})
    #     message = f"Updated {object_name} with location: {location}"
    # else:
    #     # Query the location based on object_name
    #     response = table.get_item(Key={"object_name": object_name})
    #     if "Item" in response:
    #         location = response["Item"]["location"]
    #         message = f"Object {object_name} is located at: {location}"
    #     else:
    #         message = f"Object {object_name} not found."

    # return {"message": message}


# def lambda_handler(event: any, context: any):
    # Extract the list of objects and their locations
    # objects = event.get("objects", [])
    
    # # Create a DynamoDB client
    # dynamodb = boto3.resource("dynamodb")
    # table_name = os.environ["TABLE_NAME"]
    # table = dynamodb.Table(table_name)
    
    # if objects:
    #     for obj in objects:
    #         object_name = obj["object_name"]
    #         location = obj["location"]
    #         # Insert or update the object and its location in the table
    #         table.put_item(Item={"object_name": object_name, "location": location})
    #     message = f"Successfully added {len(objects)} objects."
    # else:
    #     message = "No objects provided."

    

    # return {"message": message}

def lambda_handler(event: any, context: any):
    # Create a DynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    
    # Determine the action to perform
    action = event.get("action", None)
    
    if action == "add":
        # Handle adding multiple objects
        objects = event.get("objects", [])
        if objects:
            for obj in objects:
                object_name = obj["object_name"]
                location = obj["location"]
                # Insert or update each object with its location
                table.put_item(Item={"object_name": object_name, "location": location})
            message = f"Successfully added {len(objects)} objects."
        else:
            message = "No objects provided."
    
    elif action == "query":
        # Handle querying an object
        object_name = event.get("object_name", None)
        if object_name:
            # Query the location based on the object_name
            response = table.get_item(Key={"object_name": object_name})
            if "Item" in response:
                location = response["Item"]["location"]
                message = f"Object '{object_name}' is located at: {location}"
            else:
                message = f"Object '{object_name}' not found."
        else:
            message = "No object_name provided."
    
    else:

        message = "Invalid action. Use 'add' to add objects or 'query' to query an object."
    
    return {"message": message}

if __name__ == "__main__":
    os.environ["TABLE_NAME"] = "object-location-table"
    
    event_add = {
        "action": "add",
        "objects": [
            {"object_name": "Laptop", "location": "Desk"},
            {"object_name": "Phone", "location": "Table"},
            {"object_name": "Keys", "location": "Drawer"}
        ]
    }
    print(lambda_handler(event_add, None))


    event_query = {
        "action": "query",
        "object_name": "Laptop"
    }
    print(lambda_handler(event_query, None))
    

    event_invalid = {
        "object_name": "Laptop"
    }
    print(lambda_handler(event_invalid, None)) 

# if __name__ == "__main__":
#     os.environ["TABLE_NAME"] = "object-location-table"
    
#     # Example event for adding multiple objects
#     event = {
#         "objects": [
#             {"object_name": "Laptop", "location": "Desk"},
#             {"object_name": "Phone", "location": "Table"},
#             {"object_name": "Keys", "location": "Drawer"}
#         ]
#     }
#     print(lambda_handler(event, None))

# if __name__ == "__main__":
    # create_dynamodb_table()
    # os.environ["TABLE_NAME"] = "object-location-table"
    
    # # Example event for updating an object
    # event_update = {"object_name": "Laptop", "location": "Desk"}
    # print(lambda_handler(event_update, None))

    # # Example event for querying an object
    # event_query = {"object_name": "Laptop"}
    # print(lambda_handler(event_query, None))