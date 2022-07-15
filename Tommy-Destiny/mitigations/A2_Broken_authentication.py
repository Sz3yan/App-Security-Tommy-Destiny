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
    detail_dict = firebase.get_user_info()
    if 'userID' in session:
        user = [x for x in detail_dict if x.userID == session["userID"]][0]
        g.user = user

