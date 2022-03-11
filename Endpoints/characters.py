from flask import request, Response
import json
import DbInteractions.charInteractions as ci


def get():
    char_json = None
    success = False
    try:
        user_id = request.args['userId']
        success, char_list = ci.get_characters(user_id)
        char_json = json.dumps(char_list, default=str)
    except:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
    if(success):
        return Response(char_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
