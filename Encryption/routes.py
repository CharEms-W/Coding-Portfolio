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