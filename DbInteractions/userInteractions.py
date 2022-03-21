import mariadb as db
import DbInteractions.dbhandler as dbh
import DbInteractions.userLogin as ul
import traceback

# Function that returns the information about our user


def get_users(userId):
    user = {}
    conn, cursor = dbh.db_connect()
    try:
        cursor.execute(
            "SELECT id, email, username FROM users WHERE id = ?", [userId])
        users = cursor.fetchone()
        users = {
            'userId': users[0],
            'email': users[1],
            'username': users[2]
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
    return True, user

# Function that will change information based on if the values of the arguments are None or not, we check one by one and update one by one, which is less than ideal.


def patch_user(userId, email, username, password, salt):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        if(email != None):
            cursor.execute(
                "UPDATE users SET email = ? WHERE users.id = ?", [email, userId])
            conn.commit()
        if(username != None):
            cursor.execute(
                "UPDATE users SET username = ? WHERE users.id = ?", [username, userId])
            conn.commit()
        if(password != None):
            cursor.execute(
                "UPDATE users SET password = ?, salt = ? WHERE users.ud = ?", [password, salt, userId])
            conn.commit()
        # After all updates and commits are done, a select statement runs to get the information on the newly updated user. Save the data to a variable and change it to an object before disconnecting and returning the data
        cursor.execute(
            "SELECT users.id, email, username FROM users WHERE users.id = ?", [userId])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2]
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
    return True, user

# Function that will create a new user. Takes multiple arguments.


def post_user(email, username, pass_hash, salt):
    user = []
    conn, cursor = dbh.db_connect()
    try:
        # Inserting a new user into the DB with the values from the arguments and then commit
        cursor.execute(
            "INSERT INTO users (email, username, password, salt) VALUES (?, ?, ?, ?)", [email, username, pass_hash, salt])
        conn.commit()
        # After creating the user in the DB, we pass in information to the user login endpoint to also log the user in after creation, creating a login token.
        user = ul.post_login(email, None, pass_hash)
        # Saving the login token to a variable
        login_token = user[1]['loginToken']
        # Run a select statement to get data on the newly created user, save it to a variable and then change to an object, with the logintoken aswell. before disconnecting and returning the data
        cursor.execute(
            "SELECT users.id, email, username FROM users WHERE username = ?", [username])
        user = cursor.fetchone()
        user = {
            'userId': user[0],
            'email': user[1],
            'username': user[2],
            'loginToken': login_token
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
    # If user is empty, something went wrong. If not return the user.
    if(user == []):
        return False, None
    else:
        return True, user

# Function that will delete a user. Takes in login token and hashed password as arguments NOT USED AT THE MOMENT


def delete_user(loginToken, pass_hash):
    conn, cursor = dbh.db_connect()
    try:
        # Delete statement that deletes a user from the DB if login token and password are valid(password is correct and user is logged in). Commit, disconnect and return true to validate success
        cursor.execute(
            "DELETE users FROM users inner join user_session on users.id = user_session.userId WHERE password = ? and logintoken = ? ", [pass_hash, loginToken])
        conn.commit()
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
    return True
