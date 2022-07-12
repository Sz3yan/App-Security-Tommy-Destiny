from flask import Blueprint, render_template, request
from web.user.static.py.Forms import CreateUser
from mitigations.A3_Sensitive_data_exposure import Secure
from static.py.firebaseConnection import FirebaseClass

user = Blueprint('user', __name__, template_folder="templates", static_folder='static')

@user.route("/")
def index():
    return render_template('home.html')


@user.route("/pricing")
def pricing():
    return render_template("pricing.html")


@user.route("/login")
def login():
    return render_template('login.html')


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