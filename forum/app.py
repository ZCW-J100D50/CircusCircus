
from flask import render_template
from flask_login import LoginManager
from flask_mysqldb import MySQL
from forum.models import Subforum, db, User
#from frontend_app import application as frontend

#application = DispatcherMiddleware(frontend, {
#    '/backend': backend
#})


from . import create_app

app = create_app()

app.config['SITE_NAME'] = 'Groove Gathering'
app.config['SITE_DESCRIPTION'] = 'a social dance forum'
app.config['FLASK_DEBUG'] = 1
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'lydia'
# app.config['MYSQL_PASSWORD'] = 'celeste'
# app.config['MYSQL_DB'] = 'flask'


mysql = MySQL(app)
#cursor = mysql.connection.cursor()

app.config['UPLOAD_FOLDER'] = '/path/to/the/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def init_site():
	print("creating initial subforums")
	admin = add_subforum("Forum", "Announcements, bug reports, and general discussion about the forum belongs here")
	add_subforum("Announcements", "View forum announcements here", admin)
	add_subforum("Bug Reports", "Report bugs with the forum here", admin)
	add_subforum("General Discussion", "Use this subforum to post anything you want")
	add_subforum("Other", "Discuss other things here")

def add_subforum(title, description, parent=None):
	sub = Subforum(title, description)
	if parent:
		for subforum in parent.subforums:
			if subforum.title == title:
				return
		parent.subforums.append(sub)
	else:
		subforums = Subforum.query.filter(Subforum.parent_id == None).all()
		for subforum in subforums:
			if subforum.title == title:
				return
		db.session.add(sub)
	print("adding " + title)
	db.session.commit()
	return sub

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	return User.query.get(userid)

with app.app_context():
	db.create_all() # TODO this may be redundant
	if not Subforum.query.all():
		init_site()

@app.route('/')
def index():
	subforums = Subforum.query.filter(Subforum.parent_id == None).order_by(Subforum.subID)
	return render_template("subforums.html", subforums=subforums)




