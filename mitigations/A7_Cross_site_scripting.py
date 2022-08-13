from multiprocessing import set_forkserver_preload
from flask_csp.csp import csp_header
from static.firebaseConnection import FirebaseAdminClass

# <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src https://images.unsplash.com;">
# @csp_header(CspClass().return_csp_header())
class CspClass:
    def __init__(self):
        self.__fba_db = FirebaseAdminClass()
        self.__default_src = ""
        self.__script_src = ""
        self.__script_src_elem = ""
        self.__script_src_attr = ""
        self.__img_src = ""
        self.__style_src = ""
        self.__style_src_elem = ""
        self.__style_src_attr = ""

    def create_policy(self, child_name:str, default_src:list=None, script_src:list=None, script_src_elem:list=None, script_src_attr:list=None, img_src:list=None, style_src:list=None, style_src_elem:list=None, style_src_attr:list=None):
        policy_dict = {}
        
        if default_src:
            policy_dict['default-src'] = default_src

        if script_src:
            policy_dict['script-src'] = script_src

        if script_src_elem:
            policy_dict['script-src-elem'] = script_src_elem

        if script_src_attr:
            policy_dict['script-src-attr'] = script_src_attr

        if img_src:
            policy_dict['img-src'] = img_src

        if style_src:
            policy_dict['style-src'] = style_src

        if style_src_elem:
            policy_dict['style-src-elem'] = style_src_elem

        if style_src_attr:
            policy_dict['style-src-attr'] = style_src_attr

        self.__fba_db.fa_create_csp(child_name, policy_dict)

    def return_csp_header(self, child_name:str):
        db_policy = self.__fba_db.fa_get_csp()[child_name]

        for key,value in db_policy.items():
            db_policy[key] = ' '.join(value)

        return db_policy

# if __name__ == "__main__":
    # print(CspClass().return_csp_header('homepage'))