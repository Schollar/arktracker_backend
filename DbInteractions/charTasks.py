import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback


def get_tasks(charId):
    user_tasks = {}
    user_tasks['daily'] = []
    user_tasks['weekly'] = []
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at FROM task_actions inner join user_tasks on user_taskId = user_tasks.id WHERE task_actions.characterId = ? and started_at < DATE_ADD(CURDATE() +1 , INTERVAL '05:00' HOUR_MINUTE) and type = 'Daily' and completed_at is NULL", [charId])
        daily_tasks = cursor.fetchall()
        for task in daily_tasks:
            user_tasks['daily'].append({
                'taskId': task[0],
                'taskName': task[1],
                'taskDescription': task[2],
                'taskType': task[3],
                'started_at': task[4]
            })
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at FROM task_actions inner join user_tasks on user_taskId = user_tasks.id WHERE task_actions.characterId = ? and started_at < CURDATE() + interval (7 + 3 - weekday(CURDATE())) % 7 day and type = 'Weekly' and completed_at is NULL", [charId])
        weekly_tasks = cursor.fetchall()
        for task in weekly_tasks:
            user_tasks['weekly'].append({
                'taskId': task[0],
                'taskName': task[1],
                'taskDescription': task[2],
                'taskType': task[3],
                'started_at': task[4]
            })
    except db.OperationalError:
        traceback.print_exc()
        print('Something went wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    dbh.db_disconnect(conn, cursor)

    return True, user_tasks
