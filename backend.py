
import pyrebase
from getpass import getpass
from flask import Flask
from flask import request
import os
app = Flask(__name__)


firebaseConfig = {"apiKey": "AIzaSyArqx_yIgbUwCSlJCWUgmKtkP1d1YP-YNM",
                  "authDomain": "neighbourly-5369a.firebaseapp.com",
                  "projectId": "neighbourly-5369a",
                  "storageBucket": "neighbourly-5369a.appspot.com",
                  "messagingSenderId": "147725957925",
                  "appId": "1:147725957925:web:053fc885c4a4ca7ca7b8cc",
                  "measurementId": "G-KTYZMRV4WQ",
                  "databaseURL": "https://neighbourly-5369a-default-rtdb.firebaseio.com/"}
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
# pip uninstall crypto
# pip uninstall pycryptodome
# pip install pycryptodome


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/signup")
def signup():
    email = request.args.get("email")
    password = request.args.get("password")
    # email = 'rahulbulls12@gmail.com'
    # password = 'rahul2000'
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])
        return auth.get_account_info(user['idToken'])
    except:
        return 'Invalid email id or email id already exists'
# auth.get_account_info(user['idToken'])


@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        info = auth.get_account_info(user['idToken'])
        if info['users'][0]['emailVerified'] == False:
            return 'User still not verified'
        else:
            return info
    except:
        return 'No user found'


@app.route("/reverify")
def resend_verify():
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user = auth.refresh(user['refreshToken'])
        auth.send_email_verification(user['idToken'])
        return 'Verification sent to mail'
    except:
        return 'unable to send verification'

    # if info["users"]["emailVerified"] == False:
    #     return 'verified'
    # else:
    #     return 'not verified'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
