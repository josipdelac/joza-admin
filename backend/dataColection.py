import json
import pymongo
from flask import Flask, request, jsonify

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["RPA"]


app = Flask(__name__)

@app.route('/entry', methods=['POST'])
def add_entry(entry):
    
    mycol = mydb[entry.id]
    myentry = { "rpy_id": entry.id, "name": entry.name, "current_item": entry.current_item,"total_items":entry.total_items, "server_id":entry.server_id, "timestamp":entry.timestamp }
    x = mycol.insert_one(myentry)
    
        
    
    record = json.loads(request.data)
    new_records = []
    with open('/tmp/data.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
    for r in records:
        if r['name'] == record['name']:
            r['email'] = record['email']
        new_records.append(r)
    with open('/tmp/data.txt', 'w') as f:
        f.write(json.dumps(new_records, indent=2))
    return jsonify(record)
    

app.run(debug=True)