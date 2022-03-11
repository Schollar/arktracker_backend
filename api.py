from flask import Flask, request, Response
import Endpoints.users as users
import Endpoints.login as login
import Endpoints.characters as characters
import DbInteractions.dbhandler as dbh


import sys
app = Flask(__name__)

# ENDPOINT README###$
# These endpoint all create a function, which returns the
# information from the actual function that is imported and called from another file.
# All endpoints are split up into their own respective files for organizational sake.


@app.before_request
def validate_token():
    if(request.method.lower() == 'options'):
        return
    if(request.endpoint in app.view_functions):
        if(hasattr(app.view_functions[request.endpoint], 'must_authenticate')):
            success = dbh.validate_login_token(
                request.cookies.get('logintoken'))
            if(success == False):
                return Response('Invalid Login Token', mimetype="plain/text", status=403)


def authenticate(endpoint):
    endpoint.must_authenticate = True
    return endpoint

## USER ENDPOINT ##


@app.post('/api/users')
def post_user():
    return users.post()


@app.get('/api/users')
@authenticate
def get_users():
    return users.get()


@app.patch('/api/users')
@authenticate
def patch_users():
    return users.patch()


@app.delete('/api/users')
@authenticate
def delete_user():
    return users.delete()


######## LOGIN ENDPOINT #######


@app.delete('/api/login')
@authenticate
def delete_login():
    return login.delete()


@app.post('/api/login')
def post_login():
    return login.post()
######## CHARACTER ENDPOINT #######


@app.get('/api/characters')
@authenticate
def get_chars():
    return characters.get()


# Checking to see if a mode was passed to the script
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print('You must pass a mode to run this script. Either testing or production')
    exit()
# Depending on what mode is passed, we check and run the appropriate code.
if(mode == "testing"):
    print('Running in testing mode!')
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
elif(mode == "production"):
    print('Running in production mode')
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5006)
else:
    print('Please Run in either testing or production')
