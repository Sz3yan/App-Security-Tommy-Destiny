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

from routes.api.api_routes import api
from routes.admin.admin_routes import admin
from routes.user.user_routes import user
from routes.errors.error_routes import errors

from mitigations.A7_Cross_site_scripting import CspClass

load_dotenv()


app = Flask(__name__)
app.config.from_object('config.DevConfig')

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/sz3yan/Tommy-Destiny/google.json" # for key management system
# if cannot run, do this: export GOOGLE_APPLICATION_CREDENTIALS="./Tommy-Destiny/google.json"
# then python __init__.py

# CspClass().return_csp_header("homeage")

mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
sess = Session(app)
talisman = Talisman(app, force_https=True, content_security_policy=CspClass().return_csp_header("homeage"))  # enables HSTS
limiter = Limiter(app, key_func=get_remote_address, default_limits=["50 per second"])


app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(errors)


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


certpem = os.path.join(app.root_path, 'cert.pem')
keypem = os.path.join(app.root_path, 'key.pem')


if __name__ == '__main__':
    app.run(ssl_context=(certpem, keypem))
