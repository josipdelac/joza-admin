import json
from flask_cors import CORS, cross_origin
import pymongo
from flask import Flask, request, jsonify
from aeskey import AES_HANDLER
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
    print("LASTENTRIES")
    for a in x:
       # print(a)
        print("LASTENTRIES2")

        del a["_id"]
        encrypted, tag = AES_HANDLER.encrypt(str(a).encode("utf8"))
        print("ENCRIPTANOOOOO",encrypted)
        return encrypted
    print("UKURACIJE")
    return 

@app.route('/sum_total_items/<type>', methods=['GET'])
@cross_origin()
def sum_total_items(type):
    pipeline = [
        {
            "$match": {
        "$expr": {
            "$eq": ["$current_item", "$total_items"]
        },
        "type": {"$regex": type, "$options": "i"}  
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
        result=[]
        all_collections= mydb.list_collection_names()
        for x in all_collections:
            mycol = mydb[str(x)]
            agr_result= mycol.aggregate(pipeline)
            for z in agr_result:
                print(z)
                result.append(z)
        print((result))
        result_sum= 0
        for x in result:
            result_sum+= int(x["total"])
        return str(result_sum)
        # result = list(mydb.aggregate(pipeline))
        # if result:
        #     total_sum = result[0]["total"]
        #     print(total_sum)
        #     print("nije nista")
        #     return jsonify({"sum_total_items": total_sum})
        # else:
        #     return "No matching documents found."
    except Exception as e:
        return str(e) 
    
if __name__ == '__main__':
    app.run(debug=True, port=8001)
