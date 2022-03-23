import mariadb as db
import DbInteractions.dbhandler as dbh
import traceback
import secrets

# Function to delete a login token(log a user out)


def delete_login(loginToken):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement, commit disconnect and return true
        cursor.execute(
            "DELETE FROM user_session WHERE logintoken = ? ", [loginToken])
        conn.commit()
        rowcount = cursor.rowcount
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
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

# Function that creates a new user session(log a user in)


def post_login(email, username, pass_hash):
    user = []
    userId = None
    conn, cursor = dbh.db_connect()
    try:
        # Check to see wether we are passed the username or email, and based on which does not have a value of None is which statement is ran to get the userId.
        if(email != None):
            cursor.execute(
                "SELECT users.id FROM users WHERE email = ? and password = ?", [email, pass_hash])
            userId = cursor.fetchone()

            userId = userId[0]
        elif(username != None):
            cursor.execute(
                "SELECT users.id FROM users WHERE username = ? and password = ?", [username, pass_hash])
            userId = cursor.fetchone()
            userId = userId[0]
        # Insert statement to insert a session to the user_session table based on the userId we get above. Commit the changes
        token = secrets.token_urlsafe(40)
        cursor.execute(
            "INSERT INTO user_session (userId, logintoken) VALUES (?, ?)", [userId, token])
        conn.commit()
        # Select statement to grab information about the user, aswell as the just created login token, save data to variable change it to an object and return the data
        cursor.execute(
            "SELECT users.id, email, username, loginToken FROM users inner join user_session on users.id = user_session.userId WHERE users.id = ? and loginToken = ?", [userId, token])
        user = cursor.fetchone()
        if(user == None):
            dbh.db_disconnect(conn, cursor)
            return False
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'loginToken': user[3]
        }
    except db.OperationalError:
        traceback.print_exc()
        print('Something went  wrong with the db!')
    except db.ProgrammingError:
        traceback.print_exc()
        print('Error running DB query')
    except:
        traceback.print_exc()
        print("Something unexpected went wrong")
    dbh.db_disconnect(conn, cursor)
    if(userId == None):
        return False, None
    else:
        return True, user
