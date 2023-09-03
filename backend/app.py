from asyncio import wait
import random
import traceback
from flask import Flask, request, jsonify, send_file
from passlib.hash import sha256_crypt
import mysql.connector
from flask_cors import CORS, cross_origin
import io
import base64
import xml.etree.ElementTree as ET
import requests
import concurrent
from requests import get
from concurrent.futures import ThreadPoolExecutor
import json
import concurrent.futures
import subprocess
from Crypto.Cipher import AES
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from io import BytesIO
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-jaki-key" 
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"}})

# Konfiguracija baze podataka
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uiapp"
)
def get_db():
    return mysql.connector.connect(
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

@app.route('/api/countries', methods=['POST'])
@jwt_required()
def proxy_countries_request():
    try:
        # Dohvatite SOAP zahtjev iz tijela zahtjeva
        soap_request = request.data

        # Šaljite SOAP zahtjev prema vanjskoj web usluzi
        response = requests.post('http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso', data=soap_request, headers={'Content-Type': 'application/soap+xml'})

        # Parsiranje XML odgovora
        root = ET.fromstring(response.content)
        country_elements = root.findall(".//{http://www.oorsprong.org/websamples.countryinfo}tCountryCodeAndName")

        # Izdvajanje imena država
        country_names = [country.find("{http://www.oorsprong.org/websamples.countryinfo}sName").text for country in country_elements]

        # Vratite imena država kao JSON
        print (country_names)
        return jsonify(country_names)

    except Exception as e:
        print("Error:", e)
        return jsonify([])
    


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
        

       
        return jsonify({'message': 'User registered successfully', "jwt": create_access_token(identity=email), "user_details": data})
    except Exception as e:
        print("Error:", e) 
        traceback.print_exc()  # Ispis detalja greške

        return jsonify({'message': 'Error registering user'}), 500
    


def hash_password(password, salt, pepper):
    combined_password = password + salt + pepper
    #hashed_combined_password = sha256_crypt.hash(combined_password)
    return combined_password

def verify_password(combined_password, stored_password):
    return sha256_crypt.verify(combined_password, stored_password)

def process_login(email, password, ipAddress, ipMetadata, salt_string,index):
    country = ipMetadata['country']
    city = ipMetadata['city']
    timezone = ipMetadata['timezone']
    cursor= db.cursor(buffered=True)
    # Dohvaćanje korisnika iz baze prema emailu
    query = "SELECT id, password, first_name, last_name FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    print("UserData"+str(user_data))
    return_value= False
    if user_data:
        
        user_id = user_data[0]
        stored_password = user_data[1]
        first_name = user_data[2]
        last_name = user_data[3]
        pepper = generate_pepper(first_name, last_name, email)

        for char in salt_string:
            salt = char
            combined_password = password + salt + pepper
            #hashed_combined_password = hash_password(combined_password)
            print (str(index)+":"+"Password je "+password+" Sol je "+salt+" Biber je "+pepper+" hesirana je: "+combined_password)

            if verify_password(combined_password, stored_password):
                print("pogodak"+city+timezone+country+ipAddress)

                query = "INSERT INTO transaction (userid, coutry, city, ip, timezone) VALUES (%s, %s, %s, %s, %s)"
                test=cursor.execute(query, (user_id, country, city, ipAddress, timezone))
                blabla=db.commit()
                print("Test",test,blabla)
                return_value= (True,user_data)
                break


    return (index,return_value)
    
    
#Api za login
@app.route('/api/login', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])
def login_route():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    data = request.get_json()
    email = data['email']
    password = data['password']
    ipAddress = data['ipAddress']
    ipMetadata = get_ip(ipAddress)
    salts= ['abcčćdđ','efghijk','lmnopqrs','štuvwxyzž']
    results = []
    for index,salt in enumerate(salts):
        print("Salt",salt,index)
        results.append(executor.submit(process_login,email, password, ipAddress, ipMetadata, salt,index))
    executor.shutdown()
    for result in results:
        print(result.result())
    print(results)

    for x in results:
        if(x.result()[1][0]):
            return jsonify({'message': 'User logged in successfully', "jwt": create_access_token(identity=email), "user_details": x.result()[1][1]}) 
   
    return jsonify({'message': 'Error logging in user'})

   



def get_ip(ip):
    from requests import get
    meta = get("http://ip-api.com/json/"+ip).json()
    print (meta)
    return meta





