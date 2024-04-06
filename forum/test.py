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



test = Blueprint('test', __name__, template_folder='templates')



@test.route('/test') #done
def testit():
	return render_template("login.html")