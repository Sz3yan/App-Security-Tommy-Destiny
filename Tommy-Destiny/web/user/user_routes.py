from argon2 import hash_password
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from web.user.static.py.Forms import CreateUser, LoginUser
from mitigations.A2_Broken_authentication import *
from mitigations.A3_Sensitive_data_exposure import Argon2
from static.py.firebaseConnection import FirebaseClass
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

user = Blueprint('user', __name__, template_folder="templates", static_folder='static')

# jwt = JWTManager(app)  

@user.route("/")
def index():
    return render_template('home.html')


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
        # if request.is_json:
        #     username = request.json["name"]

        ph = Argon2()

        if request.method == "POST" and loginUser.validate():
            session.pop('userID', None) #auto remove session when trying to login
            # hash = ph.get_hash()

            email = loginUser.email.data
            password = loginUser.password.data

            # ph.verify(hash, password)

            # if ph.check_needs_rehash(hash):
            #     db.set_password_hash_for_user(user, ph.hash(password))

            #username = loginUser.name.data
            if not firebase.login_user(email, password):
                userID = firebase.get_user()
                session['userID'] = userID
                return redirect(url_for("user.profile"))
            else:                                           #If user not inside
                return render_template('login.html', form=loginUser, message=str(firebase.login_user(email, password)))

    return render_template('login.html', form=loginUser, message="")


@user.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('userID', None)
   return redirect(url_for('user.index'))


@user.route('/profile')
def profile():
    if "userID" not in session: #actually i wanna use g.user but idk how to link it to init.py
        return redirect(url_for("user.login"))
    return render_template('profile.html')


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

        # hashing = Argon2()
        # hash_password = hashing.hash(password)
        # hash_phno = hashing.hash(phno)
        # print(f"hashed password: {hash_password}","\n",f"hashed phno: {hash_phno}")       

        firebase.create_user(email, password)
        firebase.create_user_info(username, phno, "customer")
    return render_template('signup.html', form=createUser)
