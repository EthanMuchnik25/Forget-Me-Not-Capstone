import json 
import random

def random_drink():
    drinks = [" coffee", "tea", "beer", "wine", "water", "juice"]
    return random.choice(drinks)


def lambda_handler(event, context):
    drink = random_drink()
    message = f"You should drink some {drink}"
    return {
        'statusCode': 200,
        'body': json.dumps({"message": message, "drink": drink})
    }