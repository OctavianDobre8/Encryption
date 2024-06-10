from flask import Flask, request
import re

app = Flask(__name__)

def decryption(message, key_input):
    decryption_message = ""
    key_length = len(key_input)
    num_rows = len(message) // key_length
    remainder = len(message) % key_length

    # Initialize the matrix
    matrix = [["" for _ in range(key_length)] for _ in range(num_rows + (1 if remainder else 0))]

    # Populate the matrix column by column
    idx = 0
    for i in range(key_length):
        for j in range(num_rows + (1 if i < remainder else 0)):
            if idx < len(message):
                matrix[j][i] = message[idx]
                idx += 1

    print("Debug: Matrix dimensions:", len(matrix), "x", len(matrix[0]))  # Debug print

    # Sort the key and determine the column order
    sorted_key = sorted(enumerate(key_input), key=lambda x: x[1])
    col_order = [index for index, _ in sorted_key]

    # Read the matrix row by row in the order of the sorted key
    for i in range(num_rows + (1 if remainder else 0)):
        for col in col_order:
            if i < len(matrix) and col < len(matrix[i]):
                decryption_message += matrix[i][col]

    # Remove the last character
    if decryption_message:
        decryption_message = decryption_message[:-1]

    return decryption_message







@app.route('/')
def index():
    return "Server is running. This is the main branch"

@app.route('/message', methods=['PUT'])
def receive_message():
    message = request.args.get('message')
    key = request.args.get('key')
    print(f"The message before decryption is: {message}")
    decrypted_message = decryption(message, key)
    print(f"The message after decryption is: {decrypted_message}")
    return '', 200

if __name__ == "__main__":
    app.run(port=18080, threaded=True)
