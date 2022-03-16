import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback


def get_tasks(charId):
    # Setting up an object to return. Object holds arrays of tasks.
    user_tasks = {}
    user_tasks['daily'] = []
    user_tasks['weekly'] = []
    conn, cursor = dbh.db_connect()
    try:
        # Select statement to get task information, as well as character info. Where statement checks to get char DAILY tasks of charId passed to it, where started at is greater than the current day minus one at 5am. Task type must be daily and completed at must be null so task is still in progress
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
            # Select statement to get task information, as well as character info. Where statement checks to get char WEEKLY tasks of charId passed to it, where started at is greater than the last thursday at 5AM. Task type must be weekly and completed at must be null so task is still in progress
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
    task = None
    try:
        # Insert statment to create a new task in the user_tasks table
        cursor.execute(
            "INSERT INTO user_tasks (name, description, type, userId) VALUES (?, ?, ?, ?)", [taskname, taskdescription, tasktype, userId])
        conn.commit()
        # Select statement to select the task just inserted to return it.
        cursor.execute(
            "SELECT id, name, description, type, userId from user_tasks WHERE name = ? and description = ? and userId = ?", [
                taskname, taskdescription, userId]
        )
        task = cursor.fetchone()
        # Setting the task as an object
        task = {
            'taskId': task[0],
            'taskName': task[1],
            'taskDescription': task[2],
            'taskType': task[3],
            'userId': task[4]
        }
        # Insert statement to start tracking the task. I assume users input tasks they want to track instead of having another button or request to start a task. Instead i just do it here
        cursor.execute(
            "INSERT INTO task_actions (characterId, user_taskId) VALUES (?, ?)", [
                charId, task['taskId']]
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
    return True, task

# Function to delete a task that is in progress. Requires a taskId. Returns true if rowcount is greater than 1


def delete_task(taskId):
    rowcount = None
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "DELETE FROM task_actions WHERE id = ?", [taskId])
        rowcount = cursor.rowcount
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
    if(rowcount < 1):
        return False
    else:
        return True


def patch_task(taskId):
    conn, cursor = dbh.db_connect()
    task = None
    try:
        # Insert statment to insert the current timestamp into completed at
        cursor.execute(
            "UPDATE task_actions SET completed_at = now() WHERE id = ?", [taskId])
        conn.commit()
        # Select statement to select the task just completed
        cursor.execute(
            "SELECT task_actions.id, name, description, type, userId from user_tasks inner join task_actions on user_taskId = user_tasks.id WHERE task_actions.id = ?", [
                taskId]
        )
        task = cursor.fetchone()
        # Setting the task as an object
        task = {
            'taskId': task[0],
            'taskName': task[1],
            'taskDescription': task[2],
            'taskType': task[3],
            'userId': task[4]
        }
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
    return True, task
