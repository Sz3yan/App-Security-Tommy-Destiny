import pyrebase
import firebase_admin
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials



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
        # firebaseAdmin = firebase_admin.initialize_app(credentials.Certificate("path/to/serviceAccountKey.json"))

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
        for i in self.__database.child("Post").get().each():
            if i.val()["_Post__id"] == post_id:
                self.__database.child("Post").child(i.key()).update(post_dict.__dict__)
                return "Post updated"

    def delete_post(self, post_id):
        for i in self.__database.child("Post").get().each():
            if i.val()["_Post__id"] == post_id:
                self.__database.child("Post").child(i.key()).remove()
                return "Post deleted"
    
    # Storage
    def get_image_url(self):
        print(self.__storage.child("image").get_url(None))

    def upload_image(self, stoarge_path, local_image_path):
        self.__storage.child("image").child(stoarge_path).put(local_image_path)


# # Test
if __name__ == "__main__":
    fb = FirebaseClass()
#     # fb.get_image_url()
#     # fb.create_user("plshelpme@mail.com", "unknown")
#     # fb.login_user("hai@mail.com", "unknown")

#     pushorpull_post = FirebaseClass()
#     for i in pushorpull_post.get_post().each():
#         print(i.key())