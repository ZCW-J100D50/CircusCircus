from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from flask import Blueprint, render_template, request, redirect, url_for
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error
from forum.user import username_taken, email_taken, valid_username

# ACTION LINKS FROM FLASK
# USER_CHANGE_PASSWORD_URL = '/user/change-password'
# USER_CHANGE_USERNAME_URL = '/user/change-username'
# USER_FORGOT_PASSWORD_URL = '/user/forgot-password'

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/loginform') #done
def loginform():
	return render_template("login.html")

# CHANGE PASSWORD
# USER_CHANGE_PASSWORD_URL = '/user/change-password'
# need TRUE username + TRUE PASSWORD to change
# ELSE "access denied?  Need proper login credentials!"
@auth.route('/action_login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        login_user(user)
    else:
        errors = []
        errors.append("Username or password is incorrect!")
        return render_template("login.html", errors=errors)
    return redirect("/")

# CHANGE USERNAME
# USER_CHANGE_USERNAME_URL = '/user/change-username'
@auth.route('/action_login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        login_user(user)
    else:
        errors = []
        errors.append("Username or password is incorrect!")
        return render_template("login.html", errors=errors)
    return redirect("/")

# FORGOT PASSWORD - cannot verify just let them change.
# USER_FORGOT_PASSWORD_URL = '/user/forgot-password'
@auth.route('/action_login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        login_user(user)
    else:
        errors = []
        errors.append("Username or password is incorrect!")
        return render_template("login.html", errors=errors)
    return redirect("/")



@auth.route('/action_login', methods=['POST'])
def action_login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter(User.username == username).first()
    if user and user.check_password(password):
        login_user(user)
    else:
        errors = []
        errors.append("Username or password is incorrect!")
        return render_template("login.html", errors=errors)
    return redirect("/")


@login_required
@auth.route('/action_logout')
def action_logout():
    #todo
    logout_user()
    return redirect("/")


@auth.route('/action_createaccount', methods=['POST'])
def action_createaccount():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    errors = []
    retry = False
    if username_taken(username):
        errors.append("Username is already taken!")
        retry=True
    if email_taken(email):
        errors.append("An account already exists with this email!")
        retry = True
    if not valid_username(username):
        errors.append("Username is not valid!")
        retry = True
    # if not valid_password(password):
    # 	errors.append("Password is not valid!")
    # 	retry = True
    if retry:
        return render_template("login.html", errors=errors)
    user = User(email, username, password)
    if user.username == "admin":
        user.admin = True
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect("/")
