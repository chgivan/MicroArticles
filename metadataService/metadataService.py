from threading import Thread
from flask import Flask, jsonify, request
import pika

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100'))
channel = connection.channel()
channel.queue_declare(queue="createArticle")

cache = {
    "0":{
        "title":"Hello World",
        "likes":123,
        "dislikes":32,
        "views":89322,
        "authorID":"0",
        "authorUsername":"Chris"
    }
}

def OnArticleCreated():
    print("Received Message")
    
def testThread():
    channel.basic_consume(OnArticleCreated,queue="createArticle",no_ack=True)
    channel.start_consuming()
    print("Start Consuming")
    
thread = Thread(target=testThread)
thread.start()

@app.route("/articles/<articleID>/like", methods=["GET"])
def like(articleID):
    global cache
    if not articleID in cache:
        return getResponse(404,"Article with id {} doesn't exist".format(articleID))
    cache[articleID]["likes"] += 1
    return getResponse(200)

@app.route("/articles/<articleID>/dislike", methods=["GET"])
def dislike(articleID):
    global cache
    if not articleID in cache:
        return getResponse(404,"Article with id {} doesn't exist".format(articleID))
    cache[articleID]["dislikes"] += 1
    return getResponse(200)

@app.route("/articles/<articleID>/metadata", methods=["GET"])
def getArticleMetadata(articleID):
    if not articleID in cache:
        return getResponse(404,"Article with id {} doesn't exist".format(articleID))
    metadata = cache[articleID]
    return getResponse(
        200,
        title=metadata["title"],
        likes=metadata["likes"],
        dislikes=metadata["dislikes"],
        views=metadata["views"],
        get_author="/users/{}".format(metadata["authorID"]),
        post_like="/articles/{}/like".format(articleID),
        post_dislike="/articles/{}/dislike".format(articleID),
        authorUsername=metadata["authorUsername"]
    )

@app.route("/articles", methods=["GET"])
def listArticlesMetadata():
    articleList = []
    for articleID, metadata in cache.items():
        articleList.append({
            "title":metadata["title"],
            "views":metadata["views"],
            "authorUsername":metadata["authorUsername"],
            "get_author":"/users/{}".format(metadata["authorID"]),
            "get_article":"/articles/{}".format(articleID)
        })
    return getResponseList(200, articleList)

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

