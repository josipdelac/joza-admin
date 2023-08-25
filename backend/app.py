import random
import traceback
from flask import Flask, request, jsonify, send_file
from passlib.hash import sha256_crypt
import mysql.connector
from flask_cors import CORS, cross_origin
import io
import base64

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*", "methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"}})

# Konfiguracija baze podataka
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uiapp"
)

# Funkcija za generiranje "soli" na temelju slova hrvatske abecede
def generate_salt():
    hrvatska_abeceda = 'abcčćdđefghijklmnopqrsštuvwxyzž'
    return random.choice(hrvatska_abeceda)


# Funkcija za generiranje "papra" na temelju ime, prezime i emaila
def generate_pepper(first_name, last_name, email):
    email_prefix = email.split('@')[1]
    return f"{first_name.lower()}{last_name.lower()}{email_prefix}"

#Api za registraciju
@app.route('/api/register', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])


def register():
    data = request.get_json()
    print("Received data:", data)  
    try:
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        country = data['country']
        password = data['password']
        if 'profile_image' in data:
            profile_image_base64 = data['profile_image']     # Dobivanje slike iz JSON-a
            # Pretvorba base64 stringa u binarni sadržaj
            profile_image_data = base64.b64decode(profile_image_base64)
        else:
            profile_image_data:None


        # Generiranje soli i papra
        salt = generate_salt()
        pepper = generate_pepper(first_name, last_name, email)
        print (salt)
        print (pepper)

        

        # Kombiniranje soli, papra i lozinke te hasiranje
        combined_password = password + salt + pepper
        
        hashed_password = sha256_crypt.hash(combined_password)
        print ("Password je "+password+" Sol je "+salt+" Biber je "+pepper+" hesirana je: "+hashed_password)

        # Pohranjivanje u bazu
        
        cursor = db.cursor()
        query = "INSERT INTO users (first_name, last_name, email, country, password, profile_image) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (first_name, last_name, email, country, hashed_password, profile_image_data))
        db.commit()
        cursor.close()
        

       
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        print("Error:", e) 
        traceback.print_exc()  # Ispis detalja greške

        return jsonify({'message': 'Error registering user'}), 500

#Api za login
@app.route('/api/login', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])

def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Dohvaćanje korisnika iz baze prema emailu
    cursor = db.cursor()
    query = "SELECT id, password, first_name, last_name FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    

    if user_data:
        stored_password = user_data[1]
        first_name = user_data[2]
        last_name = user_data[3]
        pepper = generate_pepper(first_name, last_name, email)  # Generiraj "papar" kao kod registracije

        # Pokušaj različite soli dok se ne pronađe točna kombinacija lozinke
        for char in 'abcčćdđefghijklmnopqrsštuvwxyzž':
            salt = char
            combined_password = password + salt + pepper
            print(pepper)
            hashed_combined_password = sha256_crypt.hash(combined_password)
            print ("Password je "+password+" Sol je "+salt+" Biber je "+pepper+" hesirana je: "+hashed_combined_password)
            
            print(hashed_combined_password+"----"+stored_password)
            if sha256_crypt.verify(combined_password, stored_password):
                print("pogodak")
                return jsonify({'message': 'Login successful'})
                break
            
    else:
        return jsonify({'message': 'User not found'}), 404
    
    cursor.close()


    

if __name__ == '__main__':
    app.run(debug=True)
