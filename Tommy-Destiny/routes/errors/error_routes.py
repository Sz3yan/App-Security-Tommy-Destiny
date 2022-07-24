from flask import Blueprint
from flask import render_template, current_app
from jinja2 import UndefinedError

errors = Blueprint('error', __name__, template_folder='templates')


@errors.app_errorhandler(400)
def handle_400(err):
    error_message = "Bad Request. The request was malformed and could not be parsed."
    return render_template('error.html', error_number="400", error_message=error_message)


@errors.app_errorhandler(401)
def handle_401(err):
    error_message = "This error happens when a website visitor tries to access a restricted web page but isn’t " \
                    "authorized to do so, usually because of a failed login attempt. "
    return render_template('error.html', error_number="401", error_message=error_message)


@errors.app_errorhandler(403)
def handle_400(err):
    error_message = "Access Denied. Access token was missing, invalid, or does not have the necessary permissions."
    return render_template('error.html', error_number="400", error_message=error_message)


@errors.app_errorhandler(404)
def handle_404(err):
    error_message = "This page doesn't exist. Check what was typed in the address bar."
    return render_template('error.html', error_number="404", error_message=error_message)


@errors.app_errorhandler(413)
def handle_404(err):
    error_message = "Request entity too large. The request exceeded the maximum size"
    return render_template('error.html', error_number="404", error_message=error_message)


@errors.app_errorhandler(429)
def handle_404(err):
    error_message = "Too Many Requests"
    return render_template('error.html', error_number="404", error_message=error_message)


@errors.app_errorhandler(500)
def handle_500(err):
    error_message = f"Something wrong with website. Either try again or send email to {current_app.config['MAIL_USERNAME']}"
    return render_template('error.html', error_number="500", error_message=error_message)


@errors.app_errorhandler(UndefinedError)
def handle_undefined_error(err):
    error_message = "check variable"
    return render_template('error.html', error_number="500", error_message=error_message)