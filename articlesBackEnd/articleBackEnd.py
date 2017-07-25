from flask import Flask
app = Flask(__name__)

articles = {
    "ag3egfd":"agjiejisjijsdigjsidgsdgjsg",
    "24rfe":"agokwoeggkj0g3k0g",
    "g33r":"t03gkekg03gk303"
}

@app.route("/articles/<articleID>")
def getArticle(articleID):
   return articles[articleID]
