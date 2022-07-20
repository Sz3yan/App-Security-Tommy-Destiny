from argon2 import hash_password
from argon2 import hash_password
from flask import Blueprint, render_template, request, session, redirect, url_for, g, current_app, Flask
from web.user.static.py.Forms import CreateUser, LoginUser
from base64 import b64decode
from mitigations.A3_Sensitive_data_exposure import AES_GCM, PBKDF2_SHA256
from static.py.firebaseConnection import FirebaseClass
import json

user = Blueprint('user', __name__, template_folder="templates", static_folder='static')


@user.route("/")
def index():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
    except:
        posts = []
        print("No posts found")

    return render_template('home.html', posts=posts)


@user.route("/pricing")
def pricing():
    return render_template("pricing.html")


@user.route("/login", methods=["POST", "GET"])
def login():
    firebase = FirebaseClass()
    loginUser = LoginUser(request.form)
    if "userID" in session:
        return redirect(url_for('user.profile'))
    else:

        if request.method == "POST" and loginUser.validate():
            session.pop('userID', None) #auto remove session when trying to login
            email = loginUser.email.data
            password = loginUser.password.data

            if not firebase.login_user(email, password):
                userID = firebase.get_user()
                session['userID'] = userID
                return redirect(url_for("user.profile"))
            else:
                return render_template('login.html', form=loginUser, message=str(firebase.login_user(email, password)))

    return render_template('login.html', form=loginUser, message="")


@user.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('userID', None)
   return redirect(url_for('user.index'))


@user.route('/profile')
def profile():

    if 'userID' in session:
        firebase = FirebaseClass() # this will not hve any id
        user_ID = session["userID"]
        print(user_ID)

        userInfo = firebase.get_user_info(user_ID)
        g.current_user = userInfo
        return render_template('profile.html')
    else:
        return redirect(url_for('user.index'))



@user.route("/payment")
def payment():
    return render_template("payment.html")


@user.route("/signup", methods=["POST", "GET"])
def signup():
    firebase = FirebaseClass()
    createUser = CreateUser(request.form)
    if request.method == 'POST' and createUser.validate():
        username = createUser.name.data
        email = createUser.email.data
        phno = createUser.phno.data
        password = createUser.register_password.data

        if not firebase.create_user(email, password):
            firebase.create_user_info(username, phno, "customer")
        else:
            return render_template('signup.html', form=createUser, message=str(firebase.create_user(email, password)))
    return render_template('signup.html', form=createUser)


@user.route("/post/<id>")
def post(id):
    aes_gcm = AES_GCM()
    secret_key = "yourSecretKey"

    data = [{
        "type" : "header",
        "data" : {
            "text" : "Post title",
        }
    }]

    try:
        pull_post = FirebaseClass()

        for i in pull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                plaintext = i.val()["_Post__plaintext"]

                decrypted = aes_gcm.decrypt(secret_key, plaintext)
                print("decrypted: ", decrypted)

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
                # print(data)
            else: 
                data = data
    except:
        print("No posts found")
        return redirect(url_for("home"))

    return render_template('post.html', id=id, data=data)