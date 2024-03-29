from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import Flask
from forum import app as forum
from flask_blog import app1 as blog
from werkzeug.exceptions import NotFound

app = Flask(__name__)




app.wsgi_app = DispatcherMiddleware(forum.app, {
    '/blog': blog.app
})

if __name__ == "__main__":
    app.run()
