from flask_rbac import UserMixin, RoleMixin
from static.py.firebaseConnection import FirebaseClass

class User(UserMixin):
    pass

class Role(RoleMixin):
    pass
