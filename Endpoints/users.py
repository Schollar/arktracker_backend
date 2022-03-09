from flask import request, Response
import json
import DbInteractions.userInteractions as ue
import DbInteractions.dbhandler as dbh
import secrets
import hashlib


# Function to create password salts

def create_salt():
    return secrets.token_urlsafe(10)

# This endpoint takes in an optional user id. If no Id is sent it will get ALL users from DB back. If ID is sent only info about that user is sent back.
# If success returns True, return converted data in the reponse


def get():
    users_json = None
    success = False
    try:
        user_id = request.args.get('userId')
        success, user_list = ue.get_users(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)

# This endpoint will update user information based on what is sent to it. All optional except for logintoken which is required, you can send info seperatly or all at once.
# Convert the returned data to json, and if successful return the converted data in the response


def patch():
    user_json = None
    success = False
    try:
        loginToken = request.json['loginToken']
        email = request.json.get('email')
        username = request.json.get('username')
        success, user = ue.patch_user(
            loginToken, email, username)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong editing user information", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong editing user information", mimetype="application/json", status=400)

# This endpoint will delete a user from the DB. it takes in a password and login token, and if matching will return nothing indicating user no longer exits on planet.
# Use the helper get password function to get hashed+salted password. If dbinteractions function returns success as True, return a response with None.


def delete():
    success = False
    try:
        logintoken = request.json['loginToken']
        password = request.json['password']
        pass_hash = dbh.get_password(password, logintoken=logintoken)
        success = ue.delete_user(logintoken, pass_hash)
    except:
        return Response("Something went wrong deleting this user", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong deleting this user", mimetype="application/json", status=400)

# This endpoint creates a new user. It takes in a bunch of data that is required and two optional peices of data. It also creates a salt for the user and hashes the salted password.
# Convert the returned data to json, return the converted data in the response if success returned as true.


def post():
    user_json = None
    success = False
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        salt = create_salt()
        password = salt + password
        pass_hash = hashlib.sha512(password.encode()).hexdigest()
        success, user = ue.post_user(email, username, pass_hash, salt)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong creating a new user", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong create a new user", mimetype="application/json", status=400)
