from flask import Flask, Response, request

import pymongo
import json
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(host="localhost",port=27017)
    db = mongo.office
    mongo.server_info()
except:
    print("ERROR -Cannot connect to database")
#####


@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        data= list(db.users.find())
        for user in data:
            user["_id"]= str(user["_id"])
        return Response(
            response= json.dumps(data),
            status=500,
            mimetype="application/json"
        )


    except Exception as ex:
        print(ex)
        return Response(
             response= json.dumps(
             {"mesaasge":"cannot read users"}),
         
             status=500,
             mimetype="application/json"
         )






@app.route("/users", methods=["POST"])
def create_user():
    try:
         user = {"name":request.form["name"],
         "lastName":request.form["lastName"]}
         dbResponse= db.users.insert_one(user)
         print(dbResponse.inserted_id)
         
        
    except Exception as ex:
        print(ex)         
        
@app.route("/users/<id>", methods=["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set":{"name":request.form["name"]}}
        )
        for attr in dir(dbResponse):
            print(f"{attr}")
            return Response(
             response= json.dumps(
             {"mesaasge":" user updated"}),
         
             status=200,
             mimetype="application/json"
         )

         


    except Exception as ex :
        print("ex")
        return Response(
             response= json.dumps(
             {"mesaasge":"cannot update user"}),
         
             status=500,
             mimetype="application/json"
         )

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        for attr in dir(dbResponse):
            print(f"{attr}")
        return Response(
             response= json.dumps(
             {"mesaasge":" user deleted","id":f"{id}"}),
         
             status=200,
             mimetype="application/json"
         )


    except Exception as ex:
        print(ex)
        return Response(
             response= json.dumps(
             {"mesaasge":"cannot delete user"}),
         
             status=500,
             mimetype="application/json"
         )    
#######
if __name__ =="__main__":
    app.run(port=80, debug=True)