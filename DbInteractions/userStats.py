import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback


def get_stats(userId):
    # Setting up an object to return. Object holds arrays of tasks completed and failed.
    user_tasks = {}
    user_tasks['completed'] = []
    user_tasks['failed'] = []
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to get tasks completed in the last 7 days.
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at, completed_at FROM task_actions inner join characters on characters.id = characterId inner join users on characters.userId = users.id inner join user_tasks on user_taskId = user_tasks.id WHERE users.id = ? and completed_at >= (CURDATE() - INTERVAL 7 DAY)", [userId])
        completed_tasks = cursor.fetchall()
        for task in completed_tasks:
            user_tasks['completed'].append({
                'taskId': task[0],
                'taskName': task[1],
                'taskDescription': task[2],
                'taskType': task[3],
                'started_at': task[4],
                'completed_at': task[5]
            })
            # Select statement to get task information, as well as character info. Where statement checks to get char WEEKLY tasks of charId passed to it, where started at is greater than the last thursday at 5AM. Task type must be weekly and completed at must be null so task is still in progress
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at, completed_at FROM task_actions inner join characters on characters.id = characterId inner join users on characters.userId = users.id inner join user_tasks on user_taskId = user_tasks.id WHERE users.id = ? and completed_at is NULL", [userId])
        weekly_tasks = cursor.fetchall()
        for task in weekly_tasks:
            user_tasks['failed'].append({
                'taskId': task[0],
                'taskName': task[1],
                'taskDescription': task[2],
                'taskType': task[3],
                'started_at': task[4],
                'completed_at': 'DNF'
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
