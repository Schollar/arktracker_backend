from flask import request, Response
import DbInteractions.charTasks as ct
import json

# Function that requires a characterId to get that chars tasks. Returns Object with lists(arrays) of tasks as key value pairs daily, weekly


def get():
    char_json = None
    success = False
    try:
        charId = request.args['charId']
        success, task_list = ct.get_tasks(charId)
        char_json = json.dumps(task_list, default=str)
    except:
        return Response("Something went wrong getting character tasks", mimetype="application/json", status=400)
    if(success):
        return Response(char_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting character tasks", mimetype="application/json", status=400)

# Function that takes in a bunch of user required input to post a new task for a character. return newly added task in response


def post():
    success = False
    task_json = None
    try:
        userId = request.json['userId']
        taskname = request.json['taskName']
        taskdescription = request.json['taskDescription']
        tasktype = request.json['taskType']
        charId = request.json['charId']
        success, task = ct.post_task(
            userId, taskname, taskdescription, tasktype, charId)
        task_json = json.dumps(task, default=str)
    except:
        return Response("Something went wrong creating a new task", mimetype="application/json", status=400)
    if(success):
        return Response(task_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong creating a new task", mimetype="application/json", status=400)


# Delete function that requires a taskId to be deleted. If success comes back as true, return a plain text response confirming.

def delete():
    success = False
    try:
        taskId = request.json['taskId']
        success = ct.delete_task(taskId)
    except:
        return Response("Something went wrong deleting the task", mimetype="application/json", status=400)
    if(success):
        return Response("Task has been deleted.", mimetype="plain/text", status=200)
    else:
        return Response("Something went wrong deleting the task", mimetype="application/json", status=400)

# Patch function that takes in a taskId. If success returns as true. return completed task in response


def patch():
    success = False
    task_json = None
    try:
        taskId = request.json['taskId']
        success, task = ct.patch_task(taskId)
        task_json = json.dumps(task, default=str)
    except:
        return Response("Something went wrong updating the task", mimetype="application/json", status=400)
    if(success):
        return Response(task_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong updating the task", mimetype="application/json", status=400)
