from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    "0":{"username":"testtestopoulos", "password":"2323g4ffeddf"},
    "1":{"username":"efkowekgfs", "password":"433424334"}
}


@app.route("/users/<userID>")
def getUser(userID):
    if not userID in users: 
        resp =  jsonify({"message":"User with id " + userID + " doesn't exist"})
        resp.status_code = 404
        return resp
    user = users[userID]
    return jsonify({"username":user["username"],"passwordLength":len(user["password"])})

@app.route("/users", methods=["POST"])
def createUser():
    error = False
    print(str(request.json))
    '''if not request.form.has_key("username"):
        error = "Missing username field. "
    if not "password" in request.form:
        error += "Missing password field. "
'''
    
    if error:
        resp = jsonify({"message":error})
        resp.status_code = 400
        return resp
    
