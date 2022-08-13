import json

from datetime import datetime

from flask import Blueprint, render_template, request, session, redirect, url_for
from mitigations.A3_Sensitive_data_exposure import AES_GCM, GoogleCloudKeyManagement
from mitigations.API10_Insufficient_logging_and_monitoring import User_Logger
from static.firebaseConnection import FirebaseClass, FirebaseAdminClass
from routes.user.static.py.Forms import CreateUser, LoginUser
from routes.admin.static.py.Post import Post

user = Blueprint('user', __name__, template_folder="templates", static_folder='static')
User_Logger = User_Logger()
keymanagement = GoogleCloudKeyManagement()
secret_key = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", "key_id"))


@user.route("/")
def index():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        User_Logger.log_info("User home: retrieved posts")
    except:
        posts = []
        User_Logger.log_exception("User home: no posts found")

    return render_template('home.html', posts=posts)


@user.route("/pricing")
def pricing():
    return render_template("pricing.html")


@user.route("/login", methods=["POST", "GET"])
def login():
    User_Logger.log_info("User login: access login page")

    firebase = FirebaseClass()
    loginUser = LoginUser(request.form)
    if "userID" in session:
        return redirect(url_for('user.profile'))
    else:
        if request.method == "POST" and loginUser.validate():
            session.pop('userID', None)  # auto remove session when trying to login
            email = loginUser.email.data
            password = loginUser.password.data

            if not firebase.login_user(email, password):
                userID = firebase.get_user()
                session['userID'] = userID
                User_Logger.log_info("User login: login successful, session created")
                return redirect(url_for("user.profile"))
            else:
                User_Logger.log_warning("User login: login failed")
                return render_template('login.html', form=loginUser, message=str(firebase.login_user(email, password)))

    return render_template('login.html', form=loginUser, message="")


@user.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('userID', None)

    User_Logger.log_info("User logout: logout successful, session removed")
    return redirect(url_for('user.index'))


@user.route('/profile')
def profile():
    
    fa = FirebaseAdminClass()
    if 'userID' in session:
        # this will not hve any id
        user_ID = session["userID"]
        print(user_ID)
        
        userInfo = fa.get_user(user_ID)
        print(userInfo)
        
        userInfo = fa.get_user(user_ID)
        print(userInfo)
        return render_template('profile.html')
    else:
        return redirect(url_for('user.index'))


@user.route("/payment")
def payment():
    return render_template("payment.html")


@user.route("/signup", methods=["POST", "GET"])
def signup():
    User_Logger.log_info("User signup: access signup page")

    firebase = FirebaseClass()
    createUser = CreateUser(request.form)
    if request.method == 'POST' and createUser.validate():
        username = createUser.name.data
        email = createUser.email.data
        phno = createUser.phno.data
        password = createUser.register_password.data

        if not firebase.create_user(email, password):
            firebase.create_user_info(username, phno, "customer")
            User_Logger.log_info("User signup: signup successful, user created")
        else:
            User_Logger.log_warning("User signup: signup failed")
            return render_template('signup.html', form=createUser, message=str(firebase.create_user(email, password)))
    return render_template('signup.html', form=createUser)


@user.route("/top4post/<id>")
def top4post(id):
    newPost = Post("title")
    newPost.set_id(id)
    aes_gcm = AES_GCM()

    data = [{
        "type": "header",
        "data": {
            "text": "Post title",
        }
    }]

    try:
        pull_post = FirebaseClass()

        for i in pull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                plaintext = i.val()["_Post__plaintext"]
                title = i.val()["_Post__title"]
                date = i.val()["_Post__published_at"]

                decrypted = aes_gcm.decrypt(secret_key, plaintext)
                User_Logger.log_info(f"User post: decrypted post {id}")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        User_Logger.log_exception("User post: No posts found")
        return redirect(url_for("user.index"))

    return render_template('top4post.html', id=id, data=data, title=title, date=date)


@user.route("/post/<id>")
def post(id):
    newPost = Post("title")
    newPost.set_id(id)
    aes_gcm = AES_GCM()

    data = [{
        "type": "header",
        "data": {
            "text": "Post title",
        }
    }]

    try:
        pull_post = FirebaseClass()

        for i in pull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                plaintext = i.val()["_Post__plaintext"]
                title = i.val()["_Post__title"]
                date = i.val()["_Post__published_at"]

                decrypted = aes_gcm.decrypt(secret_key, plaintext)
                User_Logger.log_info(f"User post: decrypted post {id}")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        User_Logger.log_exception("User post: No posts found")
        return redirect(url_for("user.index"))

    return render_template('post.html', id=id, data=data, title=title, date=date)


@user.route("/about")
def about():
    return render_template("about.html")


@user.route("/allposts")
def allposts():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        User_Logger.log_info("User allposts: retrieved posts")
    except:
        posts = []
        User_Logger.log_exception("User allposts: no posts found")

    return render_template("allposts.html", posts=posts)


@user.route("/privacy-policy")
def policy():
    return render_template("policy.html")
