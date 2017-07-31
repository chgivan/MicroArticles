#Metadata Service
import threading, json
from time import sleep
from flask import Flask, jsonify, request
import pika, redis

#globals
redisDB = redis.StrictRedis(host='192.168.99.100', port=6379, db=0)
app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100'))
channel = connection.channel()
channel.queue_declare(queue="createArticle")
channel.queue_declare(queue="updateArticle")
internal_lock = threading.Lock()

#Message Bus communications
def OnArticleCreated(ch, method, prop, body):
    obj = json.loads(body)
    id = obj['articleID']
    with redisDB.pipeline() as pipe:
        pipe.hset(id, "title", obj['title'])
        pipe.hset(id, "authorID", obj["authorID"])
        pipe.hset(id, "views", 0)
        pipe.hset(id, "likes", 0)
        pipe.hset(id, "dislikes", 0)
        pipe.hset(id, "lastModifiedTimestamp", obj["timestamp"])
        r = pipe.execute()

def OnArticleUpdated(ch, method, prop, body):
    obj = json.loads(body)
    id = obj['articleID']
    with redisDB.pipeline() as pipe:
        pipe.hset(id, "title", obj['title'])
        pipe.hset(id, "lastModifiedTimestamp", obj["timestamp"])
        r = pipe.execute()
    print(obj['title'])    


def _process_data_events():
    channel.basic_consume(OnArticleCreated, queue='createArticle', no_ack=True)
    channel.basic_consume(OnArticleUpdated, queue='updateArticle', no_ack=True)
    channel.basic_consume(OnUserCreated, queue='createUser', no_ack=True)

    while True:
        with internal_lock:
            connection.process_data_events()
            sleep(0.1)

#Rest EndPoints
@app.route("/articles/<articleID>/like", methods=["POST"])
def like(articleID):
    redisDB.hincrby(articleID, "likes", 1)
    return getResponse(200)

@app.route("/articles/<articleID>/dislike", methods=["POST"])
def dislike(articleID):
    redisDB.hincrby(articleID, "dislikes", 1)
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
    pipe.hget(articleID, "lastModifiedTimestamp")
    pipe.hincrby(articleID, "views", 1)
    rList = pipe.execute()
    userID = rList[4].decode("utf-8")
    return getResponse(
        200,
        title=rList[0].decode("utf-8"),
        views=int(rList[1]),
        likes=int(rList[2]),
        dislikes=int(rList[3]),
        get_author="/users/{}".format(userID),
        get="/articles/{}".format(articleID),
        lastModified=rList[5].decode("utf-8")
    )  

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
