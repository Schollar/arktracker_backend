from flask import request, Response
import json
import DbInteractions.userStats as us


def get():
    tasks_json = None
    success = False
    try:
        user_id = request.args.get('userId')
        success, task_list = us.get_stats(user_id)
        tasks_json = json.dumps(task_list, default=str)
    except:
        return Response("Something went wrong getting task information", mimetype="application/json", status=400)
    if(success):
        return Response(tasks_json, mimetype="application/json", status=200)
    else:
        return Response("Something went wrong getting task information", mimetype="application/json", status=400)
