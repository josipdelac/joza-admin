import json
import pymongo
from flask import Flask, request, jsonify

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["RPA"]


app = Flask(__name__)

@app.route('/entry', methods=['POST'])
def add_entry():
    entry = request.json
    print(entry)
    mycol = mydb[str(entry["id"])]
    myentry = { "rpy_id": entry["id"], "name": entry["name"], "current_item": entry["current_item"],"total_items":entry["total_items"], "server_id":entry["server_id"], "timestamp":entry["timestamp"] }
    x = mycol.insert_one(myentry)
        
    
    
    return str(x.inserted_id)

@app.route('/entries/<robot_id>', methods=['GET'])
def get_entries(robot_id):
    mycol = mydb[str(robot_id)]
    x = mycol.find({})
    temp= []
    for a in x:
        print(a)
        del a["_id"]
        temp.append(a)
        
    
    
    return temp
    

app.run(debug=True)