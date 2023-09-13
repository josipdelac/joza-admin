from asyncio import wait
from functools import wraps
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
from flask_jwt_extended import create_access_token, get_jwt, verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
import configparser
import datetime
import secrets
import xml.etree.ElementTree as ET
from flask_basicauth import BasicAuth
from flask_httpauth import HTTPBasicAuth
from functools import wraps
from datetime import timedelta




app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "8a31f60e7c2e99b01c88d1b2873b6b6dce874483bf2b07988aa77711b1a95a88" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=50)
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
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            print("test:", claims)
            if claims["is_administrator"]:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Samo Admin!"), 403

        return decorator

    return wrapper    

        



# AES kriptiranje
# Uvoz ključa za AES iz .env datoteke
load_dotenv()
aes_key_hex = os.getenv("AES_ENCRYPTION_KEY")  
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
        #  SOAP zahtjev iz tijela zahtjeva
        soap_request = request.data

        #  SOAP zahtjev prema vanjskoj web usluzi
        response = requests.post('http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso', data=soap_request, headers={'Content-Type': 'application/soap+xml'})

        # Parsiranje XML odgovora
        root = ET.fromstring(response.content)
        country_elements = root.findall(".//{http://www.oorsprong.org/websamples.countryinfo}tCountryCodeAndName")

        # Izdvajanje imena država
        country_names = [country.find("{http://www.oorsprong.org/websamples.countryinfo}sName").text for country in country_elements]

        # imena država kao JSON
        print (country_names)
        return jsonify(country_names)

    except Exception as e:
        print("Error:", e)
        return jsonify([])
    
xml_file = "users.xml"

if not os.path.exists(xml_file):
    
    root = ET.Element("users")
else:
    
    tree = ET.parse(xml_file)
    root = tree.getroot()

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
            profile_image_base64 = data['profile_image']     
           
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
        user_id
       

        
        user_id = str(len(root) + 1)  
        user = ET.SubElement(root, "user")

        ET.SubElement(user, "id").text = user_id  
        ET.SubElement(user, "first_name").text =first_name
        ET.SubElement(user, "last_name").text = last_name
        ET.SubElement(user, "email").text = email
        ET.SubElement(user, "country").text = country

        tree = ET.ElementTree(root)
        tree.write(xml_file)
    
       
        return jsonify({'message': 'User registered successfully', "jwt": create_access_token(identity=email), "user_details": data})
    except Exception as e:
        print("Error:", e) 
        traceback.print_exc()  

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
        type = user_data[8]
        
       
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
                return_value= (True,{"first_name":first_name,"last_name":last_name,"email":email, "admin": type== 'admin'})
                break

    # cursor.reset()
    return (index,return_value)
    
    
#Api za login
@app.route('/api/login', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])
#@jwt_required()
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
    # for result in results:
    #     print(result.result())  
    # print(results)

    for x in results:
        if(x.result()[1][0]):
            return jsonify({'message': 'User logged in successfully', "jwt": create_access_token(identity=email,fresh=True,expires_delta=timedelta(days=50), additional_claims={"is_administrator": x.result()[1][1]["admin"]} ), "user_details": x.result()[1][1]}) 
   
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

    # Dekriptiranje 
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
@admin_required()
def run_process_b():
    data = request.get_json()
    claims = get_jwt()
    print("test:", claims)
    if not claims["is_administrator"]:
        return jsonify(msg="Samo Admin!"), 403

    excel_izlazna_putanja = data.get('excel_izlazna_putanja')
    pdf_direktorijum = data.get('pdf_direktorijum')
    print("TUUU SAAM")

    try:
        subprocess.run(['python', 'tablica.py', excel_izlazna_putanja, pdf_direktorijum], check=True)
        return jsonify({'message': 'Sve informacije su uspješno upisane u tablicu.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': f'Greška prilikom obrade podataka: {e}'})    
    

# Select * from users
def get_users():
    cursor = db.cursor()
    query = "SELECT u.*, o.* FROM users u JOIN user_organisation uo ON u.id = uo.user_id JOIN organization o ON uo.organisation_id = o.id WHERE u.deleted=0 ORDER BY u.id;" 
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

# app.route that show all users in datatable
@app.route('/api/users', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])
@admin_required()

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
            'type': user[8],
            'department': user[12],
            'sector': user[13],
           
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
            'type': user[8],
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
    type = data['type']

    cursor = db.cursor()
    query = "UPDATE users SET first_name = %s, last_name = %s, email = %s, country = %s, type = %s WHERE id = %s"
    cursor.execute(query, (first_name, last_name, email, country, type, id))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Korisnik s ID-om {} je ažuriran.'.format(id)})

logs = []

# app.route for deleting user by ID
@app.route('/api/userdelete/<int:id>', methods=['DELETE'])
@cross_origin(origins='http://localhost:3000', methods=['DELETE'])

