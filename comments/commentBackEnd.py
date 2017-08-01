#Comments BackEnd
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

clientDB = MongoClient('mongodb://192.168.99.100:27017')
db = clientDB["comments"]
comments = db["comments-collection"]
app = Flask(__name__)

@app.route("/articles/<articleID>/comments", methods=["GET"])
def listComments(articleID):
    commentList = comments.find({"articleID":ObjectId(articleID)})
    resultList = []
    for comment in commentList:
        resultList.append({
            "body": comment["body"],
            "get":"/articles/{}/comments/{}".format(articleID, str(comment["_id"]))
        })
    return getResponseList(200, resultList)

@app.route("/articles/<articleID>/comments", methods=["POST"])
def createComment(articleID):
    params = request.get_json()
    errFlag = False
    errMsg = ""
    if not "body" in params:
        errFlag = True
        errMsg += "Missing field body"
    if errFlag:
        return getResponse(400, message=errMsg)

    newComment = {
        "body": params["body"],
        "articleID": ObjectId(articleID)
    }
    commentID = comments.insert_one(newComment).inserted_id

    return getResponse(
        201,
        get="/articles/{}/comments/{}".format(articleID, str(commentID))
    )



@app.route("/articles/<articleID>/comments/<commentID>", methods=["PUT"])
def updateComment(articleID, commentID):
   params = request.get_json()
   updateObj = {}
   if "body" in params:
      updateObj["body"] = params["body"]
   comments.update({'_id': ObjectId(commentID)},{"$set":updateObj})
   return getResponse(
    200,
    get="/articles/{}/comments/{}".format(articleID, str(commentID))
   )


def getResponseList(status, aList):
    if aList is None:
        aList = []
    resp = jsonify(aList)
    resp.status_code = status
    return resp

def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp 

if __name__=='__main__':
    app.run(debug=True, port=5003)
