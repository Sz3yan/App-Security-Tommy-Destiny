import sentry_sdk

from flask import Flask, jsonify, request, session, g
from config import DevConfig, ProdConfig
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

from routes.api.api_routes import api
from routes.admin.admin_routes import admin
from routes.user.user_routes import user
from routes.errors.error_routes import errors
from static.firebaseConnection import FirebaseClass

from mitigations.A7_Cross_site_scripting import CspClass


load_dotenv()


sentry_sdk.init(
    dsn="https://585c1767c8c84a8ab976b3af393fa29d@o1323719.ingest.sentry.io/6645595",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_object(DevConfig())


jwt = JWTManager(app)
csrf = CSRFProtect(app)
sess = Session(app)


"""
    https://cdn.tailwindcss.com

    "https://source.unsplash.com/random",
    "https://source.unsplash.com/xfngap_DToE",
    "https://source.unsplash.com/i1TP8hZX8c4",
    "https://source.unsplash.com/Bt_J-VvC9-A",
    "https://source.unsplash.com/JBghIzjbuLs",
    "https://source.unsplash.com/b2qszO9C7sw"

    "https://cdn.jsdelivr.net/npm/codex.editor.header@2.0.4/dist/bundle.js",
    "https://cdn.jsdelivr.net/npm/@editorjs/header@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/simple-image@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/delimiter@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/list@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/checklist@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/quote@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/code@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/embed@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/table@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/link@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/warning@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/image@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/marker@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/inline-code@latest",
    "https://cdn.jsdelivr.net/npm/@editorjs/editorjs@latest"
"""

talisman = Talisman(app, 
    force_https=False, 
    force_https_permanent=True,
    content_security_policy=False, # for now
    # content_security_policy=CSP,
    # content_security_policy_nonce_in=["script-src"],
    strict_transport_security=True,
    strict_transport_security_preload=True,
    strict_transport_security_max_age=31536000, 
    strict_transport_security_include_subdomains=True,
)

limiter = Limiter(app, 
    key_func=get_remote_address, 
    default_limits=["75 per second"]
)


app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(errors)

csrf.exempt(api)

# prevent caching
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
def api_error(errorCode):
    if request.path.startswith('/api'):
        return jsonify(error=str(errorCode)), errorCode.code



@app.before_request
def before_request():
    if 'userID' in session:
        firebase = FirebaseClass() # this will not hve any id
        user_ID = session["userID"]

        userInfo = firebase.get_user_info(user_ID)
        g.current_user = userInfo


if __name__ == "__main__":
    app.run()