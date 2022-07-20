from flask import Blueprint, redirect, render_template, request, url_for,g, session
from web.admin.static.py.Post import Post, SubmitPostForm
from static.py.firebaseConnection import FirebaseClass
from base64 import b64encode, b64decode
from functools import wraps
import json, logging

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')
# logging.basicConfig(filename='../../tommy-destiny.log', encoding='utf-8', level=logging.DEBUG)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        firebase = FirebaseClass() # this will not hve any id
        user_ID = session["userID"]
        print(user_ID)

        userInfo = firebase.get_user_info(user_ID)
        g.current_user = userInfo
        if 'userID' in session:
            if g.current_user.get("Role") == "admin":
                print(g.current_user.get("Role"))
                return f(*args, **kwargs)
            else:
                return redirect(url_for('user.index'))
        else:
            return redirect(url_for("user.index"))
    return wrap


@admin.route("/dashboard")
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')


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
        print("No posts found")

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

    data = [{
        "type" : "header",
        "data" : {
            "text" : "Post title",
        }
    }]

    try:
        pull_post = FirebaseClass()

        for i in pull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                iv = i.val()["_Post__iv"]
                key = i.val()["_Post__key"]
                plaintext = i.val()["_Post__plaintext"]

                trimiv = iv[1:-1]
                trimkey = key[1:-1]
                trimplaintext = plaintext[1:-1]

                encode_iv = b64decode(trimiv)
                encode_key = b64decode(trimkey)
                encode_plaintext = b64decode(trimplaintext)

                s = Secure()
                s.set_iv(encode_iv)
                s.set_key(encode_key)
                decrypted = s.decrypt(encode_plaintext)

                to_json = json.loads(decrypted.decode())
                data = to_json["blocks"]
                print(data)
            else:
                data = data
    except:
        print("No posts found")

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
            print("error")
            title = "title"

        secure = Secure()
        encrypted_content = secure.encrypt(content)

        newPost.set_id(id)
        newPost.set_title(title)
        newPost.set_key(str(b64encode(secure.get_key())))
        newPost.set_iv(str(b64encode(secure.get_iv())))
        newPost.set_plaintext(str(b64encode(encrypted_content)))

        # need fix duplication of post
        pushorpull_post = FirebaseClass()
        for i in pushorpull_post.get_post().each():
            if i.val()["_Post__id"] == id:
                pushorpull_post.update_post(id, newPost)
                print("Post updated")
                return redirect(url_for('admin.post'))
            else:
                pushorpull_post.create_post(newPost)
                print("Post created")
                return redirect(url_for('admin.post'))

        return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)

    return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)


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
