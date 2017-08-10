#Users BackEnd
from pony import orm
from flask import Flask, jsonify, request
import uuid, json
from os import environ

port = int(environ.get("PORT", 5000))
debug = bool(environ.get("DEBUG", False))
dbhost = environ.get("DB_HOST")
dbuser = environ.get("DB_USER")
dbpassword = environ.get("DB_PASSWORD")
dbase = environ.get("DB_DATABASE")

app = Flask(__name__)
db = orm.Database()
db.bind(
    provider='postgres',
    user=dbuser,
    password=dbpassword,
    host=dbhost,
    database=dbase
)

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
            if user is None:
                return getResponse(404, message="Wrong username or password")
            global tokens
            token = str(uuid.uuid4())
            tokens[str(user.id)] = token
            return getResponse(200, userID = str(user.id), token=token)
    except orm.core.ObjectNotFound:
        return getResponse(404, message="Wrong username or password")

@app.route("/users/<userID>", methods=["GET"])
def getUser(userID):
    try:
        with orm.db_session():
            user = User[userID]
            return getResponse(
                200,
                username=user.username,
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
        userID=str(userID),
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

@app.route("/users", methods=["GET"])
def listUsers():
    ids = request.args.get("ids",default=None)
    if ids is None:
        return getResponse(400, message="Missing ids parameter")
    results = {}
    for userID in ids.split(','):
        results[userID] = "NULL"
    with orm.db_session:
        for userID, username in orm.select((u.id, u.username) for u in User):
            userID = str(userID)
            if userID in results:
                results[userID] = username
    resp= jsonify(results)
    resp.status_code = 200
    return resp

@app.route("/users/<userID>/isValidToken", methods=["POST"])
def isValidToken(userID):
    data = request.get_json(force=True, silent=True)
    if data is None:
        return getResponse(400, message="Fail to readed json data")
    errFlag = False
    errMsg = ''
    if not "token" in data:
        errFlag = True
        errMsg += "Missing field token"
    if errFlag:
        return getResponse(400, message=errMsg)

    return getResponse(
        200,
        isValid=validToken(token=data["token"],userID=userID)
    )

def validToken(token, userID):
    global tokens
    if not userID in tokens:
        return False
    return tokens[userID] == token

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
    app.run(host="0.0.0.0", debug=debug, port=port)
