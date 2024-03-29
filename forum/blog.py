from flask import render_template, request, flash, redirect, url_for, Blueprint
#from forum.app import app
from forum.models import Blogposts

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

    posts = Blogposts.query.all()
    return render_template('blogindex.html', post=posts)


@blog.route('/blog/<int:post_id>')
def post(post_id):
    post = Blogposts.query.filter(id=post_id)
    return render_template('post.html', post=post)


@blog.route('/blog/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            pass
            # my_cursor.execute('INSERT INTO blogposts (title, content) VALUES (%s, %s)',  (title, content))
            # mydb.commit()
            # return redirect(url_for('index'))

    return render_template('createblogpost.html')


@blog.route('/blog/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = Blogposts.query.filter(id=id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            pass
            # get_db_connection()
            # my_cursor.execute('UPDATE blogposts SET title = %s, content = %s, WHERE id = %d', (title, content, id))
            # mydb.commit()

            #return redirect(url_for('index'))

    return render_template('edit.html', post=post)



@blog.route('/blog/<int:id>/delete', methods=('POST',))
def delete(id):
    post = Blogposts.query.filter(id=id)
    # get_db_connection()
    # my_cursor.execute('DELETE FROM blogposts WHERE id = %d', (id,))
    # mydb.commit()
    # flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))




