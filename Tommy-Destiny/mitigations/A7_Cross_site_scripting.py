from flask_csp.csp import csp_header
from static.py.firebaseConnection import FirebaseClass
# <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src https://images.unsplash.com;">
# @csp_header(CspClass().return_csp_header())
class CspClass:
    def __init__(self):
        self.__firebaseDb = FirebaseClass()
        self.__default_src = ""
        self.__script_src = ""
        self.__script_src_elem = ""
        self.__script_src_attr = ""
        self.__img_src = ""
        self.__style_src = ""
        self.__style_src_elem = ""
        self.__style_src_attr = ""

    def create_policy(self):
        pass

    def return_csp_header(self):
        return {'default-src':"'self'"}



    