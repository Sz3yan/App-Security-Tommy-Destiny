from uuid import uuid4
from datetime import datetime

class Post:
    def __init__(self, title):
        self.__id = str(uuid4())
        self.__title = title
        self.__plaintext = ""
        self.__featured = 0
        self.__status = "Draft"
        self.__visibility = 0
        self.__created_at = str(datetime.now())
        self.__updated_at = str(datetime.now())
        self.__published_at = str(datetime.now())
        self.__iv = ""
        self.__key = ""

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        self.__title = title

    def get_plaintext(self):
        return self.__plaintext

    def set_plaintext(self, plaintext):
        self.__plaintext = plaintext

    def get_featured(self):
        return self.__featured

    def set_featured(self, featured):
        self.__featured = featured

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def get_visibility(self):
        return self.__visibility

    def set_visibility(self, visibility):
        self.__visibility = visibility

    def get_created_at(self):
        return self.__created_at

    def set_created_at(self):
        self.__created_at = datetime.now()

    def get_updated_at(self):
        return self.__updated_at

    def set_updated_at(self):
        self.__updated_at = datetime.now()

    def get_published_at(self):
        return self.__published_at

    def set_published_at(self):
        self.__published_at = datetime.now()

    def get_iv(self):
        return self.__iv

    def set_iv(self, iv):
        self.__iv = iv

    def get_key(self):
        return self.__key

    def set_key(self, key):
        self.__key = key

    def __str__(self):
        return f"{self.__id}\n {self.__title}\n {self.__plaintext}\n {self.__featured}\n {self.__status}\n {self.__visibility}\n {self.__created_at}\n {self.__updated_at}\n {self.__published_at}\n {self.__iv}\n {self.__key}"


from wtforms import Form, HiddenField

class SubmitPostForm(Form):
    content = HiddenField()