from flask import request, Response
import DbInteractions.userLogin as ul
import DbInteractions.dbhandler as dbh
import json

# Delete endpoint, takes in a login token, upon success it deletes row from user session table(logs user out). If success returns true, return a response of None.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        success = ul.delete_login(logintoken)
    except:
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong with logging out", mimetype="application/json", status=400)

# Function to create a new row in user_session table(log a user in). After getting password, use helper function to get the hashed+salted password. Send data to dbinteractions function
# Convert the returned data to json, and if success returns true, return the converted data in the response


def post():
    user_json = None
    success = False
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json['password']
        pass_hash = dbh.get_password(password, email=email, username=username)
        success, user = ul.post_login(
            email, username, pass_hash)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong logging in.", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong logging in.", mimetype="application/json", status=400)
