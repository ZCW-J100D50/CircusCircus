import datetime
from flask import render_template, request, flash, redirect, url_for, Blueprint
#from forum.app import app
from forum.models import DirectMessages, db

messages = Blueprint('messages', __name__, template_folder='templates')



@messages.route('/messages')
def inbox():
    messages = DirectMessages.query.order_by(DirectMessages.id)
    return render_template('messages.html', messages=messages)



