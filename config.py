"""Flask configuration."""

import os
from datetime import timedelta
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Base config."""
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    SESSION_PERMANENT = True
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_THRESHOLD = 100
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LdPSO8gAAAAADq9_WWZcX7MhXkx8J4ceGFynwWp'
    RECAPTCHA_PRIVATE_KEY = '6LdPSO8gAAAAAFVKTV67Tchj8hwjQi0P6QKFOKsx'
    RECAPTCHA_OPTIONS = {'theme': 'white'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER_IMAGE = "static/image"
    ALLOWED_IMAGE_EXTENSIONS = ("png", "jpg", "jpeg")
    UPLOAD_FOLDER_VIDEO = "static/videos"
    ALLOWED_VIDEO_EXTENSIONS = ".mp4, .mov, .avi, .mpeg4, .webm, .mpegs, .wmv"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "sz3yan@gmail.com"
    MAIL_PASSWORD = os.getenv("EMAIL_PASS")


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
