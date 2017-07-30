#Article BackEnd
from flask import Flask, jsonify, request
from uuid import uuid4
import pika, json

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
def createAsrticle():
   global articles
   id = str(uuid4())
   data = request.get_json()
   articles[id] = data["body"]
   sendObj = {
      "articleID":id,
      "title":data["title"],
      "authorID":data["authorID"]
   }

   channel.basic_publish(
      exchange='',
      routing_key='createArticle',
      body=json.dumps(sendObj)
   )
   
   
   return getResponse(
      201,
      get="/articles/{}".format(id),
      metadata="/articles/{}/metadata".format(id)
   )

@app.route("/articles/<articleID>", methods=["PUT"])
def updateArticle(articleID):
   global articles
   if not articleID in articles:
      return getResponse(404,message="Articles with id {} doesn't exist".format(articleID))
   params = request.json
   if "body" in params:
      articles[articleID] = params["body"]
   if "title" in params:
      channel.basic_publish(
         exchange="",
         routing_key="updateArticle",
         body=json.dumps({
            "title": params["title"],
            "articleID": articleID
         })
      )
      print(params["title"]) 
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

if __name__=='__main__':
   app.run(debug=True, port=5000)
