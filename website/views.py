from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Post
from .db_config import CharLimits
from . import db


views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html")


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post(title="", body=""):
    if request.method == "POST":
        data = request.form
        given_title = data.get("title")
        given_body = data.get("body")

        title_limits = CharLimits.post["title"]
        body_limits = CharLimits.post["body"]

        if (len(given_title) < title_limits["min"] or len(given_title) > title_limits["max"]):
            flash(f"Title must be between {title_limits['min']} and {title_limits['max']} characters long.",
                category="error")

        elif (len(given_body) < body_limits["min"] or len(given_body) > body_limits["max"]):
            flash(f"Body must be between {body_limits['min']} and {body_limits['max']} characters long.",
                category="error")

        else:
            new_post = Post(title=given_title, body=given_body, author=current_user)
            db.session.add(new_post)
            db.session.commit()
            flash("Post created.", category="success")
            return redirect(url_for("views.home"))

        return redirect(url_for("views.create_post", title=given_title, body=given_body))

    return render_template(
        "create-post.html",
        title_to_display=request.args.get("title"),
        body_to_display=request.args.get("body"),
    )
