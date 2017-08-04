#Article BackEnd
from flask import Flask, jsonify, request
from uuid import uuid4
import pymongo
from bson.objectid import ObjectId
from authClient import AuthClient
from os import environ

rabbitmq = environ.get("RABBITMQ")
db_host = environ.get("DB_HOST")
debug = bool(environ.get("DEBUG",False))
port = int(environ.get("PORT",5000))

clientDB = pymongo.MongoClient('mongodb://{}:27017'.format(db_host))
db = clientDB["articles"]
articles = db["articles-collection"]
app = Flask(__name__)
authClient = AuthClient(host=rabbitmq)

@app.route("/search", methods=["GET"])
def listArticle():
    params = request.args
    limit = params.get(key="limit",default=5,type=int)
    owner = params.get(key="owner",default=None,type=int)
    results = []
    query = {}
    if not owner is None:
        query["owner"] = owner
    for article in articles.find(query).limit(limit).sort('views',pymongo.DESCENDING):
        results.append({
            "id":str(article["_id"]),
            "title":article["title"],
            "owner":article["owner"],
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
      views=article["views"] + 1
   )

@app.route("/articles", methods=["POST"])
def createAsrticle():
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

   if not authClient.isTokenValid(token=params["token"],userID=params["userID"]):
      return getResponse(403, message="Access Denied!!")

   newArticle = {
      "title": params["title"],
      "body": params["body"],
      "owner": params["userID"],
      "views": 0
   }
   articleID = articles.insert_one(newArticle).inserted_id

   return getResponse(
      201,
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
   if not authClient.isTokenValid(token=params["token"],userID=article["owner"]):
      return getResponse(403, message="Access Denied!!")

   articles.update({'_id': ObjectId(articleID)},{"$set":updateObj})
   return getResponse(
      200,
      get="/articles/{}".format(str(articleID)),
   )


def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp

if __name__=='__main__':
   app.run(host="0.0.0.0", debug=debug, port=port)
