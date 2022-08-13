import sentry_sdk

from flask import Flask
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
# talisman = Talisman(app, force_https=True, content_security_policy=CspClass().return_csp_header("homeage"))  # enables HSTS
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


if __name__ == "__main__":
    app.run()