import datetime
from datetime import *
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from forum.models import db

from . import cre

#from werkzeug import abort
import MySQLdb
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kristofer'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://chrism:lesson@localhost/circuscircus'

mydb = mysql.connector.connect(
    host="localhost",
    user="chrism",
    passwd="lesson",
)




my_cursor = mydb.cursor(buffered=True)

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chrism:lesson@localhost/circuscircus'

def get_db_connection():
    #conn = sqlite3.connect('../database.db')
    #conn.row_factory = sqlite3.Row
    my_cursor.execute('use circuscircus')


def get_post(post_id):
    get_db_connection()
    post = my_cursor.execute('SELECT * FROM blogposts WHERE id = %d',
                        (post_id,))

    if post is None:
#abort(404)
        return post



@app.route('/')
def index():
    get_db_connection()
    my_cursor.execute('SELECT * FROM blogposts')
    posts = my_cursor.fetchall()
    return render_template('index.html', post=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:

            my_cursor.execute('INSERT INTO blogposts (title, content) VALUES (%s, %s)',  (title, content))
            mydb.commit()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            get_db_connection()
            my_cursor.execute('UPDATE blogposts SET title = %s, content = %s, WHERE id = %d', (title, content, id))
            mydb.commit()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)



@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    get_db_connection()
    my_cursor.execute('DELETE FROM blogposts WHERE id = %d', (id,))
    mydb.commit()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))




