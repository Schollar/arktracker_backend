import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback

# Function that takes in a userId to get users characters.


def get_characters(userId):
    characters = []
    conn, cursor = dbh.db_connect()
    user_characters = []
    try:
        cursor.execute(
            "SELECT characters.id, name, class, username FROM users inner join characters on characters.userId = users.id WHERE users.id = ?", [userId])
        characters = cursor.fetchall()
        # Convert data to object and append to user characters array
        for char in characters:
            user_characters.append({
                'charId': char[0],
                'name': char[1],
                'class': char[2],
                'username': char[3]
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
    # TODO Add logic here, always returns true?? Return array of user characters
    return True, user_characters


def add_character(userId, charName, charClass):
    character = {}
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute("INSERT INTO characters (name, class, userId ) VALUES (?, ?, ?)", [
            charName, charClass, userId])
        rowcount = cursor.rowcount
        conn.commit()
        cursor.execute(
            "SELECT characters.id, name, class, username FROM users inner join characters on characters.userId = users.id WHERE users.id = ? and characters.name = ?", [userId, charName])
        character = cursor.fetchone()
        character = {
            'charId': character[0],
            'name': character[1],
            'class': character[2],
            'username': character[3]
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
    if(rowcount < 1):
        return False
    else:
        return True, character
