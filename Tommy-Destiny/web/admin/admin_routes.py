import json
from functools import wraps

from flask import Blueprint, redirect, render_template, request, url_for, g, session
from mitigations.A3_Sensitive_data_exposure import AES_GCM
from mitigations.API10_Insufficient_logging_and_monitoring import Admin_Logger
from static.py.firebaseConnection import FirebaseClass
from web.admin.static.py.Post import Post, SubmitPostForm

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')
Admin_Logger = Admin_Logger()


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        firebase = FirebaseClass()
        userInfo = firebase.get_user_info()
        userID = firebase.get_user()
        if 'userID' in session:
            if userID == session['userID']:
                g.current_user = userInfo  ###it does reach here
                if g.current_user.get("Role") == "Admin":
                    print(g.current_user.get("Role"))
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('user.index'))

    return wrap


@admin_required
@admin.route("/dashboard")
def admin_dashboard():
    return render_template('admin_dashboard.html')


@admin_required
@admin.route("/viewsite")
def view_admin():
    return render_template('admin_viewsite.html')


@admin_required
@admin.route("/posts")
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


@admin_required
@admin.route("/pages")
def page():
    return render_template('admin_pages.html')


@admin_required
@admin.route("/editor/posts/<id>", methods=["GET", "POST"])
def editor_post(id):
    newPost = Post("title")
    newPost.set_id(id)
    aes_gcm = AES_GCM()
    secret_key = "yourSecretKey"

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
                Admin_Logger.log_info(f"view: post_id {id}: " + str(data)) # demo. log only encrypted data
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


@admin_required
@admin.route("/delete/posts/<id>", methods=["GET", "POST"])
def delete_page(id):
    deletepost = FirebaseClass()
    deletepost.delete_post(id)
    Admin_Logger.log_info(f"deleted post_id {id}:")
    return redirect(url_for('admin.post'))


@admin_required
@admin.route("/editor/pages/<id>", methods=["POST"])
def editor_pages(id):
    return render_template('admin_editor.html')


@admin_required
@admin.route("/tags")
def tags():
    return render_template('admin_tags.html')


@admin_required
@admin.route("/members")
def members():
    return render_template('admin_members.html')


@admin_required
@admin.route("/settings")
def settings():
    return render_template('admin_settings.html')
