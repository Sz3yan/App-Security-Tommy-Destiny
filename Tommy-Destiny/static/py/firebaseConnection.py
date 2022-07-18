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
            print("Duplicate user")

    def login_user(self, email, password):
        try:
            user = self.__auth.sign_in_with_email_and_password(email, password)
            print("Signed in")
        except:
            return "User not found"

    def create_user_info(self, name="", ph_no="", role="customer"):
        detail_dict = {"Name": name, "Phone number": ph_no, "role": role}
        self.__database.child("User").child(self.__User_ID).set(detail_dict)

    def get_user_info(self):
        users = self.__database.child("User").get()
        for user in users.each():
            userval = user.val()
            #print("Username =", userval.get("Name")) how to get stuff from firebase
            return userval

    def get_user(self):
        users = self.__database.child("User").get()
        for user in users.each():
            userkey = user.key()
            return userkey

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
