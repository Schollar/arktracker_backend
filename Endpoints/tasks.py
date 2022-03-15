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


def post():
    task_json = None
    success = False
    try:
        userId = request.json['userId']
        taskname = request.json['taskName']
        taskdescription = request.json['taskDescription']
        tasktype = request.json['taskType']
        charId = request.json['charId']
        success = ct.post_task(
            userId, taskname, taskdescription, tasktype, charId)
    except:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
    if(success):
        return Response("New task added.", mimetype="plain/text", status=200)
    else:
        return Response("Something went wrong getting user information", mimetype="application/json", status=400)
