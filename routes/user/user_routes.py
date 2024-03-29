import json

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_jwt_extended import create_access_token
from ..api.api_routes import user_info
from static.firebaseConnection import FirebaseClass, FirebaseAdminClass
from routes.user.static.py.Forms import CreateUser, LoginUser, TwoFactorAuth, EnterOTP
from routes.admin.static.py.Post import Post
from mitigations.A3_Sensitive_data_exposure import AES_GCM, GoogleCloudKeyManagement, GoogleSecretManager
from mitigations.API10_Insufficient_logging_and_monitoring import GoogleCloudLogging
from mitigations.A2_Broken_authentication import getOTPTwilio


user = Blueprint('user', __name__, template_folder="templates", static_folder='static')

write_logs = GoogleCloudLogging()
googlesecretmanager = GoogleSecretManager()
keymanagement = GoogleCloudKeyManagement()

secret_key_post = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", googlesecretmanager.get_secret_payload("tommy-destiny", "hsm_tommy", "1")))
secret_key_page = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", googlesecretmanager.get_secret_payload("tommy-destiny", "hsm_tommy1", "1")))

recapcha_public_key = googlesecretmanager.get_secret_payload("tommy-destiny", "recaptcha-public-key", "1")


@user.route("/")
def index():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        write_logs.write_entry_info("User home: retrieved posts")
    except:
        posts = []
        write_logs.write_entry_exception("User home: no posts found")

    return render_template('home.html', posts=posts)


@user.route("/login", methods=["POST", "GET"])
def login():
    write_logs.write_entry_info("User login: access login page")

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
                write_logs.write_entry_info("User login: login successful, session created")
                return redirect(url_for("user.profile")) #redirect(url_for("user.2FA"))
            else:
                write_logs.write_entry_warning("User login: login failed")
                return render_template('login.html', form=loginUser, message=str(firebase.login_user(email, password)))

    return render_template('login.html', form=loginUser, message="", recapcha_public_key=recapcha_public_key)

@user.route('/2FA', methods=["POST", "GET"])
def twoFactorAuth():
    twoFactorAuth = TwoFactorAuth(request.form)
    if request.method == "POST" and twoFactorAuth.validate():
        phno = twoFactorAuth.phno.data

    else:
        return render_template('2FA.html', form=twoFactorAuth)
    return render_template('2FA.html', form=twoFactorAuth)


@user.route('/enterOTP', methods=["POST", "GET"])
def enterOTP():
    enterOTP = EnterOTP(request.form)
    fba = FirebaseAdminClass()
    user_ID = session["userID"]
    userInfo = fba.fa_get_user(user_ID)
    phno = userInfo["UI2"][user_ID]["Phone number"]
    num = getOTPTwilio(phno)
    if request.method == "POST" and enterOTP.validate():
        otp = enterOTP.otp.data
        if num != "" and otp == num:
            
            return redirect(url_for("user.enterOTP"))
        #else:
            #return render_template('enterOTP.html', form=enterOTP, message="Invalid OTP")
    return render_template('enterOTP.html', form=enterOTP)
    


@user.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('userID', None)

    write_logs.write_entry_info("User logout: logout successful, session removed")
    return redirect(url_for('user.index'))


@user.route('/profile')
def profile():
    
    fa = FirebaseClass()
    if 'userID' in session:
        # this will not hve any id
        user_ID = session["userID"]
        print(user_ID)
        
        userInfo = fa.get_user_info(user_ID)
        print(userInfo)
        return render_template('profile.html', userinfo=userInfo)
    else:
        return redirect(url_for('user.index'))


@user.route("/signup", methods=["POST", "GET"])
def signup():
    write_logs.write_entry_info("User signup: access signup page")

    firebase = FirebaseClass()
    createUser = CreateUser(request.form)
    if request.method == 'POST' and createUser.validate():
        username = createUser.name.data
        email = createUser.email.data
        phno = createUser.phno.data
        password = createUser.register_password.data

        if not firebase.create_user(email, password):
            firebase.create_user_info(username, phno, "customer")
            write_logs.write_entry_info("User signup: signup successful, user created")
            return redirect(url_for("user.login"))
        else:
            write_logs.write_entry_warning("User signup: signup failed")
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

                decrypted = aes_gcm.decrypt(secret_key_post, plaintext)
                write_logs.write_entry_info(f"User post: decrypted post {id} with hsm_tommy key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        write_logs.write_entry_exception("User post: No posts found")
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

                decrypted = aes_gcm.decrypt(secret_key_post, plaintext)
                write_logs.write_entry_info(f"User post: decrypted post {id} with hsm_tommy key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        write_logs.write_entry_exception("User post: No posts found")
        return redirect(url_for("user.index"))

    return render_template('post.html', id=id, data=data, title=title, date=date)


@user.route("/pricing")
def pricing():
    return render_template("pricing.html")
    

@user.route("/about")
def about():
    data = [{
        "type": "header",
        "data": {
            "text": "Page title",
        }
    }]

    try:
        aes_gcm = AES_GCM()
        firebase = FirebaseClass()

        for i in firebase.get_page().each():
            if i.val()["_Page__id"] == "96e4d495-29bb-414a-a4ab-adb0a65debc8":
                plaintext = i.val()["_Page__plaintext"]

                decrypted = aes_gcm.decrypt(secret_key_page, plaintext)
                write_logs.write_entry_info(f"User post: decrypted About page with hsm_tommy1 key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        write_logs.write_entry_exception("User about: no page found")
        return redirect(url_for("user.index"))

    return render_template("about.html", data=data)


@user.route("/allposts")
def allposts():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        write_logs.write_entry_info("User allposts: retrieved posts")
    except:
        posts = []
        write_logs.write_entry_exception("User allposts: no posts found")

    return render_template("allposts.html", posts=posts)


@user.route("/privacy-policy")
def policy():
    data = [{
        "type": "header",
        "data": {
            "text": "Page title",
        }
    }]

    try:
        aes_gcm = AES_GCM()
        firebase = FirebaseClass()

        for i in firebase.get_page().each():
            if i.val()["_Page__id"] == "70006058-1f60-4824-b77a-b63bc22342c1":
                plaintext = i.val()["_Page__plaintext"]

                decrypted = aes_gcm.decrypt(secret_key_page, plaintext)
                write_logs.write_entry_info(f"User post: decrypted Privacy-Policy page with hsm_tommy1 key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        write_logs.write_entry_exception("User about: no page found")
        return redirect(url_for("user.index"))

    return render_template("policy.html", data=data)
