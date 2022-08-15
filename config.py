from datetime import timedelta


class Config(object):
    """Base Flask configuration"""
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_THRESHOLD = 100
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = '6LdPSO8gAAAAADq9_WWZcX7MhXkx8J4ceGFynwWp'
    RECAPTCHA_PRIVATE_KEY = '6LdPSO8gAAAAAFVKTV67Tchj8hwjQi0P6QKFOKsx'
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
