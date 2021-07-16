#pip dependencies are "pip install flask" and "pip install flask-restful"

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
import pymongo
from dotenv import load_dotenv
from textblob import TextBlob
import os
import time
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import  check_password_hash
from flask import request

#aut
auth = HTTPBasicAuth()



def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
  return  TextBlob(text).sentiment.polarity

# Create two new columns 'Subjectivity' & 'Polarity

def getAnalysis(score):
    if score < 0:
      return 'Negative'
    elif score == 0:
      return 'Neutral'
    else:
      return 'Positive'


load_dotenv()
#Standard minimal Restful Api initialization of Flask library
#https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
application= app = Flask(__name__)
api = Api(app)

DATABASE_URL=f'mongodb+srv://NodeJs:{os.environ.get("password")}@sentiment.6g24c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' # get connection url from environment
#DATABASE_URL=f'mongodb+srv://NodeJs:NodeJs@sentiment.6g24c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority' # get connection url from environment
        
client=pymongo.MongoClient(DATABASE_URL) # establish connection with database
mongo_db=client.myFirstDatabase
collection=mongo_db.sentiment


# User dictionary. Stores index:key pairs for userid and sub-info.

#The main building block provided by Flask-RESTful are resources.
# Resources are built on top of Flask pluggable views, 
# giving you easy access to multiple HTTP methods just by defining methods on your resource.


class PositivityAccount(Resource):

    # GET METHOD, uses http id for looking at the userid.
    # READ's Users dict for get method.
    def get(self,accName):
       
       
        # Looks for id in the Users dict, if not found abort the program.
        
        res = collection.find_one({"acc":accName})
        print("res is ",res)
        if not res:
            abort(404,message=" Account  not found. ERROR 404")
       
        get_res={"acc":res["acc"],"score":res["score"]}
        return  (get_res,200)
   

    # POST METHOD, uses http id for looking at the userid.
    # CREATE's Users in the dict with userid.
    def post(self,accName):
    # Looks if user exists, aborts if found.
        res = collection.find_one({"acc":accName},{"tweets"})
        if res: abort(409,message=" Account  already exist.Use get request for more information Error:409")
        else:
            os.system("node Retweet.js "+accName)
            while(not res):
                # for not to send request to mongoDb constantly
                time.sleep(1)
                res = collection.find_one({"acc":accName},{"tweets"})
        
        score=0
        pos=0
        neg=0
        neutral=0
        for i in res["tweets"]:
            polarity=getPolarity(str(i))
            if polarity>0: pos+=1
            elif polarity<0: neg+=1
            else: neutral+=1
        diff=float((pos-neg))
        l=len(res["tweets"])
        score=  diff/l*100
        result={"acc":accName,"score":"%"+str(score),"pos":pos,"neg":neg,"neutral":neutral}
        collection.update_one({"acc":accName},{"$set":result})
        
        return jsonify(result)
        
    #DELETE METHOD, uses http id for looking at the userid.
    #DELETE'S Users from dict according to their id.
    @auth.login_required
    def delete(self,accName):

        # Looks for id in the Users dict, if not found abort the program.
        res=collection.delete_one({"acc":accName})
        if not res: abort(404,message="Account not found, delete request cancelled. ERROR 404")

            # Only signal code is needed for confirmation since indexed dictionary is deleted.
        return "",200
    """
    #PUT METHOD, uses http id for looking at the userid.
    #REPLACE'S  current user with diffrent user preserving the userid.
    def put(self,id):
        # Looks for id in the Users dict, if not found abort the program.
        if id not in Users:
            abort(404,message="User not found, update request cancelled. ERROR 404")
        else:
            #Deletes current user, then creates new user with parsed info.
            del Users[id]
            args=users_put_args.parse_args()
            Users[id]=args

            #return is a Python dictionary which is same as JSON.
            return Users[id]

    def patch(self,id):

        ##PATCH METHOD, uses http id for looking at the userid.
        #UPDATE'S  current user information with requested.
        if id not in Users:
            abort(404,message="User not found, update request cancelled. ERROR 404")
        else:
            args=users_put_args.parse_args()
            Users[id]=args
            return Users[id]
"""
#Routed into resource

@auth.verify_password
def verify_password(username,pasword):
    username = request.args.get('username', None)
    pasword  = request.args.get('password', None)
    check_userName=os.environ.get("super_username")
    check_userPass=os.environ.get("super_password")
    if username==check_userName:
        if check_userPass==pasword: return True
    return False
api.add_resource(PositivityAccount , "/PositivityAccount/<accName>")
@app.route('/')
def home():
    records=[]
    res = collection.find({})
    if res and len(records)==0 :
        print("in res")
        
        for  i in res:
            print("starting", i)
            records.append(
            {
            "acc":i["acc"],
            "score":i["score"]
            })
    return jsonify(records)
    
    
    
