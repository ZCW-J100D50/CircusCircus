from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Blogposts(db.Model):

    id = db.Column(db.INTEGER, primary_key=True)
    created = db.Column(db.DateTime)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.String(120), nullable=False)

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