@app.route('/api/tablice', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])
def run_process_b():
    data = request.get_json()
    excel_izlazna_putanja = data.get('excel_izlazna_putanja')
    pdf_direktorijum = data.get('pdf_direktorijum')
    print("TUUU SAAM")

    try:
        subprocess.run(['python', 'tablica.py', excel_izlazna_putanja, pdf_direktorijum], check=True)
        return jsonify({'message': 'Proces B je uspješno izvršen.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Greška prilikom izvršavanja Procesa B: {e}'})    
    

# Select * from users
def get_users():
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE deleted = FALSE"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

# app.route that show all users in datatable
@app.route('/api/users', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])

def get_all_users():
    users = get_users()
    user_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'country': user[4],
            # Dodajte ostale podatke o korisnicima prema potrebi
        }
        user_list.append(user_dict)
    
    return jsonify(user_list)

# app.route for showing user details by ID
@app.route('/api/userdetails/<int:id>/edit', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])

def get_user_details(id):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    user = cursor.fetchone()
    cursor.close()

    if user is not None:
        user_dict = {
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'email': user[3],
            'country': user[4],
            # Dodajte ostale podatke o korisniku prema potrebi
        }
        return jsonify(user_dict)
    else:
        return jsonify({'message': 'Korisnik s ID-om {} nije pronađen.'.format(id)}), 404
    
# app.route for updating user by ID
@app.route('/api/userupdate/<int:id>/edit', methods=['PUT'])
@cross_origin(origins='http://localhost:3000', methods=['PUT'])

def update_user(id):
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    country = data['country']

    cursor = db.cursor()
    query = "UPDATE users SET first_name = %s, last_name = %s, email = %s, country = %s WHERE id = %s"
    cursor.execute(query, (first_name, last_name, email, country, id))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Korisnik s ID-om {} je ažuriran.'.format(id)})

# app.route for deleting user by ID
@app.route('/api/userdelete/<int:id>', methods=['DELETE'])
@cross_origin(origins='http://localhost:3000', methods=['DELETE'])

def delete_user(id):
    cursor = db.cursor()
    query = "UPDATE users SET deleted = 1 WHERE id =%s"
    cursor.execute(query, (id,))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Korisnik s ID-om {} je izbrisan.'.format(id)})


"""

# Dohvati šifrirani ključ iz varijable okruženja
encrypted_key_hex = os.environ.get("ENCRYPTION_KEY")
encryption_key = base64.b64decode(encrypted_key_hex)

# Kriptiranje teksta koristeći AES
def encrypt_text(data, key):
    cipher = Cipher(algorithms.AES(key), modes.EAX(), default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return ciphertext

# Dekriptiranje kriptiranog teksta koristeći AES
def decrypt_text(data, key):
    cipher = Cipher(algorithms.AES(key), modes.EAX(), default_backend())
    encryptor = cipher.encryptor()
    ciphertext, tag = encryptor.update(data), encryptor.finalize()
    return ciphertext, tag

# Endpoint za kriptiranje PDF-a
@app.route('/api/encrypt', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])
def encrypt_pdf():
    

   def encrypt_pdf():
    # Provjerava prisutnost ključa 'pdf' u zahtjevu
    if 'pdf' not in request.files:
        return jsonify({'error': 'PDF file not found in request'}), 400

    pdf_file = request.files['pdf']

    # Provjerava je li poslana datoteka PDF formata
    if not pdf_file.content_type.startswith('application/pdf'):
        return jsonify({'error': 'Invalid PDF file'}), 400

    # Kriptira PDF datoteku
    pdf_data = pdf_file.read()
    encrypted_pdf_data = encrypt_text(pdf_data, encryption_key)

    # Vraća kriptiranu PDF datoteku
    return send_file(
        io.BytesIO(encrypted_pdf_data),
        as_attachment=True,
        download_name='encrypted.pdf',
    )


# Endpoint za dekriptiranje PDF-a
@app.route('/api/decrypt', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])

def decrypt_pdf():
    # Prima PDF datoteku iz frontend-a
    pdf_file = request.files['pdf']
    pdf_data = pdf_file.read()

    
    decrypted_pdf_data = decrypt_text(pdf_data, encryption_key)

    return send_file(io.BytesIO(decrypted_pdf_data), as_attachment=True, download_name='decrypted.pdf')

    """

if __name__ == '__main__':
    app.run(debug=True)
