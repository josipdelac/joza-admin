from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Povezivanje s MySQL bazom podataka
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Vaš korisničko ime
    password="",  # Vaša lozinka
    database="smartdoc"
)

cursor = db.cursor()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    print("Dogodilo se nes", str(request))
    query = "SELECT username, password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(debug=True)
