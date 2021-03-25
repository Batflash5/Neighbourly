
import pyrebase
from getpass import getpass
from flask import Flask
from flask import request
import os
import math
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
db = firebase.database()
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


@app.route('/viewpost')
def viewpost():
    try:
        lat = request.args.get("lat")
        lon = request.args.get("long")
        x = db.child('post').get().val()
        postNearYou = {}
        for i in x:
            for j in x[i]:
                lat1 = math.radians(float(lat))
                lon1 = math.radians(float(lon))
                lat2 = math.radians(float(x[i][j]['lat']))
                lon2 = math.radians(float(x[i][j]['lon']))
                dlong = lon2-lon1
                dlat = lat2-lat1
                ans = pow(math.sin(dlat/2), 2)+math.cos(lat1) * \
                    math.cos(lat2)*pow(math.sin(dlong), 2)
                ans = 2 * math.asin(math.sqrt(ans))
                ans = ans*6371
                if ans < 15000.0:
                    postNearYou[i] = x[i]
        return postNearYou
    except:
        return 'Error getting posts'


@app.route("/newpost")
def newPost():
    try:
        email = request.args.get("email").split('@')[0]
        title = request.args.get("title")
        description = request.args.get("desc")
        flair = request.args.get("flair")
        lat = request.args.get("lat")
        lon = request.args.get("long")
        # email = 'rahul'
        # title = 'sanju'
        # description = 'safda'
        # flair = 'ffkjg'
        data = {"title": title, "description": description,
                "flair": flair, 'lat': lat, 'lon': lon}
        db.child("post").child(email).push(data)
        return 'uploaded successfully'
    except:
        return 'not able to upload'


@app.route("/currentLocation")
def currentLocation():
    try:
        email = request.args.get("email").split('@')[0]
        lat = request.args.get("lat")
        lon = request.args.get("long")
        data = {'email': email, 'lat': lat, 'long': lon}
        db.child("location").child(email).set(data)
        x = db.child('location').get().val()
        pplNearYou = {}
        for i in x:
            lat1 = math.radians(float(lat))
            lon1 = math.radians(float(lon))
            lat2 = math.radians(float(x[i]['lat']))
            lon2 = math.radians(float(x[i]['long']))
            dlong = lon2-lon1
            dlat = lat2-lat1
            ans = pow(math.sin(dlat/2), 2)+math.cos(lat1) * \
                math.cos(lat2)*pow(math.sin(dlong), 2)
            ans = 2 * math.asin(math.sqrt(ans))
            ans = ans*6371
            if ans < 10.0:
                pplNearYou[i] = x[i]
        return pplNearYou
    except:
        return 'not able to store current location'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
