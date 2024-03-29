from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/chatter")
def index():
    return render_template("chatter.html")