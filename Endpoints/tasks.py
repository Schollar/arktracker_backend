from flask import request, Response
import DbInteractions.charTasks as ct
import DbInteractions.dbhandler as dbh
import json


def get():
    char_json = None
    success = False
    try:
        charId = request.args['charId']
        success, task_list = ct.get_tasks(charId)
        char_json = json.dumps(task_list, default=str)
    except:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
    if(success):
        return Response(char_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
