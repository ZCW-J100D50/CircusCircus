from flask_login import current_user, login_user, logout_user
import datetime
from flask_login.utils import login_required
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error, Media
from flask import Blueprint, render_template, request, redirect, url_for


posts = Blueprint('posts', __name__, template_folder='templates')


@login_required
@posts.route('/addpost')
def addpost():
	subforum_id = int(request.args.get("sub"))
	subforum = Subforum.query.filter(Subforum.subID == subforum_id).first()
	if not subforum:
		return error("That subforum does not exist!")

	return render_template("createpost.html", subforum=subforum)



@posts.route('/viewpost')
def viewpost():
    postid = int(request.args.get("post"))
    post = Post.query.filter(Post.postID == postid).first()
    if not post:
        return error("That post does not exist!")
    if not post.subforum.path:
        subforumpath = generateLinkPath(post.subforum.subID)
    comments = Comment.query.filter(Comment.post_id == postid).order_by(Comment.commentID.desc()) # no need for scalability now
    return render_template("viewpost.html", post=post, path=subforumpath, comments=comments)


@login_required
@posts.route('/action_post', methods=['POST'])
def action_post():
    subforum_id = int(request.args.get("sub"))
    subforum = Subforum.query.filter(Subforum.subID == subforum_id).first()
    if not subforum:
        return redirect(url_for("subforums"))

    user = current_user
    title = request.form['title']
    content = request.form['content']
    image = request.form['image']
    #check for valid posting
    errors = []
    retry = False
    if not valid_title(title):
        errors.append("Title must be between 4 and 140 characters long!")
        retry = True
    if not valid_content(content):
        errors.append("Post must be between 10 and 5000 characters long!")
        retry = True
    #TODO Check for valid image (null image is also valid)
    if retry:
        return render_template("createpost.html",subforum=subforum,  errors=errors)
    post = Post(title, content, datetime.datetime.now())
    media = Media()
    subforum.posts.append(post)
    user.posts.append(post)
    db.session.commit()
    return redirect("/viewpost?post=" + str(post.postID))

@login_required
@posts.route('/media_post', methods=['GET', 'POST'])
def upload_media():
    if request.method=='POST':
        file = request.files['file']
        return f'Uploaded: {file.filename}'
    return render_template('index.html')