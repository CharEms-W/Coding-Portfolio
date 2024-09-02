    from flask import Flask, request, jsonify

app = Flask(__name__)

def caesar_cipher(text, shift):
    result = ""

    for i in range(len(text)):
        char = text[i]

        # Encrypt uppercase characters
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        # Encrypt lowercase characters
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char

    return result

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    text = data.get('text')
    shift = int(data.get('shift'))
    encrypted_text = caesar_cipher(text, shift)
    return jsonify({'result_text': encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    text = data.get('text')
    shift = int(data.get('shift'))
    decrypted_text = caesar_cipher(text, -shift)  # Decrypt by reversing the shift
    return jsonify({'result_text': decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)

    # Test the cipher functions before running the server
    text = "Well I guess this one was not difficult enough!"
    shift = -8

    encrypted_text = caesar_cipher(text, shift)
    print("Encrypted:", encrypted_text)

    # Note: Shift should be passed as positive for decryption function
    decrypted_text = caesar_cipher(encrypted_text, -shift)
    print("Decrypted:", decrypted_text)

