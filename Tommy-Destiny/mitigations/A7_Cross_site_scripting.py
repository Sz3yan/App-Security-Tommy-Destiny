from flask_csp.csp import csp_header
# <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src https://images.unsplash.com;">
# @csp_header(CspClass().return_csp_header())
class CspClass:
    def __init__(self):
        self.__default_src = ""
        self.__script_src = ""
        self.__img_src = ""
        self.__script_src = ""

    def return_csp_header(self):
        return {'default-src':"'self'"}



    