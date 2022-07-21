from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mailman import Mail
from flask_session import Session
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from api.routes import api
from web.admin.admin_routes import admin
from web.user.user_routes import user
from dotenv import load_dotenv
from datetime import timedelta
import os


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

app.config["RECAPTCHA_USE_SSL"] = False
app.config["RECAPTCHA_PUBLIC_KEY"] = '6LdPSO8gAAAAADq9_WWZcX7MhXkx8J4ceGFynwWp'
app.config["RECAPTCHA_PRIVATE_KEY"] = '6LdPSO8gAAAAAFVKTV67Tchj8hwjQi0P6QKFOKsx'
app.config["RECAPTCHA_OPTIONS"] = {'theme' : 'white'}

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER_IMAGE"] = "static/image"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ("png", "jpg", "jpeg")
app.config["UPLOAD_FOLDER_VIDEO"] = "static/videos"
app.config["ALLOWED_VIDEO_EXTENSIONS"] = (".mp4, .mov, .avi, .mpeg4, .webm, .mpegs, .wmv")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "sz3yan@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("EMAIL_PASS")

app.config["DEBUG"] = True


mail = Mail(app)
jwt = JWTManager(app)
csrf = CSRFProtect(app)
sess = Session(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["50 per second"])


app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)


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
    app.run()