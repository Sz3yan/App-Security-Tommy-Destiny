import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, db, exceptions
import os
from dotenv import load_dotenv
from pprint import pprint



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

        self.__firebase = pyrebase.initialize_app(firebaseConfig)
        self.__auth = self.__firebase.auth()
        self.__database = self.__firebase.database()
        self.__storage = self.__firebase.storage()
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
            pprint(user)
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


class FirebaseAdminClass(FirebaseClass):
    def __init__(self):
        super().__init__()
        self.__firebaseAdmin = firebase_admin.initialize_app(credentials.Certificate("Tommy-Destiny/static/serviceAccountKey.json"),{"databaseURL": os.getenv("DATABASE_URL")})
        self.__firebaseAdmin_db_reference = db.reference()

    # Get User
    def fa_get_user(self, UserID):
        # if auth.UserNotFoundError(message="User not found"):
        #     return auth.UserNotFoundError(message="User not found")
        # elif exceptions.FirebaseError(message="Unable to connect to firebase"):
        #     return exceptions.FirebaseError(message="Unable to connect to firebase")
        # else:
            try:
                return auth.get_user(UserID)
            except ValueError:
                return "Invalid User ID"
    
    # Get Post
    def fa_get_post(self):
        return self.__firebaseAdmin_db_reference.child('Post').get()

    # Create Policy
    def fa_create_csp(self, child_name:str, policy_dict:dict):
        return self.__firebaseAdmin_db_reference.child('Content_Security_Policy').child(child_name).set(policy_dict)
    
    # Get Policy
    def fa_get_csp(self):
        return self.__firebaseAdmin_db_reference.child('Content_Security_Policy').get()
    

    


# # Test
if __name__ == "__main__":
    fb = FirebaseClass()
    fba = FirebaseAdminClass()

    # fba.fa_create_csp('homeage',['hellp'], ['asdas','sadasdass'])
    # fba.fa_create_csp('login',['hellp'], ['asdas','sadasdass'])
    # fba.fa_create_csp()
    print(fba.fa_get_csp())

    # fb.create_user("YouKnow@gmail.com","Hello123456")
    # fb.login_user("YouKnow@gmail.com","Hello123456")

    # auth.update_user(fb.get_user(), display_name="Your welcome")
    # print(fb.get_user())
    
    # print(fba.get_user(fb.get_user()).uid)
    # # print(fba.get_db())





#     # fb.get_image_url()
#     # fb.create_user("plshelpme@mail.com", "unknown")
#     # fb.login_user("hai@mail.com", "unknown")

#     pushorpull_post = FirebaseClass()
#     for i in pushorpull_post.get_post().each():
#         print(i.key())