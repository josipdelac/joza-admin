import json
from flask_cors import CORS, cross_origin
import pymongo
from flask import Flask, request, jsonify

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["RPA"]


app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/all_entries/', methods=['GET'])
@cross_origin()
def get_all_entries():
    all_collections= mydb.list_collection_names()
    result= []
    for collection in all_collections:
        x= mydb[collection].find({})
        for a in x:
            print(a)
            del a["_id"]
            result.append(a)
    
    return result

@app.route('/last_entries/', methods=['GET'])
@cross_origin()
def get_entries():
    all_collections= mydb.list_collection_names()
    result= []
    for collection in all_collections:
        x= mydb[collection].find({})
        temp= []
        for a in x:
          #  print(a)
            del a["_id"]
            temp.append(a)
        if(len(temp)>0):
            result.append(temp[-1])
        # elif(len(temp)):
        #     result.append(temp[0])
    
    return result

@app.route('/last_entry/<robot_id>', methods=['GET'])
@cross_origin()
def get_last_entry(robot_id):
    mycol = mydb[str(robot_id)]
    x = mycol.find().sort([('timestamp', -1)]).limit(1)    
    #print(x)
    for a in x:
       # print(a)
        del a["_id"]
        return a
    return "JBG"

@app.route('/sum_total_items/', methods=['GET'])
@cross_origin()
def sum_total_items():
    pipeline = [
        {
            "$match": {
                "current_item": {"$eq": "total_items"},
                "type": {"$regex": "pdf", "$options": "i"}
            }
        },
        {
            "$group": {
                "_id": None,
                "total": {"$sum": {"$toInt": "$total_items"}}
            }
        }
    ]
    
    try:
        result = list(mydb.aggregate(pipeline))
        if result:
            total_sum = result[0]["total"]
            print(total_sum)
            print("nije nista")
            return jsonify({"sum_total_items": total_sum})
        else:
            return "No matching documents found."
    except Exception as e:
        return str(e) 
    
if __name__ == '__main__':
    app.run(debug=True, port=8001)
