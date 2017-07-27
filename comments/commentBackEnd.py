
from flask import Flask, jsonify, request
from uuid import uuid4
import time

app = Flask(__name__)

comments = {
    "2":{
        "0":{"createDate":"03/02/1997-19:23","body":"Hello World"},
        "1":{"createDate":"03/02/1997-20:43","body":"Good job"}
    }
}

@app.route("/articles/<articleID>/comments", methods=["GET"])
def getComments(articleID):
    if not articleID in comments:
        return getResponse(404,message="Article with id {} doesn't exist".format(articleID))
    commentlist = []
    for commentID, comment in comments[articleID].items():
        print(comment)
        commentlist.append({
            "update":"/articles/{}/comments/{}".format(articleID,commentID),
            "createDate":comment["createDate"],
            "body":comment["body"]
        })
    return getResponseList(200, commentlist)

@app.route("/articles/<articleID>/comments", methods=["POST"])
def createComment(articleID):
    global comments
    if not articleID in comments:
        comments[articleID] = {}
    if request.data is None:
        return getResponse(400, message="Comment body is None")
    commentID = str(uuid4())
    comments[articleID][commentID] = {
        "createDate":time.strftime("%d/%m/%Y-%H:%M"),
        "body":request.data.decode('utf-8')
    }
    return getResponse(201, update="/articles/{}/comments/{}".format(articleID,commentID))

@app.route("/articles/<articleID>/comments/<commentID>", methods=["PUT"])
def updateComment(articleID, commentID):
    if not articleID in comments:
        return getResponse(404,message="Article with id {} doesn't exist".format(articleID))
    if not commentID in comments[articleID]:
        return getResponse(404,message="Comment with id {} doesn't exist".format(commentID))
    if request.data is None:
        return getResponse(400, message="Comment body is None")
    comment = comments[articleID][commentID]
    comment["body"] = request.data.decode('utf-8')
    comments[articleID][commentID] = comment
    return getResponse(200,list="/article/{}/comments".format(articleID))
    
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
