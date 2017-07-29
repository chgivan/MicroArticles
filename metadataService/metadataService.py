import threading, json
from time import sleep
from flask import Flask, jsonify, request
import pika, redis

from diskcache import Cache

#globals
redisDB = redis.StrictRedis(host='192.168.99.100', port=6379, db=0)
app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100'))
channel = connection.channel()
channel.queue_declare(queue="createArticle")
internal_lock = threading.Lock()

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

#Message Bus communications
def OnArticleCreated(ch, method, prop, body):
    print(str(json.loads(body)))
    obj = json.loads(body)
    id = obj['articleID']
    with redisDB.pipeline() as pipe:
        pipe.hset(id, "title", obj['title'])
        pipe.hset(id, "authorUsername", "Change this later")
        pipe.hset(id, "authorID", obj["authorID"])
        pipe.hset(id, "views", 0)
        pipe.hset(id, "likes", 0)
        pipe.hset(id, "dislikes", 0)
        r = pipe.execute()
        print(r)
                  
def _process_data_events():
    channel.basic_consume(OnArticleCreated, queue='createArticle', no_ack=True)
    while True:
        with internal_lock:
            connection.process_data_events()
            sleep(0.1)

#Rest EndPoints
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
    if not redisDB.exists(articleID):
        return getResponse(404,message="Article with id {} doesn't exist".format(articleID))
    pipe = redisDB.pipeline()
    pipe.hget(articleID, "title")
    pipe.hget(articleID, "views")
    pipe.hget(articleID, "likes")
    pipe.hget(articleID, "dislikes")
    pipe.hget(articleID, "authorID")
    pipe.hget(articleID, "authorUsername")
    rList = pipe.execute()
    print(rList)
    return getResponse(
        200,
        title=rList[0].decode("utf-8"),
        views=int(rList[1]),
        likes=int(rList[2]),
        dislikes=int(rList[3]),
        get_author="/users/{}".format(rList[4].decode("utf-8")),
        get="/articles/{}".format(articleID),
        authorUsername=rList[5].decode("utf-8")
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

#Utils Functions
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

#Running Program
thread = threading.Thread(target=_process_data_events)
thread.setDaemon(True)
if __name__=='__main__':
    thread.start()
    app.run(debug=True, port=5001)
