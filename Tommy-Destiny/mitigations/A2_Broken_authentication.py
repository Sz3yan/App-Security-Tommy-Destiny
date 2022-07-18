from flask import Flask, session, g
from flask_session import Session
from datetime import timedelta
from static.py.firebaseConnection import FirebaseClass


app = Flask(__name__)

#session
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

sess = Session()
sess.init_app(app)

@app.before_request
def before_request():
    firebase = FirebaseClass()
    userInfo = firebase.get_user_info()
    userID = firebase.get_user()
    if 'userID' in session:
        if userID == session['userID']:
            g.user = userInfo
        else:
            g.user = "Hi"

