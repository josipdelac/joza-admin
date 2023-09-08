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
from dotenv import load_dotenv
import configparser
import datetime
import secrets




app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-jaki-key" 
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*", "methods": "GET,PUT,POST,DELETE,PATCH,OPTIONS"}})
# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

config= configparser.ConfigParser()
config.read("app.ini")
config.set("app", "last_run",timestamp)
config.write(open("app.ini", "w"))

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
    


# AES kriptiranje
# Uvoz ključa za AES iz .env datoteke
load_dotenv()
aes_key_hex = os.getenv("AES_ENCRYPTION_KEY")  # Prilagodite kako odgovara vašoj konfiguraciji
aes_key = bytes.fromhex(aes_key_hex)
print(aes_key)
# Generiranje slučajnog inicijalizacijskog vektora (IV)
iv = os.urandom(16)  # 16 bajtova IV
print(iv)
# Inicijalizacija AES kriptera
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

# Funkcija za generiranje "soli" na temelju slova hrvatske abecede
def generate_salt():
    hrvatska_abeceda = 'abcčćdđefghijklmnopqrsštuvwxyzž'
    return random.choice(hrvatska_abeceda)


# Funkcija za generiranje "papra" na temelju ime, prezime i emaila
def generate_pepper(first_name, last_name, email):
    email_prefix = email.split('@')[1]
    return f"{first_name.lower()}{last_name.lower()}{email_prefix}"

@app.route('/api/countries', methods=['POST'])

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
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    #print("UserData"+str(user_data))
    return_value= (False,None)
    if user_data:
        
        user_id = user_data[0]
        stored_password = user_data[5]
        first_name = user_data[1]
        last_name = user_data[2]
        email = user_data[3]
        encrypted_email = user_data[8]
        email_iv = user_data[9]
       
       # picture =str(io.BytesIO(user_data[6]), mimetype='image/jpeg')

        
        
        pepper = generate_pepper(first_name, last_name, email)

        for char in salt_string:
            salt = char
            combined_password = password + salt + pepper
            #hashed_combined_password = hash_password(combined_password)
            print (str(index)+":"+"Password je "+password+" Sol je "+salt+" Biber je "+pepper+" hesirana je: "+combined_password)

            if verify_password(combined_password, stored_password):
                print("pogodak"+city+timezone+country+ipAddress)
                
                ipAddress_bytes =ipAddress.encode('utf-8')
                while len(ipAddress_bytes) % 16 != 0:
                    ipAddress_bytes += b' '  # Dopuniti sa praznim bajtovima ako je potrebno
                encrypted_ipAddress = cipher.encrypt(ipAddress_bytes)

                query = "INSERT INTO transaction (userid, coutry, city, ip, iv, timezone) VALUES (%s, %s, %s, %s, %s, %s)"
                test=cursor.execute(query, (user_id, country, city, encrypted_ipAddress, iv, timezone))
                blabla=db.commit()
                print("Test",test,blabla)
                return_value= (True,{"first_name":first_name,"last_name":last_name,"email":email})
                break

    # cursor.reset()
    return (index,return_value)
    
    
#Api za login
@app.route('/api/login', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])
#@jwt_required()
def login_route():
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
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
    # for result in results:
    #     print(result.result())  
    # print(results)

    for x in results:
        if(x.result()[1][0]):
            return jsonify({'message': 'User logged in successfully', "jwt": create_access_token(identity=email,expires_delta=False ), "user_details": x.result()[1][1]}) 
   
    return jsonify({'message': 'Error logging in user'})

@app.route('/api/get_user', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])
@jwt_required()
def get_user():
    print(request.headers)
    print("prije ulaska u upit")
   # user_pub= request.json["user_pub"]
    email=get_jwt_identity()
    print(email)
    query = "SELECT * FROM users INNER JOIN transaction ON users.id = transaction.userid WHERE users.email = %s ORDER BY transaction.timestamp DESC LIMIT 1"
    cursor = db.cursor()
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    
     # Inicijalizacija AES kriptera za dekripciju
    decryptor = AES.new(aes_key, AES.MODE_CBC, iv=user_data[16])

    # Dekriptiranje kriptiranog emaila
    decrypted_ip_bytes = decryptor.decrypt(user_data[15])	

   
   
    decrypted_ip = decrypted_ip_bytes.rstrip(b' ').decode('utf-8')
    print(decrypted_ip)
   
   
    
    first_name = user_data[1]
    last_name = user_data[2]
    email = user_data[3]
    
    type = user_data[7]
    ipAddress = decrypted_ip
    
   
    
    
    
    
    
    return jsonify({'userdata': {"first_name":first_name,"last_name":last_name,"email":email, "type":type, "ipAddress":ipAddress}})
    # return {}

   



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


   

if __name__ == '__main__':
    app.run(debug=config.getboolean("app","debug"), port=config.getint("app",option="port"))
