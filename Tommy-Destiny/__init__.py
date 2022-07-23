import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mailman import Mail
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

from api.routes import api
from web.admin.admin_routes import admin
from web.user.user_routes import user

load_dotenv()

app = Flask(__name__)
app.config.from_object('config.DevConfig')

mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
sess = Session(app)
talisman = Talisman(app, force_https=True, content_security_policy=False) # enables HSTS
limiter = Limiter(app, key_func=get_remote_address, default_limits=["50 per second"])


app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)


# prevent caching
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


# @app.before_request
# def before_request():
#     firebase = FirebaseClass()
#     user_ID = firebase.get_user(userID)
#     userInfo = firebase.get_user_info(user_ID)
#     if 'userID' in session:
#         if user_ID == session['userID']:
#             g.current_user = userInfo
#         else:
#             return redirect(url_for(user.index))


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))
