#Users BackEnd
from pony import orm
from flask import Flask, jsonify, request
import pika
import uuid, json

app = Flask(__name__)
db = orm.Database("sqlite", "tmp.sqlite", create_db=True)
connMQ = pika.BlockingConnection(
    pika.ConnectionParameters(host="192.168.99.100")
)
channelMQ = connMQ.channel()
channelMQ.exchange_declare(exchange='auth', type='fanout')

tokens = {}
class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)

db.generate_mapping(create_tables=True)
orm.sql_debug(True)

@app.route("/login", methods=['POST'])
def login():
    params = request.json
    errFlag, errMsg = validParams(params)
    if errFlag:
        return getResponse(400, message=errMsg)

    try:
        with orm.db_session:
            user = orm.select(
                user for user in User
                if user.password == params["password"]
                and user.username == params["username"]
            ).first()
            global tokens
            token = str(uuid.uuid4())
            tokens[token] = user.id
            channelMQ.basic_publish(
                exchange='auth',
                routing_key='',
                body=json.dumps({"id":user.id,"token":token})
            )
            return getResponse(200, userID = user.id, token=token)
    except orm.core.ObjectNotFound:
        return getResponse(404, message="Wrong username or password")

@app.route("/users/<userID>", methods=["GET"])
def getUser(userID):
    token = request.args.get('token')
    if token is None:
        return getResponse(400,message="Missing token!")
    if not validToken(token=token, userID=userID):
        return getResponse(403,message="Access Denied!!")
    try:
        with orm.db_session():
            user = User[userID]
            return getResponse(
                200,
                username=user.username,
                passwordLength=len(user.password),
                get="/users/{}".format(userID)
            )
    except orm.core.ObjectNotFound:
        return getResponse(404, message="User id {} doesn't exist".format(userID))

@app.route("/users", methods=["POST"])
def createUser():
    params = request.json
    errFlag, errMsg = validParams(params)
    if errFlag:
        return getResponse(400, message=errMsg)

    userID = None
    try:
        with orm.db_session:
            user = User(
                username=params["username"],
                password=params["password"]
            )
            orm.commit()
            userID = user.id
    except orm.core.TransactionIntegrityError:
        return getResponse(400, message="User with username {} already exist!".format(params["username"]))

    return getResponse(
        201,
        get="/users/{}".format(userID)
    )

@app.route("/users/<userID>", methods=["PUT"])
def updateUser(userID):
    params = request.json
    if not "token" in params:
        return getResponse(400,message="Missing token!")
    if not validToken(token=params["token"],userID = userID):
        return getResponse(403,message="Access Denied!!")

    if not "password" in params:
        return getResponse(400, message="No password given!!") 

    try:
        with orm.db_session:
            user = User[userID]
            user.password = params["password"]
            return getResponse(
                200,
                get="/users/{}".format(userID),
                message="Updated data of user with id {}".format(userID)
            )
    except orm.core.ObjectNotFound:
        return getResponse(
            404,
            message="User ID {} doesn't exist!".format(userID)
        )

@app.route("/list/users", methods=["POST"])
def listUsers():
    results = {}
    idList = ""
    for userID in request.json:
        idList += "{},".format(userID)
    if idList[-1] == ',':
        idList = idList[:-1]
    with orm.db_session:
        select_sql = 'SELECT username, id FROM User WHERE id IN({})'.format(idList)
        print(select_sql)
        r = User.select_by_sql(select_sql)[:]
        print (str(r))
        for user in r:
            results[user.id] = user.username
    resp = jsonify(results)
    resp.status_code = 200
    return resp

def validToken(token, userID):
    global tokens
    if not token in tokens:
        return False
    return int(tokens[token]) == int(userID)

def validParams(params):
    errorFlag = False
    errorMsg = ""
    if not "username" in params:
        errorMsg += "Missing username field.\n"
        errorFlag = True
    if not "password" in params:
        errorMsg += "Missing password field.\n"
        errorFlag = True
    return errorFlag, errorMsg

def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp

if __name__=='__main__':
    print("Starting User BackEnd")
    app.run(debug=True, port=5002)
