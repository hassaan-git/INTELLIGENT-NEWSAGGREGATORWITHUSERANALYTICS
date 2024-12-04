

import sqlite3

# Function to check credentials
def check_credentials(name, password):
    conn = sqlite3.connect('Login.db')
    cursor = conn.cursor()
    
    # Query the database
    cursor.execute("SELECT * FROM login WHERE name = ? AND password = ?", (name, password))
    result = cursor.fetchone()

    conn.close()
    
    return result  # Return the result of the login query
