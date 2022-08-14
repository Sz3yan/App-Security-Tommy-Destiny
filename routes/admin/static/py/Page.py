from uuid import uuid4
from datetime import datetime

class Page:
    def __init__(self, title):
        self.__id = str(uuid4())
        self.__title = title
        self.__plaintext = ""
        self.__created_at = str(datetime.now())
        self.__updated_at = str(datetime.now())
        self.__published_at = str(datetime.now())

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

    def __str__(self):
        return f"Page id: {self.get_id()}, title: {self.get_title()}, plaintext: {self.get_plaintext()}, created_at: {self.get_created_at()}, updated_at: {self.get_updated_at()}, published_at: {self.get_published_at()}"