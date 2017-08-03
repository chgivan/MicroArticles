#Article BackEnd
from flask import Flask, jsonify, request
from uuid import uuid4
from pymongo import MongoClient
from bson.objectid import ObjectId
from authClient import AuthClient

clientDB = MongoClient('mongodb://192.168.99.100:27017')
db = clientDB["articles"]
articles = db["articles-collection"]
app = Flask(__name__)
authClient = AuthClient(host="192.168.99.100")

@app.route("/articles/<articleID>")
def getArticle(articleID):
   article = articles.find_one({'_id': ObjectId(articleID)})
   if article is None:
      return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
   return getResponse(
      200,
      title=article["title"],
      body=article["body"],
      owner=article["owner"]
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
      "owner": params["userID"]
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
   app.run(debug=True, port=5000)
