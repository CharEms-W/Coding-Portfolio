from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
import string
import secrets

from DB_User_Name import create_database, create_table
from config import USER, PASSWORD, DB_HOST

app = Flask(__name__)

# Database configuration settings
config = {
    'user': USER,  # MySQL server username
    'password': PASSWORD,  # MySQL server password
    'host': HOST,  # Host address of the MySQL server (e.g., 'localhost' or an IP address)
    'auth_plugin': 'mysql_native_password'  # Authentication plugin to be used
}

DB_NAME = 'username_secure_generator'  # Name of the database to be used

# Function to generate a secure random username
def generate_secure_username():
    characters = string.ascii_letters + string.digits  # Characters used for generating the username
    username = ''.join(secrets.choice(characters) for _ in range(12))  # Generate a username of 12 characters
    return username

# Function to insert a generated username into the database
def insert_username(cursor, username):
    add_username = "INSERT INTO usernames (username) VALUES (%s)"  # SQL query to insert the username
    data_username = (username,)  # Data to be inserted
    try:
        cursor.execute(add_username, data_username)  # Execute the SQL query
        print(f"Username '{username}' inserted successfully.")  # Confirmation message
    except mysql.connector.Error as err:
        print(f"Failed inserting username: {err}")  # Error message if insertion fails
        exit(1)  # Exit the program with an error code

# Function to save the username to the database
def save_username_to_db(username):
    conn = None  # Database connection object
    cursor = None  # Database cursor object
    try:
        conn = mysql.connector.connect(**config)  # Establish a connection to the MySQL server
        cursor = conn.cursor()  # Create a cursor object

        try:
            conn.database = DB_NAME  # Attempt to select the specified database
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # If the database does not exist, create it
                print(f"Database '{DB_NAME}' does not exist. Creating it now.")
                create_database(cursor)  # Call function to create the database
                conn.database = DB_NAME  # Select the newly created database
            else:
                print(err)  # Print any other errors encountered
                return

        create_table(cursor)  # Ensure the table exists
        insert_username(cursor, username)  # Insert the username into the table
        conn.commit()  # Commit the transaction

    except mysql.connector.Error as err:
        print(f"Error: {err}")  # Print any errors encountered
    finally:
        if conn and conn.is_connected():  # Check if the connection is open
            cursor.close()  # Close the cursor
            conn.close()  # Close the connection

# Flask route to handle requests for generating usernames
@app.route('/', methods=['GET', 'POST'])
def generate_username():
    if request.method == 'POST':
        username = generate_secure_username()  # Generate a new secure username
        save_username_to_db(username)  # Save the generated username to the database
        return jsonify({'username': username})  # Return the username in a JSON response

    return jsonify({'message': 'Submit a request to generate a username.'})  # Return a message for GET requests



if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask application with debugging enabled

# Generate and print the username
# print("Generated Username:", generate_secure_username())
##generates username- however duplicates-needs to do abit more work on this- for thursday.