from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__, url_prefix='/api')

@api.route("/api/favourites")
def api_favourite():
    pass


@api.route("/api/users")
def api_users():
    isAdmin = request.args.get('isAdmin')
    name = request.args.get("name")
    
    if isAdmin == True:
        return jsonify(message=f"Hi {name}, you are an admin"), 200
    elif name != "":
        return jsonify(message=f"Hi {name}, you are not an admin"), 200
    else:
        return jsonify(message="Invalid parameters"), 404