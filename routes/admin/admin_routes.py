import json

from functools import wraps
from flask import Blueprint, redirect, render_template, request, url_for, g, session
from static.firebaseConnection import FirebaseClass
from routes.admin.static.py.Post import Post, SubmitPostForm
from routes.admin.static.py.Page import Page
from mitigations.A3_Sensitive_data_exposure import AES_GCM, GoogleCloudKeyManagement, GoogleSecretManager
from mitigations.API10_Insufficient_logging_and_monitoring import GoogleCloudLogging


admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')

write_logs = GoogleCloudLogging()
googlesecretmanager = GoogleSecretManager()
keymanagement = GoogleCloudKeyManagement()

secret_key_post = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", googlesecretmanager.get_secret_payload("tommy-destiny", "hsm_tommy", "1")))
secret_key_page = str(keymanagement.retrieve_key("tommy-destiny", "global", "my-key-ring", googlesecretmanager.get_secret_payload("tommy-destiny", "hsm_tommy1", "1")))


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        firebase = FirebaseClass() # this will not hve any id
        if 'userID' in session:
            user_ID = session["userID"]
            userInfo = firebase.get_user_info(user_ID)
            g.current_user = userInfo
            if g.current_user.get("Role") == "admin":
                return f(*args, **kwargs)
            else:
                return redirect(url_for("user.index"))
        else:
            return redirect(url_for('user.index'))

    return wrap


@admin.route("/dashboard")
@admin_required
def admin_dashboard():
    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        write_logs.write_entry_info("Admin dashboard: retrieved posts")

    except:
        posts = []
        write_logs.write_entry_exception("Admin dashboard: No posts found")

    try:
        firebase = FirebaseClass()
        pages = [page.val() for page in firebase.get_page().each()]
        write_logs.write_entry_info("Admin posts: retrieved pages")
    except:
        pages = []
        write_logs.write_entry_exception("Admin posts: No page found")
    
    return render_template('admin_dashboard.html', posts=posts, pages=pages, countposts=len(posts), countpages=len(pages))


@admin.route("/viewsite")
@admin_required
def view_admin():
    return render_template('admin_viewsite.html')


@admin.route("/posts", methods=['GET', 'POST'])
@admin_required
def post():
    newPost = Post("title")
    new_id = newPost.get_id()

    try:
        firebase = FirebaseClass()
        posts = [post.val() for post in firebase.get_post().each()]
        write_logs.write_entry_info("Admin posts: retrieved posts")
    except:
        posts = []
        write_logs.write_entry_exception("Admin posts: No posts found")

    return render_template('admin_post.html', id=new_id, posts=posts)


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

                decrypted = aes_gcm.decrypt(secret_key_post, plaintext)
                write_logs.write_entry_info(f"Admin editor: decrypted post {id} with hsm_tommy key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data

        pull_post.delete_app()
    except:
        write_logs.write_entry_exception("Admin editor: No posts found")

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

        encrypted_content = aes_gcm.encrypt(secret_key_post, content)
        write_logs.write_entry_info(f"Admin editor: encrypted post {id} with hsm_tommy key")

        newPost.set_id(id)
        newPost.set_title(title)
        newPost.set_plaintext(encrypted_content)

        createorupdate = FirebaseClass()
        length = 0
        for posts in createorupdate.get_post().each():
            length += 1
            if posts.val()["_Post__id"] == id:
                createorupdate.update_post(id, newPost)
                write_logs.write_entry_info(f"Admin editor: update post {id}")
                return redirect(url_for('admin.post'))
            elif length == len(createorupdate.get_post().each()):
                createorupdate.create_post(newPost)
                write_logs.write_entry_info(f"Admin editor: create post {id}")
                return redirect(url_for('admin.post'))

        return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)

    return render_template('admin_editor.html', id=id, newPost=newPost, form=submit_post, data=data)


@admin.route("/delete/posts/<id>", methods=["GET", "POST"])
@admin_required
def delete_post(id):
    deletepost = FirebaseClass()
    deletepost.delete_post(id)
    write_logs.write_entry_info(f"Admin delete: delete post {id}")
    
    return redirect(url_for('admin.post'))


@admin.route("/pages", methods=['GET', 'POST'])
@admin_required
def page():
    newPage = Page("title")
    new_id = newPage.get_id()

    try:
        firebase = FirebaseClass()
        pages = [page.val() for page in firebase.get_page().each()]
        write_logs.write_entry_info("Admin posts: retrieved pages")
    except:
        pages = []
        write_logs.write_entry_exception("Admin posts: No page found")

    return render_template('admin_pages.html', id=new_id, pages=pages)


@admin.route("/editor/pages/<id>", methods=['GET', 'POST'])
@admin_required
def editor_pages(id):
    newPage = Page("title")
    newPage.set_id(id)
    aes_gcm = AES_GCM()

    data = [{
        "type": "header",
        "data": {
            "text": "Page title",
        }
    }]

    try:
        pull_page = FirebaseClass()

        for i in pull_page.get_page().each():
            if i.val()["_Page__id"] == id:
                plaintext = i.val()["_Page__plaintext"]

                decrypted = aes_gcm.decrypt(secret_key_page, plaintext)
                write_logs.write_entry_info(f"Admin editor: decrypted page {id} with hsm_tommy1 key")

                to_json = json.loads(decrypted)
                data = to_json["blocks"]
            else:
                data = data
    except:
        write_logs.write_entry_exception("Admin editor: No page found")

    submit_page = SubmitPostForm(request.form)

    try:
        hcontent_string = submit_page.content.data
        hcontent_to_dict = json.loads(hcontent_string)
        htitle = hcontent_to_dict["blocks"][0]["data"]["text"]
    except:
        htitle = "Page title"

    if request.method == "POST" and htitle != "Page title":
        content = submit_page.content.data.encode("utf-8")

        try:
            content_string = submit_page.content.data
            content_to_dict = json.loads(content_string)
            title = content_to_dict["blocks"][0]["data"]["text"]
        except:
            title = "title"

        encrypted_content = aes_gcm.encrypt(secret_key_page, content)
        write_logs.write_entry_info(f"Admin editor: encrypted page {id} with hsm_tommy1 key")

        newPage.set_id(id)
        newPage.set_title(title)
        newPage.set_plaintext(encrypted_content)

        createorupdate = FirebaseClass()
        length = 0
        for pages in createorupdate.get_page().each():
            length += 1
            if pages.val()["_Page__id"] == id:
                createorupdate.update_page(id, newPage)
                write_logs.write_entry_info(f"Admin editor: update page {id}")
                return redirect(url_for('admin.page'))
            elif length == len(createorupdate.get_page().each()):
                createorupdate.create_page(newPage)
                write_logs.write_entry_info(f"Admin editor: create page {id}")
                return redirect(url_for('admin.page'))

        return render_template('admin_editor_page.html', id=id, newPost=newPage, form=submit_page, data=data)

    return render_template('admin_editor_page.html', id=id, newPost=newPage, form=submit_page, data=data)


@admin.route("/delete/pages/<id>", methods=["GET", "POST"])
@admin_required
def delete_page(id):
    deletepage = FirebaseClass()
    deletepage.delete_page(id)
    write_logs.write_entry_info(f"Admin delete: delete page {id}")
    
    return redirect(url_for('admin.page'))
