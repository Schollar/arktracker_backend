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

# Function to add a character, takes in userId character name and class


def add_character(userId, charName, charClass):
    character = {}
    conn, cursor = dbh.db_connect()
    try:
        # Insert statement inserts character into DB
        cursor.execute("INSERT INTO characters (name, class, userId ) VALUES (?, ?, ?)", [
            charName, charClass, userId])
        # Grab the rowcount to verify things happened
        rowcount = cursor.rowcount
        conn.commit()
        # Select statement to grab the newly added character to return
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
    # If rowcount is less than one nothing happened, if not return the new character
    if(rowcount < 1):
        return False
    else:
        return True, character

# Function to remove a character, requires userId and character name


def remove_character(userId, charName):
    charId = None
    conn, cursor = dbh.db_connect()
    try:
        # Grab the charId to return to make things easy on the front end to remove character without running another request
        cursor.execute(
            "SELECT id FROM characters WHERE userId = ? and name = ?", [userId, charName])
        charId = cursor.fetchone()
        charId = charId[0]
#  Delete statement
        cursor.execute("DELETE FROM characters WHERE name = ? and userId = ?", [
                       charName, userId])
        # Grabbing the rowcount to confirm something happened
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
        # Return the charId to make things easy on the front end to remove character from list
        return True, charId
