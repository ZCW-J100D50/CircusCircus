from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error
from flask import Blueprint, render_template, request, redirect, url_for

subforums = Blueprint('subforum', __name__, template_folder='templates')


@subforums.route('/subforum')
def subforum():
	subforum_id = int(request.args.get("sub"))
	subforum = Subforum.query.filter(Subforum.subID == subforum_id).first()
	if not subforum:
		return error("That subforum does not exist!")
	posts = Post.query.filter(Post.subforum_id == subforum_id).order_by(Post.postID.desc()).limit(50)
	if not subforum.path:
		subforumpath = generateLinkPath(subforum.subID)

	subforums = Subforum.query.filter(Subforum.parent_id == subforum_id).all()
	return render_template("subforum.html", subforum=subforum, posts=posts, subforums=subforums, path=subforumpath)
