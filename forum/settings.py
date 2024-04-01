import bcrypt
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from flask_login.utils import login_required
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, request, redirect, url_for
from forum.models import User, Post, Comment, Subforum, valid_content, valid_title, db, generateLinkPath, error
from forum.user import username_taken, email_taken, valid_username



settings = Blueprint('settings', __name__, template_folder='templates')



@settings.route('/settingsform') #done
def settingsform():
	return render_template("settings.html")

#Form class
class UserForm(FlaskForm):
	username = StringField("enter new username")
	password = PasswordField("enter new password")
	email = EmailField("enter new email")
	submit = SubmitField("update")


@settings.route('/updateusername/<int:user_id>', methods=['GET', 'POST']) #done
def updateusername(user_id):
	form = UserForm()
	name_to_update = User.query.get_or_404(user_id)
	if request.method == 'POST':
		name_to_update.username = request.form["username"]
		try:
			db.session.commit()
			flash("Username updated!")
			return render_template("settings.html")
		except:
			flash("error! could not update!")
			return render_template("updateusername.html",form=form,name_to_update=name_to_update)
	else:
		return render_template("updateusername.html", form=form, name_to_update=name_to_update)


@settings.route('/updatepassword/<int:user_id>', methods=['GET', 'POST']) #done
def updatepassword(user_id):
	form = UserForm()
	name_to_update = User.query.get_or_404(user_id)
	if request.method == 'POST':
		passwordstr = request.form["password"]
		password = passwordstr.encode('utf-8')
		bytes = password
		salt = bcrypt.gensalt()
		new_password_hash = bcrypt.hashpw(bytes, salt)
		name_to_update.password_hash = new_password_hash
		try:
			db.session.commit()
			flash("Password updated!")
			return render_template("settings.html")
		except:
			flash("error! could not update!")
			return render_template("updatepassword.html",form=form,name_to_update=name_to_update)
	else:
		return render_template("updatepassword.html", form=form, name_to_update=name_to_update)




@settings.route('/updateemail/<int:user_id>', methods=['GET', 'POST']) #done
def updateemail(user_id):
	form = UserForm()
	name_to_update = User.query.get_or_404(user_id)
	if request.method == 'POST':
		name_to_update.email = request.form["email"]
		try:
			db.session.commit()
			flash("Email updated!")
			return render_template("settings.html")
		except:
			flash("error! could not update!")
			return render_template("updateemail.html",form=form,name_to_update=name_to_update)
	else:
		return render_template("updateemail.html", form=form, name_to_update=name_to_update)
