#Metadata Service
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

#globals
clientDB = MongoClient('mongodb://192.168.99.100:27017')
db = clientDB["metadata"]
articlesMetadata = db["articles-metadata-collection"]
app = Flask(__name__)

#Rest EndPoints
@app.route("/articles/<articleID>/like", methods=["POST"])
def like(articleID):
   articlesMetadata.update({'_id': ObjectId(articleID)},{"$inc":{"likes":1}})
   return ('', 200)

@app.route("/articles/<articleID>/dislike", methods=["POST"])
def dislike(articleID):
    articlesMetadata.update({'_id': ObjectId(articleID)},{"$inc":{"dislikes":1}})
    return ('', 200)

@app.route("/articles/<articleID>/metadata", methods=["GET"])
def getArticleMetadata(articleID):
    metadata = articlesMetadata.find_one({"_id": ObjectId(articleID)})
    if metadata is None:
        metadata = {
            "_id": ObjectId(articleID),
            "views":1,
            "likes":0,
            "dislikes":0
        }
        articlesMetadata.insert_one(metadata)
    else:
        articlesMetadata.update({'_id': ObjectId(articleID)},{"$inc":{"views":1}})

    return getResponse(
        200,
        views = metadata["views"],
        likes = metadata["likes"],
        dislikes = metadata["dislikes"]
    )

def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp    

#Running Program
if __name__=='__main__':
    app.run(debug=True, port=5001)
