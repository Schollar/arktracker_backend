import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback


def get_tasks(charId):
    # Setting up an object to return. Object holds list of tasks.
    user_tasks = {}
    user_tasks['daily'] = []
    user_tasks['weekly'] = []
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to get task information, as well as character info. Where statement checks to get char DAILY tasks of charId passed to it, where started at is before the next day at 5AM. Task type must be daily and completed at must be null so task is still in progress
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at FROM task_actions inner join user_tasks on user_taskId = user_tasks.id WHERE task_actions.characterId = ? and started_at > DATE_ADD(CURDATE() -1 , INTERVAL '05:00' HOUR_MINUTE) and type = 'Daily' and completed_at is NULL", [charId])
        daily_tasks = cursor.fetchall()
        for task in daily_tasks:
            user_tasks['daily'].append({
                'taskId': task[0],
                'taskName': task[1],
                'taskDescription': task[2],
                'taskType': task[3],
                'started_at': task[4]
            })
            # Select statement to get task information, as well as character info. Where statement checks to get char WEEKLY tasks of charId passed to it, where started at is before the next thursday at 5AM. Task type must be weekly and completed at must be null so task is still in progress
        cursor.execute(
            "SELECT task_actions.id, user_tasks.name, user_tasks.description, user_tasks.type, started_at FROM task_actions inner join user_tasks on user_taskId = user_tasks.id WHERE task_actions.characterId = ? and started_at > CURDATE() - interval (7 + 3 - weekday(CURDATE())) % 7 day and type = 'Weekly' and completed_at is NULL", [charId])
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


def post_task(userId, taskname, taskdescription, tasktype, charId):
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to get task information, as well as character info. Where statement checks to get char DAILY tasks of charId passed to it, where started at is before the next day at 5AM. Task type must be daily and completed at must be null so task is still in progress
        cursor.execute(
            "INSERT INTO user_tasks (name, description, type, userId) VALUES (?, ?, ?, ?)", [taskname, taskdescription, tasktype, userId])
        conn.commit()
        cursor.execute(
            "SELECT id from user_tasks WHERE name = ? and description = ? and userId = ?", [
                taskname, taskdescription, userId]
        )
        taskId = cursor.fetchone()
        taskId = taskId[0]
        cursor.execute(
            "INSERT INTO task_actions (characterId, user_taskId) VALUES (?, ?)", [
                charId, taskId]
        )
        conn.commit()
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
    return True


def delete_task(taskId):
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to get task information, as well as character info. Where statement checks to get char DAILY tasks of charId passed to it, where started at is before the next day at 5AM. Task type must be daily and completed at must be null so task is still in progress
        cursor.execute(
            "DELETE FROM task_actions WHERE id = ?", [taskId])
        conn.commit()
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
    return True
