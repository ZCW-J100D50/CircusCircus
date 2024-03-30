import datetime
from flask import render_template, request, flash, redirect, url_for, Blueprint
#from forum.app import app
from forum.models import Blogposts, db

blog = Blueprint('blog', __name__, template_folder='templates')
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chrism:lesson@localhost/circuscircus'


# def get_post(post_id):
#     get_db_connection()
#     post = my_cursor.execute('SELECT * FROM blogposts WHERE id = %d',
#                         (post_id,))
#
#     if post is None:
# #abort(404)
#         return post
#


@blog.route('/blog/')
def index():
#  get_db_connection()
#   my_cursor.execute('SELECT * FROM blogposts')
#    posts = my_cursor.fetchall()

    posts = Blogposts.query.order_by(Blogposts.id)
    return render_template('blogindex.html', posts=posts)

#{{ url_for('post', post_id=post['id']) }}
@blog.route('/blog/index/<int:post_id>')
def post(post_id):
    posts = Blogposts.query.get_or_404(post_id)
    return render_template('blogpost.html', post=posts)


@blog.route('/blog/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        blog = Blogposts(title, content, datetime.datetime.now())
        if not title:
            flash('Title is required!')
        else:
            db.session.add(blog)
            db.session.commit()
            return redirect('/blog')
    return render_template('createblogpost.html')




@blog.route('/blog/edit/<int:post_id>', methods=('GET', 'POST'))
def edit(post_id):
    post = Blogposts.query.get_or_404(post_id)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        entry = Blogposts(title, content, datetime.datetime.now())
        if not title:
            flash('Title is required!')
        else:
            post.title = title
            post.content = content
            post.created = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
        return redirect('/blog')

    return render_template('edit.html', post=post)



@blog.route('/index/delete/<int:post_id>/', methods=('POST',))
def delete(post_id):
    post_to_delete = Blogposts.query.get_or_404(post_id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Entry Deleted")
        return redirect('/blog')
    except:
        pass
    # get_db_connection()
    # my_cursor.execute('DELETE FROM blogposts WHERE id = %d', (id,))
    # mydb.commit()
    # flash('"{}" was successfully deleted!'.format(post['title']))





