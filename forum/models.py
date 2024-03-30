
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_bcrypt import Bcrypt
import bcrypt
#import filePath
from flask_login import UserMixin
import datetime

# create db here so it can be imported (with the models) into the App object.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# bcrypt = Bcrypt()

#OBJECT MODELS
class User(UserMixin, db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.LargeBinary(255))
    email = db.Column(db.String(255), unique=True)
    admin = db.Column(db.Boolean, default=False)
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")
    media = db.relationship("Media", backref="user") #establishes images in relation to the user

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.bytes = password.encode('utf-8')
        self.salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(self.bytes, self.salt) #generate_password_hash(password)

    def check_password(self, password):
        check_bytes = password.encode('utf-8')
        return bcrypt.checkpw(check_bytes, self.password_hash)

    def get_id(self):
        return str(self.userID)
    
class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    comments = db.relationship("Comment", backref="post")
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    subforum_id = db.Column(db.Integer, db.ForeignKey('subforum.subID'))
    postdate = db.Column(db.DateTime)
    media = db.relationship("Media", backref="post")

    #cache stuff
    lastcheck = None
    savedresponse = None
    def __init__(self, title, content, postdate):
        self.title = title
        self.content = content
        self.postdate = postdate
    def get_time_string(self):
        #this only needs to be calculated every so often, not for every request
        #this can be a rudamentary chache
        now = datetime.datetime.now()
        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.lastcheck = now
        else:
            return self.savedresponse

        diff = now - self.postdate

        seconds = diff.total_seconds()
        print(seconds)
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.savedresponse = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.savedresponse = "Just a moment ago!"

        return self.savedresponse

class Subforum(db.Model):
    subID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    subforums = db.relationship("Subforum")
    parent_id = db.Column(db.Integer, db.ForeignKey('subforum.subID'))
    posts = db.relationship("Post", backref="subforum")
    path = None
    hidden = db.Column(db.Boolean, default=False)
    def __init__(self, title, description):
        self.title = title
        self.description = description

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    postdate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))

    lastcheck = None
    savedresponse = None
    def __init__(self, content, postdate):
        self.content = content
        self.postdate = postdate
    def get_time_string(self):
        #this only needs to be calculated every so often, not for every request
        #this can be a rudamentary chache
        now = datetime.datetime.now()
        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.lastcheck = now
        else:
            return self.savedresponse

        diff = now - self.postdate
        seconds = diff.total_seconds()
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.savedresponse = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.savedresponse = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.savedresponse = "Just a moment ago!"
        return self.savedresponse


#Define media
class Media(db.Model):
    photoID = db.Column(db.Integer, primary_key=True)
    photoName = db.Column(db.Text)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'))
    filePath = db.Column(db.Text)
    mediaType = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey("post.postID"))

    def __init__(self, name, filepath, media_type):
        self.photoName = name
        self.filePath = filepath
        self.mediaType = media_type


def error(errormessage):
    return "<b style=\"color: red;\">" + errormessage + "</b>"


def generateLinkPath(subforumid):
    links = []
    subforum = Subforum.query.filter(Subforum.subID == subforumid).first()
    parent = Subforum.query.filter(Subforum.subID == subforum.parent_id).first()
    links.append("<a href=\"/subforum?sub=" + str(subforum.subID) + "\">" + subforum.title + "</a>")
    while parent is not None:
        links.append("<a href=\"/subforum?sub=" + str(parent.subID) + "\">" + parent.title + "</a>")
        parent = Subforum.query.filter(Subforum.subID == parent.parent_id).first()
    links.append("<a href=\"/\">Forum Index</a>")
    link = ""
    for l in reversed(links):
        link = link + " / " + l
    return link


#Post checks
def valid_title(title):
    return len(title) > 4 and len(title) < 140
def valid_content(content):
    return len(content) > 10 and len(content) < 5000

#TODO CHECK what should this input be? Is this right?
def valid_media(filepath):
    return filepath.endswith(('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', None))








class Blogposts(db.Model):

    id = db.Column(db.INTEGER, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    lastcheck = None
    savedresponce = None

    def __init__(self, title, content, created):
        self.title = title
        self.content = content
        self.created = created

    def get_time_string(self):
        # this only needs to be calculated every so often, not for every request
        # this can be a rudamentary chache
        now = datetime.datetime.now()


        if self.lastcheck is None or (now - self.lastcheck).total_seconds() > 30:
            self.lastcheck = now
        else:
            return self.savedresponce

        diff = now - self.postdate

        seconds = diff.total_seconds()
        print(seconds)
        if seconds / (60 * 60 * 24 * 30) > 1:
            self.savedresponce = " " + str(int(seconds / (60 * 60 * 24 * 30))) + " months ago"
        elif seconds / (60 * 60 * 24) > 1:
            self.savedresponce = " " + str(int(seconds / (60 * 60 * 24))) + " days ago"
        elif seconds / (60 * 60) > 1:
            self.savedresponce = " " + str(int(seconds / (60 * 60))) + " hours ago"
        elif seconds / (60) > 1:
            self.savedresponce = " " + str(int(seconds / 60)) + " minutes ago"
        else:
            self.savedresponce = "Just a moment ago!"

        return self.savedresponce