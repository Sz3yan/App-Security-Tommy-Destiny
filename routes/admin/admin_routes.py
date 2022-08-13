import json
import os
from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, g, session, abort
from mitigations.A3_Sensitive_data_exposure import AES_GCM, GoogleCloudKeyManagement
from mitigations.API10_Insufficient_logging_and_monitoring import Admin_Logger, User_Logger
from static.firebaseConnection import FirebaseClass
from routes.admin.static.py.Post import Post, SubmitPostForm
from collections import OrderedDict

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

Admin_Logger = Admin_Logger()
User_Logger = User_Logger()

keymanagement = GoogleCloudKeyManagement()
secret_key = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", "key_id"))

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
def admin_dashboard():
    labels = [1,2,3,4,5,6,7,8,9,10]
    values = [514, 1433, 1687, 2711, 3715, 4184, 4398, 5322, 510, 975, 975, 1395, 1395, 1860, 2070, 2490]

    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        Admin_Logger.log_info("Admin dashboard: retrieved posts")
    except:
        posts = []
        Admin_Logger.log_exception("Admin dashboard: No posts found")

    admin_logs = Admin_Logger.read_adminlog()
    user_logs = User_Logger.read_userlog()
    
    return render_template('admin_dashboard.html',labels=labels, values=values, posts=posts, admin_logs=admin_logs, user_logs=user_logs)


@admin.route("/viewsite")
def view_admin():
    return render_template('admin_viewsite.html')


@admin.route("/posts", methods=['GET', 'POST'])
def post():
    newPost = Post("title")
    new_id = newPost.get_id()

    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        Admin_Logger.log_info("Admin posts: retrieved posts")
    except:
        posts = []
        Admin_Logger.log_exception("Admin posts: No posts found")

    return render_template('admin_post.html', id=new_id, posts=posts)


@admin.route("/pages")
def page():
    return render_template('admin_pages.html')


@admin.route("/editor/posts/<id>", methods=["GET", "POST"])
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
                Admin_Logger.log_info(f"Admin editor: decrypted post {id}")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        Admin_Logger.log_exception("Admin editor: No posts found")

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
            title = "title"

        encrypted_content = aes_gcm.encrypt(secret_key, content)
        Admin_Logger.log_info(f"Admin editor: encrypted post {id}")

        newPost.set_id(id)
        newPost.set_title(title)
        newPost.set_plaintext(encrypted_content)

        createorupdate = FirebaseClass()
        length = 0
        for posts in createorupdate.get_post().each():
            length += 1
            if posts.val()["_Post__id"] == id:
                createorupdate.update_post(id, newPost)
                Admin_Logger.log_info(f"Admin editor: update post {id}")
                return redirect(url_for('admin.post'))
            elif length == len(createorupdate.get_post().each()):
                createorupdate.create_post(newPost)
                Admin_Logger.log_info(f"Admin editor: create post {id}")
                return redirect(url_for('admin.post'))

        return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)

    return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)


@admin.route("/delete/posts/<id>", methods=["GET", "POST"])
def delete_page(id):
    deletepost = FirebaseClass()
    deletepost.delete_post(id)
    Admin_Logger.log_info(f"Admin delete: delete post {id}")
    
    return redirect(url_for('admin.post'))


@admin.route("/editor/pages/<id>", methods=["POST"])
def editor_pages(id):
    return render_template('admin_editor.html')


@admin.route("/members")
def members():
    return render_template('admin_members.html')



@admin.route("/loggingMonitoring")
def audit_log():
    admin_logs = Admin_Logger.read_adminlog()
    Admin_Logger.log_warning("Admin audit log: retrieved Admin logs")

    tojsonAdminlog = {}

    for i in admin_logs:
        tojson = json.loads(admin_logs[i])
        tojsonAdminlog[i] = tojson

    print(tojsonAdminlog)

    user_logs = User_Logger.read_userlog()
    Admin_Logger.log_warning("Admin audit log: retrieved User logs")

    tojsonUserlog = {}

    for i in user_logs:
        tojson = json.loads(user_logs[i])
        tojsonUserlog[i] = tojson

    return render_template('admin_loggingMonitoring.html', admin_logs=dict(reversed(list(tojsonAdminlog.items()))), user_logs=dict(reversed(list(tojsonUserlog.items()))), admin_count=len(admin_logs), user_count=len(user_logs))


@admin.route("/policy")
def policy():
    return render_template('admin_policy.html')