#Users BackEnd
from pony import orm
from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    "0":{"username":"testtestopoulos", "password":"2323g4ffeddf"},
    "1":{"username":"efkowekgfs", "password":"433424334"}
}
usersCount = 1
db = orm.Database("sqlite", "tmp.sqlite", create_db=True)

class User(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)

db.generate_mapping(create_tables=True)
orm.sql_debug(True)

@app.route("/users/<userID>", methods=["GET"])
def getUser(userID):
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
    errorFlag = False
    errorMsg = ""
    params = request.json
    if not "username" in params:
        errorMsg += "Missing username field.\n"
        errorFlag = True
    if not "password" in params:
        errorMsg += "Missing password field.\n"
        errorFlag = True
    if errorFlag:
        return getResponse(400, message=error)

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
def listUser():
    results = {}
    with orm.db_session:
        select_sql = 'SELECT username, id FROM User WHERE id IN(6,7,9)'
        r = User.select_by_sql(select_sql)[:]
        print (str(r))
    for userID in request.json:
        if userID in users:
            results[userID] = users[userID]["username"]
    resp = jsonify(results)
    resp.status_code = 200
    return resp

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
