#Article BackEnd
from flask import Flask, jsonify, request
from uuid import uuid4
import pymongo
from bson.objectid import ObjectId
from os import environ
import requests

users_host = environ.get("USERS_HOST")
db_host = environ.get("DB_HOST")
debug = bool(environ.get("DEBUG",False))
port = int(environ.get("PORT",5000))

clientDB = pymongo.MongoClient('mongodb://{}:27017'.format(db_host))
db = clientDB["articles"]
articles = db["articles-collection"]
app = Flask(__name__)

@app.route("/articles", methods=["GET"])
def listArticles():
    params = request.args
    limit = params.get(key="limit",default=10,type=int)
    ownerID = params.get(key="ownerID",default=None,type=int)
    query = {}
    if not ownerID is None:
        query["ownerID"] = ownerID 
    cursor = articles.find(query).limit(limit).sort('views',pymongo.DESCENDING)

    results = []
    cursor.rewind()
    for article in cursor:
        results.append({
            "id":str(article["_id"]),
            "title":article["title"],
            "owner":article["owner"],
            "ownerID":article["ownerID"],
            "views":article["views"]
        })
    resp = jsonify(results)
    resp.status_code = 200
    return resp

@app.route("/articles/<articleID>")
def getArticle(articleID):
    article = articles.find_one({'_id': ObjectId(articleID)})
    if article is None:
        return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
    articles.update({'_id': ObjectId(articleID)},{"$inc":{"views":1}})
    return getResponse(
        200,
        title=article["title"],
        body=article["body"],
        owner=article["owner"],
        ownerID=article["ownerID"],
        views=article["views"] + 1
    )

@app.route("/articles", methods=["POST"])
def createArticle():
    params = request.get_json()
    if params is None:
        return getResponse(400,message="Request body must be json type")
    errFlag = False
    errMsg = ""
    if not "title" in params:
        errFlag = True
        errMsg += "Missing field title"
    if not "body" in params:
        errFlag = True
        errMsg += "Missing field body"
    if not "userID" in params:
        errFlag = True
        errMsg += "Missing userID field"
    if not "token" in params:
        errFlag = True
        errMsg += "Missing token field"
    if errFlag:
        return getResponse(400, message=errMsg)

    if not isValidToken(token=params["token"],userID=params["userID"]):
        return getResponse(403, message="Access Denied!!")

    r = requests.get(
        "http://{}/users/{}".format(users_host,params["userID"])
    )
    if r.status_code != 200:
        return getResponse(503, message="Users service not unvailable")

    newArticle = {
        "title": params["title"],
        "body": params["body"],
        "ownerID": params["userID"],
        "owner": r.json()["username"],
        "views": 0
    }
    articleID = articles.insert_one(newArticle).inserted_id

    return getResponse(
        201,
        id=str(articleID),
        get="/articles/{}".format(str(articleID)),
    )

@app.route("/articles/<articleID>", methods=["PUT"])
def updateArticle(articleID):
   params = request.get_json()
   if params is None:
      return getResponse(400,message="Request body must be json type")
   updateObj = {}
   if "body" in params:
      updateObj["body"] = params["body"]
   if "title" in params:
      updateObj["title"] = params["title"]
   if not "token" in params:
      return getResponse(400, message="Missing token!")

   article = articles.find_one({'_id': ObjectId(articleID)})
   if article is None:
      return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
   if not isValidToken(token=params["token"],userID=article["ownerID"]):
      return getResponse(403, message="Access Denied!!")

   articles.update({'_id': ObjectId(articleID)},{"$set":updateObj})
   return getResponse(
      200,
      get="/articles/{}".format(str(articleID)),
   )

def isValidToken(userID, token):
    url = "http://{}/users/{}/isValidToken".format(users_host,userID)
    r = requests.post(url, json = {'token':token})
    if r.status_code != 200:
        return False
    return r.json()["isValid"]

def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp

if __name__=='__main__':
   app.run(host="0.0.0.0", debug=debug, port=port)
