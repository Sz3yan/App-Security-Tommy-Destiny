import os
import sentry_sdk

from flask import Flask, jsonify, request, session, g
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from config import DevConfig, ProdConfig
from static.firebaseConnection import FirebaseClass
from routes.api.api_routes import api
from routes.admin.admin_routes import admin
from routes.user.user_routes import user
from routes.errors.error_routes import errors
from static.firebaseConnection import FirebaseClass, FirebaseAdminClass
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn="https://585c1767c8c84a8ab976b3af393fa29d@o1323719.ingest.sentry.io/6645595",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_object(ProdConfig())


jwt = JWTManager(app)
csrf = CSRFProtect(app)
sess = Session(app)

talisman = Talisman(app, 
    force_https=False, 
    force_https_permanent=True,
    content_security_policy=FirebaseAdminClass().fa_get_csp()["homepage"], # for now
    strict_transport_security=True,
    strict_transport_security_preload=True,
    strict_transport_security_max_age=31536000, 
    strict_transport_security_include_subdomains=True,
)

limiter = Limiter(app, 
    key_func=get_remote_address, 
    default_limits=["50 per second"]
)


app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(errors)


csrf.exempt(api)


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(413)
@app.errorhandler(429)
@app.errorhandler(500)
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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))