from datetime import timedelta
from mitigations.A3_Sensitive_data_exposure import GoogleSecretManager


class Config(object):
    """Base Flask configuration"""
    SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
    JWT_SECRET_KEY = 'VG9tbXlEZXN0aW55and0c2VjcmV0a2V5c2VjdXJldmVyaWZpY2F0aW9u'
    secretkeymanager = GoogleSecretManager()
    SECRET_KEY = secretkeymanager.get_secret_payload("tommy-destiny", "flask-secret-key", "1")
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_THRESHOLD = 100
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = secretkeymanager.get_secret_payload("tommy-destiny", "recaptcha-public-key", "1")
    RECAPTCHA_PRIVATE_KEY = secretkeymanager.get_secret_payload("tommy-destiny", "recaptcha-private-key", "1")
    RECAPTCHA_OPTIONS = {'theme': 'white'}


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
