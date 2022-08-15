from flask import Blueprint, request, jsonify
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
from static.firebaseConnection import FirebaseAdminClass, FirebaseClass
# from mitigations.API10_Insufficient_logging_and_monitoring import User_Logger
from datetime import timedelta

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/login", methods=["POST", "GET"])
def api_login():
    
    if request.is_json and request.method == "POST":
        try:
            email = request.json['email']
            password = request.json['password']

            fb = FirebaseClass()

            if not fb.login_user(email, password):
                userID = fb.get_user()
                User_Logger().log_info("User Login Successful")
                access_token = create_access_token(identity=userID, fresh=timedelta(hours=1), expires_delta=timedelta(hours=1))
                return jsonify(message="Login Successfully", access_token=access_token), 200
            else:
                User_Logger().log_info("User Login Failed")
                return jsonify(message="Invalid email or password"), 401
        except:
            return jsonify(message="Invalid value")
    else:
        return jsonify(message="Request shall be in a JSON format.")
            

@api.route("/userInfo", methods=["POST","GET"])
@jwt_required(fresh=True)
def user_info():
    fba = FirebaseAdminClass()
    userInfo = fba.fa_get_user(get_jwt_identity())
    infoDict = {"UserID":get_jwt_identity(), "Email": userInfo.email, "Name": userInfo.display_name, "Phone Number": userInfo.phone_number}
    
    return jsonify(userInfo=infoDict)


@api.route("/users")
def api_users():
    if request.is_json:
        name = request.json["user"]
        isAdmin = False
    else:
        isAdmin = request.args.get('isAdmin')
        name = request.args.get("name")
    
    if isAdmin == True:
        return jsonify(message=f"Hi {name}, you are an admin"), 200
    elif name != "":
        return jsonify(message=f"Hi {name}, you are not an admin"), 200
    else:
        return jsonify(message="Invalid parameters"), 404