from flask import Flask, render_template, request, jsonify
from config import DB_HOST, USER, PASSWORD
from controller import get_questions, get_leaderboard, random_qs,update_score,my_data,encrypt_display_question

app=Flask(__name__)

# Route for encryption and decryption

def caesar_cipher(text, shift):
        result = ""
        for i in range(len(text)):
            char = text[i]
            if char.isupper():
                result += chr((ord(char) + shift - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                result += char
        return result
    
@app.route('/', methods=['GET','POST'])
def index():
        return render_template('index.html')

# Route for the multiple choice questions

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    question, correct, wrong1, wrong2, wrong3 = random_qs(1)
    if request.method == "POST":
        user_answer = request.form.get("answer")
        # score = update_score(score, user_answer, correct)
    
    return render_template('quiz.html', question=question, correct=correct, wrong1 = wrong1, wrong2 = wrong2, wrong3 = wrong3)
    # else:
    #     return "Error fetching the question. Please try again.", 500


# Route for decryption questions

# @app.route("/solve_cipher", methods=["POST", "GET"])
# def solve_cipher():
#     if request.method == 'POST':
#         table='decrypt_questions'

#         user_answer= request.form['user_answer']
#         results=get_questions(DB_HOST,USER, PASSWORD, table)
#         question,correct,skip_key=encrypt_display_question(results)

#         if user_answer.lower() ==correct.lower():
#             return "Correct answer"
#         else:
#             return render_template('decryptquiz.html', question=question, skip_key=skip_key)

@app.route("/solve_cipher", methods=["POST", "GET"])
def solve_cipher():
    if request.method == 'POST':
        # User submits the answer
        user_answer = request.form['user_answer']
        # Retrieve the question and correct answer from the form hidden fields or session
        question = request.form['question']
        correct = request.form['correct_answer']
        skip_key = request.form['skip_key']

        if user_answer.lower() == correct.lower():
            return "Correct answer"
        else:
            return render_template('decryptquiz.html', question=question, skip_key=skip_key)
    else:
        # On GET request, fetch a new question
        results = get_questions(DB_HOST, USER, PASSWORD, DATABASE)
        question, correct, skip_key = encrypt_display_question(results)

        return render_template('decryptquiz.html', question=question, skip_key=skip_key, correct_answer=correct)



@app.route("/leaderboard")
def leaderboard():
    scores = get_leaderboard()
    return render_template("leaderboard.html", scores=scores)
    # Flask route to handle requests for generating usernames

@app.route("/leaderboard", methods=['GET', 'POST'])
def generate_username():
    if request.method == 'POST':
        scores = get_leaderboard()
        # Generate a secure random username
        username = generate_secure_username()
        # Save the generated username to the database
        save_username_to_db(username)
        # Save the generated username to the JSON file
        save_username_to_json(username)
        # Render a template to display the generated username
    return render_template("leaderboard.html", scores=scores)
        # return render_template('leaderboard.html', username=username)



    # Routes to render webpages
    
@app.route('/encryption.html', methods=['GET','POST'])
def encryption():
        if request.method == 'POST':
            text = request.form['text']
            shift = int(request.form['shift'])
            encrypted_text = caesar_cipher(text, shift)
            return render_template('Encryption.html', encrypted_text=encrypted_text)
        return render_template('Encryption.html', encrypted_text='')
    
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
        if request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            subject = request.form['subject']
            return render_template('contact.html', success=True)
        return render_template('contact.html')

@app.route('/about.html', methods=['GET','POST'])
def about():
        return render_template('about.html')


@app.route('/game.html', methods=['GET','POST'])
def game():
        return render_template('game.html')
    
@app.route('/decryptquiz')
def decryptquiz():
    return render_template('decryptquiz.html')
    
    