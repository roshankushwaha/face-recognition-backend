import sqlite3
from app.utils.hashing import hash_password

DB_PATH = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create table if it doesn't exist
def create_users_table():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                contact TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                face_embedding TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("Table created (if not already present)")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        raise Exception("Database Error: " + str(e))

def insert_user(name: str, contact: str, email: str, password: str, embedding: list):
    try:
        # Hash the password before storing it
        hashed_password = hash_password(password)

        # Open connection to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert user data into the database
        cursor.execute('''
            INSERT INTO users (name, contact, email, password_hash, face_embedding)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, contact, email, hashed_password, str(embedding)))

        # Now fetch the inserted user data
        user_id = cursor.lastrowid  # get the inserted user's ID
        cursor.execute("SELECT id, name, contact, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return {
            "id": user[0],
            "name": user[1],
            "contact": user[2],
            "email": user[3]
        }
        
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
        raise Exception("Database Error: " + str(e))

def get_user_by_email(email:str):
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        print("🐼",user);
        return dict(user) if user else None
    except sqlite3.Error as e:
        print("DB Error:", e)
        print("😒Error", e)
        return None
    
def get_user_by_email_send(email:str):
    try:
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT name, contact, email FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        print("🐼",user);
        return dict(user) if user else None
    except sqlite3.Error as e:
        print("DB Error:", e)
        print("😒Error", e)
        return None