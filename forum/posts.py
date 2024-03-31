import os
from pathlib import Path

from flask_login import current_user, login_user, logout_user
import datetime
from flask_login.utils import login_required
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error, Media
from flask import Blueprint, render_template, request, redirect, url_for
from base64 import b64encode


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

    # Test code to show the image
    media = Media.query.filter(Media.post_id == postid).first()
    if media is None:
        return render_template("viewpost.html", post=post, path=subforumpath,
                               comments=comments)
    if media.mediaType == 'image':
        filepath = media.filePath
        return render_template("viewpost_withimage.html", post=post, path=subforumpath,
                               comments=comments, media_filepath=filepath)
    if media.mediaType == 'video':
        filepath = media.filePath
        return render_template("viewpost_withvideo.html", post=post, path=subforumpath,
                               comments=comments, media_filepath=filepath)
    # TODO: Handle case where mediaType is not image or video for some reason

    # obj = Media.query.filter(Media.post_id == postid).first()
    # if obj != None:
    #     image = b64encode(obj.data).decode("utf-8")
    #     return render_template("viewpost_withimage.html", post=post, path=subforumpath, comments=comments, obj=obj, image=image)
    # else:
    #     return render_template("viewpost.html", post=post, path=subforumpath, comments=comments)


@login_required
@posts.route('/action_post', methods=['POST'])
def action_post():
    subforum_id = int(request.args.get("sub"))
    subforum = Subforum.query.filter(Subforum.subID == subforum_id).first()
    if not subforum:
        return redirect(url_for("subforums"))
    count = 0
    privacy = 0
    user = current_user
    title = request.form['title']
    content = request.form['content']
    if 'private' in request.form:
        count += 1
        if not count % 2 == 0:
            privacy = 1
        else:
            privacy = 0



    #check for valid posting
    errors = []
    retry = False
    if not valid_title(title):
        errors.append("Title must be between 4 and 140 characters long!")
        retry = True
    if not valid_content(content):
        errors.append("Post must be between 10 and 5000 characters long!")
        retry = True
    if retry:
        return render_template("createpost.html",subforum=subforum,  errors=errors)

    post = Post(title, content, datetime.datetime.now(), is_private=privacy)
    subforum.posts.append(post)
    user.posts.append(post)

    file = request.files['image']
    basedir = os.path.abspath(os.path.dirname(__file__))
    media_is_valid = False
    upload_filepath = None
    saved_filepath = None
    media_type = None
    saved_filename = f'{post.postID}_{file.filename}'.replace(" ","_")
    if Path(file.filename).suffix in ['.mov', '.mp4']:
        upload_filepath = os.path.join(basedir, 'static/user_media/videos', saved_filename)
        saved_filepath = os.path.join('static/user_media/videos', saved_filename)
        media_type = 'video'
        media_is_valid = True
    elif Path(file.filename).suffix in ['.jpeg', '.jpg', '.png', '.bmp']:
        upload_filepath = os.path.join(basedir, 'static/user_media/images', saved_filename)
        saved_filepath = os.path.join('static/user_media/images', saved_filename)
        media_type = 'image'
        media_is_valid = True
    else:
        pass
    if media_is_valid:
        file.save(upload_filepath)
        media = Media(file.filename, saved_filepath, media_type)
        post.media.append(media)
        user.media.append(media)
    db.session.commit()
    return redirect("/viewpost?post=" + str(post.postID))

