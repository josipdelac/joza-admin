import json
from flask_cors import CORS, cross_origin
import pymongo
from flask import Flask, request, jsonify

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["RPA"]


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/entries/<robot_id>', methods=['GET'])
@cross_origin()
def get_entries(robot_id):
    mycol = mydb[str(robot_id)]
    x = mycol.find({})
    temp= []
    for a in x:
        print(a)
        del a["_id"]
        temp.append(a)
        
    
    
    return temp

@app.route('/last_entry/<robot_id>', methods=['GET'])
@cross_origin()
def get_last_entry(robot_id):
    mycol = mydb[str(robot_id)]
    x = mycol.find().sort([('timestamp', -1)]).limit(1)    
    print(x)
    for a in x:
        print(a)
        del a["_id"]
        return a
    return "JBG" 
    
if __name__ == '__main__':
    app.run(debug=True, port=8001)
