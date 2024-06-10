import re
import requests


def encryption(message, key_input):
    encryption_message = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    matrix = []
    key = []

    for index, current_char in enumerate(key_input):
        alphabet_pos = alphabet.find(current_char.lower())
        key.append((current_char, alphabet_pos, index))

    size = len(message) // len(key)
    if len(message) % len(key) != 0:
        size += 1

    for _ in range(size):
        line = []
        for _ in key:
            if message:
                line.append(message[0])
                message = message[1:]
            else:
                line.append(alphabet[0])
                alphabet = alphabet[1:]
        matrix.append(line)

    key.sort(key=lambda x: x[1])

    for _, _, col_index in key:
        for row in matrix:
            encryption_message += row[col_index]

    return encryption_message


def verify_key(key):
    pattern = re.compile("^[a-zA-Z0-9_]+$")  # Allow alphanumeric characters and underscore
    seen_characters = set()
    result = key.lower()  # Convert the key to lowercase for consistency
    print("Debug: Checking key format:", key)  # Debug print
    for character in result:
        if character in seen_characters:
            print("Debug: Duplicate character found:", character)  # Debug print
            return False
        seen_characters.add(character)

    if not pattern.match(key):
        print("Debug: Key format verification failed.")  # Debug print
        return False

    print("Debug: Key verification passed.")  # Debug print
    return True


def main():
    while True:
        key = input("Introduce the key:\n").strip().strip("'\"")  # Remove leading/trailing whitespace and quotes
        print("Debug: Entered key:", key)  # Debug print
        if verify_key(key):
            print("Debug: Key verification passed.")  # Debug print
            message = input("Introduce the message:\n")
            encrypted_message = encryption(message, key)
            response = requests.put(
                "http://localhost:18080/message",
                params={
                    "message": encrypted_message,
                    "key": key
                }
            )
            if response.status_code in (200, 201):
                print("The message was sent successfully.")
            else:
                print("There was a problem.")
        else:
            print("Introduce the key again.")
            print("Debug: Key verification failed.")  # Debug print

if __name__ == "__main__":
    main()
