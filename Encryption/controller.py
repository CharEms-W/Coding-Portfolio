from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import errorcode
import string
import secrets
import json
import os

from config import DB_HOST, PASSWORD, USER


def get_questions(DB_HOST,USER,PASSWORD,table):
    """Function to connect to the MySQL database and retrieve the information from the question set.
    this function needs to be moved to new home so not mixed up with all the flask app"""
    global data, data2
    data=[]

    #connection to mysql database
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database="quizz_db"
        )

        mycursor = mydb.cursor()
        query = f"SELECT * FROM {table}" #all the information is valid so just select *
        mycursor.execute(query)
        rows = mycursor.fetchall()

        for row in rows:
            data.append(row)
        mycursor.close()
        mydb.close()

    except mysql.connector.Error as error:
        print(f"Error reading from database: {error}")

    return data

def random_qs(difficulty):
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database='quizz_db'
        )
# Query to pull random questions
        mycursor = mydb.cursor()
        # How many questions will be returned to user?
        query = """
            SELECT question
            FROM QuestionsCipher
            WHERE difficulty = %s
            ORDER BY RAND()
            LIMIT 1
        """
        mycursor.execute(query, (difficulty,))
        randomised_qs = mycursor.fetchone()
        
# Stores pull random question in variable
        question = randomised_qs[0]
    
# Query to pull correct answer to the randomly pulled question
        fetch_correct = f"""
            SELECT correct
            FROM QuestionsCipher
            WHERE question = %s
        """
        mycursor.execute(fetch_correct, (question,))
        correct = mycursor.fetchone()
        
# Storing correct answer
        correct = correct[0]
        
# Query to pull wrong answer to the randomly pulled questions
        fetch_wrong = """
            SELECT wrong1, wrong2, wrong3
            FROM QuestionsCipher
            WHERE question = %s
        """
        
        mycursor.execute(fetch_wrong, (question,))
        wrong_answer = mycursor.fetchall()
        
        wrongans = wrong_answer[0]
        wrong1 = wrongans[0]
        wrong2 = wrongans[1]
        wrong3 = wrongans[2]
        
        mycursor.close()
        mydb.close()
        
# DB connection error message
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None
    print(question, correct, wrong1, wrong2, wrong3)

    return question, correct, wrong1, wrong2, wrong3
# TESTING DECRYPT RANDOM

def get_questions(DB_HOST, user, password, database):
    conn = mysql.connector.connect(DB_HOST=host, user=user, password=password, database=database)
    cursor = conn.cursor(dictionary=True)
    
    # Fetch a random question from the table
    cursor.execute("SELECT * FROM decrypt_questions ORDER BY RAND() LIMIT 1")
    result = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return result

def encrypt_display_question(results):
    question = result['question']
    correct = result['correct_answer']
    skip_key = result['skip_key'] 
    
    return question, correct,skip_key

    # question1 = results[0]  # access first () in the list
    # id = question1[0]
    # question = question1[1]
    # correct = question1[2]
    # skip_key = question1[3]
    # difficulty = question1[4]

    # return question,correct,skip_key


def update_score(current_score, user_answer, correct_answer):
    if user_answer == correct_answer:
        current_score += 1
    return current_score

#Insert username and score into leaderboard
def save_score(username, score):
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database="quizz_db"
        )
        mycursor = mydb.cursor()
        query = "INSERT INTO Leaderboard (username, score) VALUES (%s, %s)"
        mycursor.execute(query, (username, score))
        mydb.commit()

        mycursor.close()
        mydb.close()

    except mysql.connector.Error as error:
        print(f"Error saving score to database: {error}")

# Function to retrieve top 10 scores from leaderboard
def get_leaderboard():
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database="quizz_db"
        )
        mycursor = mydb.cursor()
        query = "SELECT username, score FROM Leaderboard ORDER BY score DESC LIMIT 10"
        mycursor.execute(query)
        leaderboard = mycursor.fetchall()

        mycursor.close()
        mydb.close()
        return leaderboard

    except mysql.connector.Error as error:
        print(f"Error retrieving leaderboard from database: {error}")
        return []


my_data = "That is the correct answer"
not_correct="Sorry that answer is wrong"
random_qs(1)

# Function to create the database if it doesn't exist
def create_database(cursor):
    try:
        # SQL query to create a new database with UTF-8 character encoding
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"Database '{DB_NAME}' created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

# Function to create the leaderboard table if it doesn't exist
def create_table(cursor):
    # SQL query to create the leaderboard table with columns for username, and score
    table_description = """
    CREATE TABLE IF NOT EXISTS leaderboard (
        username VARCHAR(80) UNIQUE NOT NULL PRIMARY KEY,
        score INT NOT NULL DEFAULT 0
    ) ENGINE=InnoDB
    """
    try:
        print("Creating table 'leaderboard': ", end='')
        cursor.execute(table_description)
        print("OK")
    except mysql.connector.Error as err:
        print(f"Failed creating table: {err}")
        exit(1)
## MAY NOT NEED THE ABOVE ##

# Function to insert a generated username into the leaderboard table
def insert_username(cursor, username):
    # SQL query to insert a new username into the leaderboard table
    add_username = "INSERT INTO leaderboard (username) VALUES (%s)"
    data_username = (username,)
    try:
        cursor.execute(add_username, data_username)
        print(f"Username '{username}' inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed inserting username: {err}")
        exit(1)

# Function to save the username to the database
def save_username_to_db(username):
    conn = None
    cursor = None
    try:
        # Establish a connection to the MySQL server using config 
        conn = mysql.connector.connect(
            user=config['user'],
            password=config['password'],
            host=config['host'],
            auth_plugin=config['auth_plugin']
        )
        cursor = conn.cursor()

        # Attempt to connect to the specified database
        try:
            conn.database = DB_NAME
        except mysql.connector.Error as err:
            # If the database does not exist, create it
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Database '{DB_NAME}' does not exist. Creating it now.")
                create_database(cursor)
                conn.database = DB_NAME
            else:
                print(err)
                return

        # # Create the leaderboard table if it doesn't exist
        # create_table(cursor)
        # Insert the username into the leaderboard table
        insert_username(cursor, username)
        # Commit the transaction to save the changes
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            # Close the cursor and connection
            cursor.close()
            conn.close()

# Function to save the username to a JSON file
def save_username_to_json(username):
    file_path = 'data.json'
    data = []

    # If the JSON file exists, read its contents
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # Handle case where the JSON file is empty or contains invalid JSON
                pass

    # Append the new username to the list
    data.append({"username": username})

    # Write the updated list back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"Username '{username}' saved to data.json successfully.")


# Function to generate a secure random username
def generate_secure_username():
    characters = string.ascii_letters + string.digits
    # Generate a 12-character random string using letters and digits
    return ''.join(secrets.choice(characters) for _ in range(12))