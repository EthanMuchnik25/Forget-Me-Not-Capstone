import boto3
import psycopg2
from psycopg2 import sql
from datetime import datetime
from dataclasses import dataclass
from typing import Tuple
from app.database.types_db import ImgObject, ImgObjectQuery
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
    database=os.getenv('db_write_line'),
    user=os.getenv('RDS_USER'),
    password=os.getenv('RDS_PASSWORD')
)
cur = conn.cursor()


def cleanup():
    cur.close()
    conn.close()

atexit.register(cleanup)


image_path = 'static/swaglab.jpg'
rds_path = 'swaglab.jpg'

# TODO : remove after verifying 
def upload_to_s3(image_path, rds_path):
    """Create path to upload an image object photo to S3"""
    s3.upload_file(image_path, bucket_name, rds_path)
    return f'https://{bucket_name}.s3.amazonaws.com/{rds_path}'


def db_write_line(output_pkt):
    try:
        user = output_pkt.user
        object_name = output_pkt.object_name 
        #TODO: confirm (x + width/2) and update this
        location = (output_pkt.p1, output_pkt.p2)
        # s3_url = upload_to_s3(image_path, rds_path)
        s3_url = db_save_image(image_path, rds_path)
        created_at = output_pkt.created_at 

        cur.execute("""
            INSERT INTO tracked_objects ("user", object, location, image_url, created_at)
            VALUES (%s, %s, %s, %s, %s);
            """, (user, object_name, location, s3_url, created_at))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")


def db_query_single(object_name, index):
    """Get the output coordinates and s3 file link"""
    # TODO: need to add index functionality  
    try:
        cur.execute(sql.SQL("""
            SELECT location, image_url 
            FROM tracked_objects 
            WHERE "user" = %s AND object = %s;
        """), (object_name, ))

        results = cur.fetchall()
        if results:
            for row in results:
                location, image_url = row
                print(f"Location: {location}, Image URL: {image_url}")
        else:
            print("No records found.")
    except Exception as e:
        print(f"An error occurred while querying: {e}")


def db_save_image(f, name):
    """Save an image object photo to S3"""
    try:
        # Upload the image to S3 using the provided file and name
        s3.upload_fileobj(f, bucket_name, name)
        return f'https://{bucket_name}.s3.amazonaws.com/{name}'
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        return None


###########################  Unit Testing  ####################################
# print("Updating the db")
# user = "jane doe"
# class_obj = 5
# x_coord = 7.0
# y_coord = 7.0

# output_pkt = ImgObject(user, str(class_obj), x_coord, y_coord, image_path, datetime.now())
# db_write_line(output_pkt)

# print("Now, querying the db")
# user_name = 'jane doe'
# object_name = '5'
# input_pkt = ImgObjectQuery(user_name, object_name)
# db_query_single(input_pkt,1)
##############################################################################