from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error, \
    ReactTypes
from forum.user import username_taken, email_taken, valid_username

comments = Blueprint('comments', __name__, template_folder='templates')


@login_required
@comments.route('/action_comment', methods=['POST', 'GET'])
def comment():
    post_id = int(request.args.get("post"))
    post = Post.query.filter(Post.postID == post_id).first()
    if not post:
        return error("That post does not exist!")
    content = request.form['content']
    postdate = datetime.datetime.now()
    comment = Comment(content, postdate)
    current_user.comments.append(comment)
    post.comments.append(comment)
    db.session.commit()
    return redirect("/viewpost?post=" + str(post_id))


# TODO This should be moved to a standalone reacts.py, but routing currently gives 404 not found
@login_required
@comments.route('/action_react', methods=['POST', 'GET'])
def react():
    if not current_user.is_authenticated:
        return redirect("/loginform")
    post_id = int(request.args.get("post"))
    post = Post.query.filter(Post.postID == post_id).first()
    if not post:
        return error("That post does not exist!")

    for reactType in ReactTypes:
        if request.form.get(reactType) is not None:
            # This was the react button pressed
            current_user.react_to_post(post, reactType)
            break

    return redirect("/viewpost?post=" + str(post_id))
