from flask import request, Response
import json
import DbInteractions.charInteractions as ci

# Get Character request requires the userId to send off. Return character info in the response


def get():
    char_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, char_list = ci.get_characters(user_id)
        char_json = json.dumps(char_list, default=str)
    except:
        return Response("Something went wrong getting user characters", mimetype="application/json", status=400)
    if(success):
        return Response(char_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting user characters", mimetype="application/json", status=400)

# Character post request to create a character. Requires userId and char info, send new char back in the response


def post():
    char_json = None
    success = False
    try:
        userId = request.json['userId']
        charName = request.json['charName']
        charClass = request.json['class']
        success, char = ci.add_character(userId, charName, charClass)
        char_json = json.dumps(char, default=str)
    except:
        return Response("Something went wrong adding a character", mimetype="application/json", status=400)
    if(success):
        return Response(char_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong adding a character", mimetype="application/json", status=400)

# Chare delete endpoint requires userId and char name, returns charId in response to make things easy on front end


def delete():
    charId_json = None
    success = False
    try:
        userId = request.json['userId']
        charName = request.json['charName']
        success, charId = ci.remove_character(userId, charName)
        charId_json = json.dumps(charId, default=str)
    except:
        return Response("Something went wrong removing a character", mimetype="application/json", status=400)
    if(success):
        return Response(charId_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong removing a character", mimetype="application/json", status=400)