def delete_user(id):
    cursor = db.cursor()
    query = "UPDATE users SET deleted = 1 WHERE id =%s"
    cursor.execute(query, (id,))
    
   
    db.commit()
    cursor.close()
    log_entry = {
        'user_id': id,
        'action': 'delete',
        'timestamp': str(timestamp),
        'deleted_by': 'ime_korisnika'
    }

    
    logs.append(log_entry)

    
    with open('delete_log.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)  

    return jsonify({'message': 'Korisnik s ID-om {} je izbrisan.'.format(id)})

# Funkcija za čitanje korisnika iz XML datoteke
def read_users(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        users = []

        for user_element in root:
            user_data = {}
            for data_element in user_element:
                user_data[data_element.tag] = data_element.text
            users.append(user_data)

        return users

    except Exception as e:
        print("Error reading users:", str(e))
        return jsonify(error="Error reading users"), 500  


@app.route('/api/xmlusers', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])
def get_users1():
    users = read_users(xml_file)
    return jsonify(users)

@app.route('/api/xmlusers', methods=['POST'])
@cross_origin(origins='http://localhost:3000', methods=['POST'])

def create_user():
    user_data = request.get_json()
    create_user(xml_file, user_data)
    return "User created", 201


@app.route('/api/xmlusers/update/<int:user_id>', methods=['PUT'])
@cross_origin(origins='http://localhost:3000', methods=['PUT'])
def update_users(user_id):
    updated_data = request.get_json()
    
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print("user_id", user_id)
        user_found = False  

        


        for user_element in root:
            print("user_element", user_element.find('id').text)
            if user_element.find('id').text == str(user_id):
                
                user_element.find('email').text = updated_data['email']
                tree.write(xml_file)  
                user_found = True
                break
        if user_found:
            return "User updated", 200
        else:
            return jsonify(error="User not found"), 404
        
        

       

    except Exception as e:
        print("Error updating user:", str(e))
        return jsonify(error="Error updating user"), 500
@app.route('/api/xmlusers/delete/<int:user_id>', methods=['DELETE'])

def delete_users(user_id):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for user_element in root:
          
            if user_element.find('id').text == str(user_id):
                root.remove(user_element)
                tree.write(xml_file) 
                return "User deleted", 200

        return jsonify(error="User not found"), 404

    except Exception as e:
        print("Error deleting user:", str(e))
        return jsonify(error="Error deleting user"), 500  


def get_allrobots():
    cursor = db.cursor()
    query = "SELECT robots.*, organization.sector AS organization_name FROM robots JOIN organization ON robots.organization_id = organization.id WHERE robots.deleted = FALSE;"
    cursor.execute(query)
    robots = cursor.fetchall()
    cursor.close()
    return robots

# app.route that show all robots in datatable
@app.route('/api/robots', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])

def get_all_robots():
  
    robots = get_allrobots()
    
    robot_list = []
    for robot in robots:
        robot_dict = {
            'robot_name': robot[1],
            'robot_status': robot[2],
            'developby': robot[4],
            'organization_name': robot[6]
        }
        
        robot_list.append(robot_dict)
    
    return jsonify(robot_list)   

@app.route('/api/robotdetails/<int:id>/edit', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])

def get_robot_details(id):
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
        }
        return jsonify(user_dict)
    else:
        return jsonify({'message': 'Korisnik s ID-om {} nije pronađen.'.format(id)}), 404
    
# app.route for updating robot by ID
@app.route('/api/robotupdate/<int:id>/edit', methods=['PUT'])
@cross_origin(origins='http://localhost:3000', methods=['PUT'])

def update_robot(id):
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

logs = []

# app.route for deleting user by ID
@app.route('/api/robotdelete/<int:id>', methods=['DELETE'])
@cross_origin(origins='http://localhost:3000', methods=['DELETE'])
#@jwt_required()

def delete_robot(id):
    cursor = db.cursor()
    query = "UPDATE robots SET deleted = 1 WHERE id =%s"
    cursor.execute(query, (id,))
     
   
    db.commit()
    cursor.close()
    log_entry = {
        'robot_id': id,
        'action': 'delete',
        'timestamp': str(timestamp),
        'deleted_by': 'ime_korisnika'  
    }

    
    logs.append(log_entry)

    
    with open('delete_log.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)  

    return jsonify({'message': 'Korisnik s ID-om {} je izbrisan.'.format(id)})

############################################################################################JSON
# Čitanje svih logova iz JSON datoteke
def read_logs():
    try:
        with open('delete_log.json', 'r') as log_file:
            logs = json.load(log_file)
    except FileNotFoundError:
        logs = []
    return logs


def edit_log(log_id, updated_data):
    logs = read_logs()
    for log in logs:
        if log['user_id'] == log_id:
            log.update(updated_data)
            with open('delete_log.json', 'w') as log_file:
                json.dump(logs, log_file, indent=4)
            return


def delete_log(log_id):
    logs = read_logs()
    logs = [log for log in logs if log['user_id'] != log_id]
    with open('delete_log.json', 'w') as log_file:
        json.dump(logs, log_file, indent=4)


@app.route('/api/logs', methods=['GET'])
@cross_origin(origins='http://localhost:3000', methods=['GET'])
def get_logs():
    logs = read_logs()
    return jsonify(logs)


@app.route('/api/logs/<int:log_id>', methods=['PUT'])
@cross_origin(origins='http://localhost:3000', methods=['PUT'])
def update_log(log_id):
    updated_data = request.get_json()
    edit_log(log_id, updated_data)
    return "Log updated", 200


@app.route('/api/logs/delete/<int:log_id>', methods=['DELETE'])
@cross_origin(origins='http://localhost:3000', methods=['DELETE'])
def delete_log_by_id(log_id):
    delete_log(log_id)
    return "Log deleted", 200

if __name__ == '__main__':
    app.run(debug=config.getboolean("app","debug"), port=config.getint("app",option="port"))
