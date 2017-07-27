from flask import Flask, jsonify, request
from uuid import uuid4
import pika

app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.99.100'))
channel = connection.channel()
channel.queue_declare(queue="createArticle")

articles = {
    "ag3egfd":"agjiejisjijsdigjsidgsdgjsg",
    "24rfe":"agokwoeggkj0g3k0g",
    "g33r":"t03gkekg03gk303"
}

@app.route("/articles/<articleID>")
def getArticle(articleID):
   if not articleID in articles:
      return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
   return articles[articleID]

@app.route("/articles", methods=["POST"])

def createArticle():
   if request.data is None:
      return getResponse(400, message=errMsg)

   global articles
   id = str(uuid4())
   articles[id] = request.data

   channel.basic_publish(
      exchange='',
      routing_key='hello',
      body='Hello World'
   )
   
   
   return getResponse(201,get="/articles/{}".format(id))

@app.route("/articles/<articleID>", methods=["PUT"])
def updateArticle(articleID):
   if not articleID in articles:
      return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
   global article
   article = articles[articleID]
   if request.data is not None:
      articles[articleID] = request.data      

   return getResponse(
      200,
      get="/articles/{}".format(articleID),
   )
   

def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp
