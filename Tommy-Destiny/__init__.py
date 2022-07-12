from flask import Flask
from api.routes import api
from web.admin.admin_routes import admin
from web.user.user_routes import user


app = Flask(__name__)
app.debug = True

app.register_blueprint(api)
app.register_blueprint(admin)
app.register_blueprint(user)


if __name__ == '__main__':
    app.run()
