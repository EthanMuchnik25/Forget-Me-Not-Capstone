import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(
    host='forgetmenotdb.c7ia02gs6fn4.us-east-2.rds.amazonaws.com',
    database='postgres',
    user='sanshu',
    password='*******'
)


cur = conn.cursor()


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