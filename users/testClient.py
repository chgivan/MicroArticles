import requests
import sys
host = "http://localhost:8080"

##Send a  request to find if a user token is valid or not

#get user id and token at args
if (len(sys.argv) != 3):
    print("[Error] Missing userID and/or token")
    sys.exit(-1)
userID = sys.argv[1]
token = sys.argv[2]
#Send request
url = "{}/users/{}/isValidToken".format(host,userID)
r = requests.post(url, json = {'token':token})
#Check status_code | output result
if r.status_code == 200:
    print("Success")
    print("is token valid =" + str(r.json()["isValid"]))
#Or check for error | outpout error
else:
    print(r.status_code)
    print(r.json()["message"])


