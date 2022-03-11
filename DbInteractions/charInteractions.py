import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback


def get_characters(userId):
    characters = []
    conn, cursor = dbh.db_connect()
    user_characters = []
    try:
        cursor.execute(
            "SELECT characters.id, name, class, username FROM users inner join characters on characters.userId = users.id WHERE users.id = ?", [userId])
        characters = cursor.fetchall()
        for char in characters:
            user_characters.append({
                'charId': char[0],
                'name': char[1],
                'class': char[2],
                'username': char[3]
            })
        dbh.db_disconnect(conn, cursor)
        return True, user_characters
    except db.OperationalError:
        traceback.print_exc()
        print('Something went wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
