import boto3
import psycopg2
from datetime import datetime


s3 = boto3.client('s3')
bucket_name = 'forget-me-not-images'


conn = psycopg2.connect(
    host='forgetmenotdb.c7ia02gs6fn4.us-east-2.rds.amazonaws.com',
    database='postgres',
    user='sanshu',
    password='********'
)
cur = conn.cursor()


def upload_to_s3(file_name):
    s3.upload_file(file_name, bucket_name, file_name)
    return f'https://{bucket_name}.s3.amazonaws.com/{file_name}'

image_path = '/Users/swatianshu/Downloads/IMG_7950.jpeg' #path to the local copy
s3_url = upload_to_s3(image_path)


user = 'john_doe'
object_name = 'keys'
location = 'living room'

cur.execute("""
    INSERT INTO tracked_objects ("user", object, location, image_url, created_at)
    VALUES (%s, %s, %s, %s, %s);
    """, (user, object_name, location, s3_url, datetime.now()))

conn.commit()


cur.close()
conn.close()