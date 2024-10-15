import sqlite3
import json

def create_table():
    """Create the object_tracking table if it doesn't exist."""
    conn = sqlite3.connect('object_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS object_tracking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        object TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def insert_record(user, obj, location):
    """Insert a new record into the object_tracking table."""
    conn = sqlite3.connect('object_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO object_tracking (user, object, location)
    VALUES (?, ?, ?)
    ''', (user, obj, location))
    conn.commit()
    conn.close()

def query_location(user, obj):
    """Query the location of an object for a specific user."""
    conn = sqlite3.connect('object_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT location FROM object_tracking
    WHERE user = ? AND object = ?
    ''', (user, obj))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_location(user, obj, new_location):
    """Update the location of an object for a specific user."""
    conn = sqlite3.connect('object_tracking.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE object_tracking
    SET location = ?
    WHERE user = ? AND object = ?
    ''', (new_location, user, obj))
    conn.commit()
    conn.close()

def view_all_records():
    """Fetch and display all records from the object_tracking table."""
    conn = sqlite3.connect('object_tracking.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM object_tracking')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No records found in the table.")


def process_packet(packet):
    try:
        data = json.loads(packet)
        
        action = data.get('action')
        user = data.get('user')
        obj = data.get('object')
        location = data.get('location', None)  
        
        if action == 'insert':
            if user and obj and location:
                insert_record(user, obj, location)
                return f"Inserted: {user}'s {obj} in {location}"
            else:
                return "Error: Missing user, object, or location for insert."
        
        elif action == 'query':
            if user and obj:
                loc = query_location(user, obj)
                if loc:
                    return f"{user}'s {obj} is located at: {loc}"
                else:
                    return f"No record found for {user}'s {obj}."
            else:
                return "Error: Missing user or object for query."
        
        elif action == 'update':
            new_location = data.get('new_location')
            if user and obj and new_location:
                update_location(user, obj, new_location)
                return f"Updated: {user}'s {obj} to new location: {new_location}"
            else:
                return "Error: Missing user, object, or new location for update."
        
        else:
            return "Error: Invalid action."
    
    except json.JSONDecodeError:
        return "Error: Failed to decode JSON."

# Main function
def main():
    # Create the table if it doesn't exist
    create_table()
    print("Waiting for a packet...")
    packet = input("Enter JSON packet: ")
    result = process_packet(packet)
    print(result)

    while True:
        print("\n=== Object Tracking System ===")
        print("1. Insert new record")
        print("2. Query object location")
        print("3. Update object location")
        print("4. View all records")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user = input("Enter user name: ")
            obj = input("Enter object name: ")
            location = input("Enter object location: ")
            insert_record(user, obj, location)
            print("Record inserted successfully!")

        elif choice == '2':
            user = input("Enter user name: ")
            obj = input("Enter object name: ")
            location = query_location(user, obj)
            if location:
                print(f"{user}'s {obj} is located at: {location}")
            else:
                print(f"No record found for {user}'s {obj}.")

        elif choice == '3':
            user = input("Enter user name: ")
            obj = input("Enter object name: ")
            new_location = input("Enter new location: ")
            update_location(user, obj, new_location)
            print("Location updated successfully!")

        elif choice == '4':
            print("Fetching all records from the database...")
            view_all_records()

        elif choice == '5':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


# {"action": "insert", "user": "Alice", "object": "Keys", "location": "table"}
# {"action": "query", "user": "Alice", "object": "Keys"}

