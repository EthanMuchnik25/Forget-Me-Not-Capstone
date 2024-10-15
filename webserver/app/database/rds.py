import boto3
import psycopg2
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import os

import atexit


load_dotenv()
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket_name = 'forget-me-not-images'

conn = psycopg2.connect(
    host=os.getenv('RDS_HOST'),
    database=os.getenv('RDS_DATABASE'),
    user=os.getenv('RDS_USER'),
    password=os.getenv('RDS_PASSWORD')
)
cur = conn.cursor()

def cleanup():
    cur.close()
    conn.close()

atexit.register(cleanup)


def upload_to_s3(image_path, rds_path):
    s3.upload_file(image_path, bucket_name, rds_path)
    return f'https://{bucket_name}.s3.amazonaws.com/{rds_path}'


# TODO this is simply here to test uploading something random... definitely 
#  delete this later, add functionality where necessary

# # Commented out as is known to work
image_path = 'static/swaglab.jpg'
rds_path = 'swaglab.jpg'
s3_url = upload_to_s3(image_path, rds_path)
# Here is s3_url: 
# https://forget-me-not-images.s3.amazonaws.com/swaglab.jpg


# user = "john doe"
# class_obj = 5
# x_coord = 5.0
# y_coord = 5.0
# output_pkt = (user, class_obj, (x_coord, y_coord), s3_url)
# user = output_pkt[0] 
# object_name = output_pkt[1]
# location = output_pkt[2]
# cur.execute("""
#     INSERT INTO tracked_objects ("user", object, location, image_url, created_at)
#     VALUES (%s, %s, %s, %s, %s);
#     """, (user, object_name, location, s3_url, datetime.now()))
# conn.commit()
# TODO I am confused by this... figure it out
# cur.close()
# conn.close()



def rds_database(output_pkt):
    user = output_pkt[0] 
    object_name = output_pkt[1]
    location = output_pkt[2]

    # TODO BAD!!!
    # Different objects from the same image will have different times!! Fix!!
    cur.execute("""
        INSERT INTO tracked_objects ("user", object, location, image_url, created_at)
        VALUES (%s, %s, %s, %s, %s);
        """, (user, object_name, location, s3_url, datetime.now()))

    conn.commit()


    cur.close()
    conn.close()




#Querying the DB 


def query_db(object, index):
    # Index will be used for this, next
    user_value = 'john_doe'  
    object_value = 'keys'    

    # Execute the query
    cur.execute(sql.SQL("""
        SELECT location, image_url 
        FROM tracked_objects 
        WHERE "user" = %s AND object = %s;
    """), (user_value, object_value))


    results = cur.fetchall()


    if results:

        for row in results:
            location, image_url = row
            print(f"Location: {location}, Image URL: {image_url}")
    else:
        print("No records found.")


    cur.close()
    conn.close()


print("querying the db")
query_db("a",1)