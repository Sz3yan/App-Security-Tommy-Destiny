import pyrebase
import os
from dotenv import load_dotenv


load_dotenv()


class FirebaseClass:
    def __init__(self):
        firebaseConfig = {
            "apiKey": os.getenv("API_KEY"),
            "authDomain": os.getenv("AUTH_DOMAIN"),
            "databaseURL": os.getenv("DATABASE_URL"),
            "projectId": os.getenv("PROJ_ID"),
            "storageBucket": os.getenv("S_BUCKET"),
            "messagingSenderId": os.getenv("M_SENDER_ID"),
            "appId": os.getenv("APP_ID"),
            "measurementId": os.getenv("M_ID")
        }

        firebase = pyrebase.initialize_app(firebaseConfig)

        self.__auth = firebase.auth()
        self.__database = firebase.database()
        self.__storage = firebase.storage()
        self.__User_ID = ""

    # User
    def create_user(self, email, password):
        try:
            user = self.__auth.create_user_with_email_and_password(email, password)
            self.__User_ID = user["localId"]
        except:
            return "Email already in use"

    def login_user(self, email, password):
        try:
            user = self.__auth.sign_in_with_email_and_password(email, password)
            self.__User_ID = user["localId"]

        except:
            return "User not found"

    def create_user_info(self, name="", ph_no="", role="customer"):
        detail_dict = {"Name": name, "Phone number": ph_no, "Role": role}
        self.__database.child("User").child(self.__User_ID).set(detail_dict)

    def get_user_info(self, User_ID):
        users = self.__database.child("User").get().each()
        print(User_ID )
        for i in users:
            if i.key() == User_ID:
                return i.val()
        # for user in users.each():
        #     userval = user.val()
        #     print(users)
        #     print(user)
        #     print(userval)
            #print("Username =", userval.get("Name")) how to get stuff from firebase
            # return userval

    def get_user(self):
        # if userId != "" and self.__User_ID == "":
        #     users = self.__database.child("User").get(userId)
        #     for user in users.each():
        #         userkey = user.key()
        #         return userkey
        #     self.__User_ID = userId
        # else:
        User_ID = self.__User_ID
        return User_ID

    # Blog Post
    def create_post(self, post_dict):
        self.__database.child("Post").push(post_dict.__dict__)

    def get_post(self):
        return self.__database.child("Post").get()

    # def update_post(self, post_dict):
    #     self.__database.child("Post").child(post_dict.__dict__["_Post__id"]).update(post_dict.__dict__)

    def update_post(self, post_id, post_dict):
        self.__database.child("Post").child(post_id).update(post_dict.__dict__)
    
    
    # Storage
    def get_image_url(self):
        print(self.__storage.child("image").get_url(None))

    def upload_image(self, stoarge_path, local_image_path):
        self.__storage.child("image").child(stoarge_path).put(local_image_path)


# Test
if __name__ == "__main__":
    fb = FirebaseClass()
    # fb.get_image_url()
    # fb.create_user("plshelpme@mail.com", "unknown")
    # fb.login_user("hai@mail.com", "unknown")

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

        # def get_iv(self):
        #     return self.__iv

        # def set_iv(self, iv):
        #     self.__iv = iv

        def get_key(self):
            return self.__key

        def set_key(self, key):
            self.__key = key

        def __str__(self):
            return f"{self.__id}\n {self.__title}\n {self.__plaintext}\n {self.__featured}\n {self.__status}\n {self.__visibility}\n {self.__created_at}\n {self.__updated_at}\n {self.__published_at}\n {self.__iv}\n {self.__key}"

    a = Post("Test")
    fb.create_post(a)
