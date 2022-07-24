import json
import os
from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, g, session, abort
from mitigations.A3_Sensitive_data_exposure import AES_GCM, GoogleCloudKeyManagement
from mitigations.API10_Insufficient_logging_and_monitoring import Admin_Logger, User_Logger
from static.py.firebaseConnection import FirebaseClass
from routes.admin.static.py.Post import Post, SubmitPostForm

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')
Admin_Logger = Admin_Logger()
User_Logger = User_Logger()
keymanagement = GoogleCloudKeyManagement()
secret_key = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", "key-rotation"))


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        firebase = FirebaseClass() # this will not hve any id
        if 'userID' in session:
            user_ID = session["userID"]
            userInfo = firebase.get_user_info(user_ID)
            g.current_user = userInfo
            if g.current_user.get("Role") == "admin":
                print(g.current_user.get("Role"))
                return f(*args, **kwargs)
            else:
                return redirect(url_for("user.index"))
        else:
            return redirect(url_for('user.index'))

    return wrap


@admin.route("/dashboard")
@admin_required
def admin_dashboard():
    labels = [1,2,3,4,5,6,7,8,9,10]
    values = [514, 1433, 1687, 2711, 3715, 4184, 4398, 5322, 510, 975, 975, 1395, 1395, 1860, 2070, 2490]

    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
    except:
        posts = []
        Admin_Logger.log_exception("No posts found")

    admin_logs = Admin_Logger.read_adminlog()
    print(admin_logs, "\n")

    user_logs = User_Logger.read_userlog()
    print(user_logs, "\n")
    
    return render_template('admin_dashboard.html',labels=labels, values=values, posts=posts, admin_logs=admin_logs, user_logs=user_logs)


@admin.route("/viewsite")
@admin_required
def view_admin():
    return render_template('admin_viewsite.html')


@admin.route("/posts")
@admin_required
def post():
    newPost = Post("title")
    new_id = newPost.get_id()

    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
    except:
        posts = []
        Admin_Logger.log_exception("No posts found")

    return render_template('admin_post.html', id=new_id, posts=posts)


@admin.route("/pages")
@admin_required
def page():
    return render_template('admin_pages.html')


@admin.route("/editor/posts/<id>", methods=["GET", "POST"])
@admin_required
def editor_post(id):
    newPost = Post("title")
    newPost.set_id(id)
    aes_gcm = AES_GCM()

    data = [{
        "type": "header",
        "data": {
            "text": "Post title",
        }
    }]

    try:
        pull_post = FirebaseClass()

        for i in pull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                plaintext = i.val()["_Post__plaintext"]

                decrypted = aes_gcm.decrypt(secret_key, plaintext)
                print("decrypted: ", decrypted)

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
                Admin_Logger.log_info(f"view: post_id {id}: ")
            else:
                data = data
    except:
        Admin_Logger.log_exception("No posts found")

    submit_post = SubmitPostForm(request.form)

    try:
        hcontent_string = submit_post.content.data
        hcontent_to_dict = json.loads(hcontent_string)
        htitle = hcontent_to_dict["blocks"][0]["data"]["text"]
    except:
        htitle = "Post title"

    if request.method == "POST" and htitle != "Post title":
        content = submit_post.content.data.encode("utf-8")

        try:
            content_string = submit_post.content.data
            content_to_dict = json.loads(content_string)
            title = content_to_dict["blocks"][0]["data"]["text"]
        except:
            Admin_Logger.log_exception("No title found, must change first")
            title = "title"

        encrypted_content = aes_gcm.encrypt(secret_key, content)
        # print("encrypted_content: ", encrypted_content)
        Admin_Logger.log_info(f"encrypted post_id {id}: " + encrypted_content)

        newPost.set_id(id)
        newPost.set_title(title)
        newPost.set_plaintext(encrypted_content)

        createorupdate = FirebaseClass()
        length = 0
        for posts in createorupdate.get_post().each():
            length += 1
            if posts.val()["_Post__id"] == id:  # false
                createorupdate.update_post(id, newPost)
                Admin_Logger.log_info(f"updated post_id {id}: " + encrypted_content)
                return redirect(url_for('admin.post'))
            elif length == len(createorupdate.get_post().each()):
                createorupdate.create_post(newPost)
                Admin_Logger.log_info(f"created post_id {id}: " + encrypted_content)
                return redirect(url_for('admin.post'))

        return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)

    return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)


@admin.route("/delete/posts/<id>", methods=["GET", "POST"])
@admin_required
def delete_page(id):
    deletepost = FirebaseClass()
    deletepost.delete_post(id)
    Admin_Logger.log_info(f"deleted post_id {id}:")
    return redirect(url_for('admin.post'))


@admin.route("/editor/pages/<id>", methods=["POST"])
@admin_required
def editor_pages(id):
    return render_template('admin_editor.html')


@admin.route("/tags")
@admin_required
def tags():
    return render_template('admin_tags.html')


@admin.route("/members")
@admin_required
def members():
    return render_template('admin_members.html')


@admin.route("/settings")
@admin_required
def settings():
    return render_template('admin_settings.html')


@admin.route("/audit_log")
@admin_required
def audit_log():
    Admin_Logger.log_warning("view: audit_log")
    admin_logs = Admin_Logger.read_adminlog()
    print(admin_logs, "\n")

    user_logs = User_Logger.read_userlog()
    print(user_logs, "\n")

    return render_template('admin_audit_log.html', admin_logs=admin_logs, user_logs=user_logs)


@admin.route("/policy")
@admin_required
def policy():
    return render_template('admin_policy.html')
