from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    "0":{"username":"testtestopoulos", "password":"2323g4ffeddf"},
    "1":{"username":"efkowekgfs", "password":"433424334"}
}
usersCount = 1

@app.route("/users/<userID>", methods=["GET"])
def getUser(userID):
    global users
    if not userID in users:
        return getResponse(404, message="User id {} doesn't exist".format(userID))
    user = users[userID]
    return getResponse(
        200,
        username=user["username"],
        passwordLength=len(user["password"]),
        update="/users/{}".format(userID)
    )

@app.route("/users", methods=["POST"])
def createUser():
    global usersCount, users
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
    for userID, user in users.items():
        if user["username"] ==  params["username"]:
            return getResponse(400, message="username {} already exists! ".format(params["username"]))
    usersCount += 1
    users[str(usersCount)] = {"username":params["username"],"password":params["password"]}
    
    return getResponse(
        201,
        get="/users/{}".format(usersCount),
        update="/users/{}".format(usersCount)
    )

@app.route("/users/<userID>", methods=["PUT"])
def updateUser(userID):
    global users
    if not userID in users:
        return getResponse(404, message="User id {} doesn't exist".format(userID))
    user = users[userID]
    params = request.json
    if "password" in params:
        user["password"] = params["password"]
    users[userID] = user
    print (users)
    return getResponse(
        200,
        get="/users/{}".format(userID),
        message="Updated data of user with id {}".format(userID)
    )
    
def getResponse(status, **kwargs):
    obj = {}
    if kwargs is not None:
        obj = kwargs
    resp = jsonify(obj)
    resp.status_code = status
    return resp
