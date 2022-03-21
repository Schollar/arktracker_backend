from flask import request, Response
import json
import DbInteractions.userInteractions as ue
import DbInteractions.dbhandler as dbh
import secrets
import hashlib


# Function to create password salts

def create_salt():
    return secrets.token_urlsafe(10)

# Get endpoint to get user info, requires userId
# If success returns True, return converted data in the reponse


def get():
    users_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, user_list = ue.get_users(user_id)
        users_json = json.dumps(user_list, default=str)
    except:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
    if(success):
        return Response(users_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)

# This endpoint will update user information based on what is sent to it. returns updated user info in response


def patch():
    user_json = None
    success = False
    try:
        userId = request.json['userId']
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        # Checking to see if user is changing password, if not empty go through the salt and hash process
        if(password != None and password != ''):
            salt = create_salt()
            password = salt + password
            password = hashlib.sha512(password.encode()).hexdigest()
        success, user = ue.patch_user(userId, email, username, password, salt)
        user_json = json.dumps(user, default=str)
    except:
        return Response("Something went wrong editing user information", mimetype="application/json", status=400)
    if(success):
        return Response(user_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong editing user information", mimetype="application/json", status=400)

# Endpoint to delete a user. NOT CURRENTLY IN USE


def delete():
    success = False
    try:
        logintoken = request.cookies['logintoken']
        password = request.json['password']
        pass_hash = dbh.get_password(password, logintoken=logintoken)
        success = ue.delete_user(logintoken, pass_hash)
    except:
        return Response("Something went wrong deleting this user", mimetype="application/json", status=400)
    if(success):
        return Response(None, status=200)
    else:
        return Response("Something went wrong deleting this user", mimetype="application/json", status=400)

# This endpoint creates a new user. Takes in requires data. It also creates a salt for the user and hashes the salted password.
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
