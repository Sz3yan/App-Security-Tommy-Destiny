from flask import Blueprint, render_template, request, session, redirect, url_for
from web.user.static.py.Forms import CreateUser, LoginUser
from mitigations.A3_Sensitive_data_exposure import Secure
from static.py.firebaseConnection import FirebaseClass

user = Blueprint('user', __name__, template_folder="templates", static_folder='static')

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
    if "customer_session" in session:
        return redirect(url_for('customer_logged_in'))
    else:
        if request.method == "POST" and loginUser.validate():
            username = loginUser.name.data
            email = loginUser.email.data
            password = loginUser.password.data
            if firebase.login_user(email, password):
                return render_template('login.html', form=loginUser, message=str(firebase.login_user(email, password))) #If user not inside
    return render_template('login.html', form=loginUser, message="")


@user.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('home'))


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
        firebase.create_user(email, password)
        firebase.create_user_info(username, phno, "customer")
    return render_template('signup.html', form=createUser)
