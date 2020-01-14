from flask import Blueprint
from flask import render_template, redirect, url_for, session, flash, request
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required

from mdblog.models import User, db, Article, Message

from .forms import LoginForm, RegisterForm, ChangeImageForm, ChangePasswordForm, ArticleForm
from werkzeug.utils import secure_filename

from configs.default import UPLOAD_PROFILE_FOLDER, UPLOAD_FOLDER
from .utils import save_image
import os

admin = Blueprint("admin", __name__)


@admin.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.get_password(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            flash("You have successfully logged", "alert alert-success text-center")
            return redirect(next_page or url_for("admin.view_admin"))
        flash("Username or password is wrong", "alert alert-danger text-center")
    return render_template("mod_admin/login.html", form=form)

@admin.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))

@admin.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered", "alert alert-success text-center")
        return redirect(url_for("admin.login"))
    else:
        flash("Invalid register", "alert alert-danger text-center")
        return render_template("mod_admin/register.html", form=form)
    return render_template("mod_admin/register.html", form=form)

@admin.route("/change_password/", methods=["GET", "POST"])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user and user.get_password(form.old_password.data):
            user.set_password(form.new_password.data)
            print(user.username)
            db.session.add(user)
            db.session.commit()
            flash("Password successfully changed", "alert alert-success text-center")
            return redirect(url_for("admin.view_admin"))
        flash("Old password is wrong", "alert alert-danger text-center")
    return render_template("mod_admin/change_password.html", form=form)

@admin.route("/change_image/", methods=["GET", "POST"])
@login_required
def change_image():
    form = ChangeImageForm()
    if form.validate_on_submit():
        picture_file = save_image(form.image.data)
        current_user.image = picture_file
        db.session.commit()
        flash("Profile image successfully changed", "alert alert-success text-center")
        return redirect(url_for("admin.view_admin"))
    return render_template("mod_admin/change_profile_image.html", form=form)

@admin.route("/add/", methods=["GET", "POST"])
@login_required
def add():
    form = ArticleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user:
            file = form.image.data
            name = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, name))
            article = Article(
                user_id = current_user.id,
                title = form.title.data,
                content = form.content.data,
                reading_time = form.reading_time.data,
                category = form.category.data,
                image = name
            )
            db.session.add(article)
            db.session.commit()
            flash("Successful", "alert alert-success text-center")
            return render_template("mod_admin/add.html", form=form)
        return redirect(url_for("admin.login"))
    return render_template("mod_admin/add.html", form=form)

@admin.route("/admin/", methods=["GET"])
@login_required
def view_admin():
    page = request.args.get("page", 1, int)
    user = User.query.filter_by(username=current_user.username).first()
    paginate = Article.query.filter_by(user_id=user.id).order_by(Article.id.desc()).paginate(page, 8, False)
    return render_template("mod_admin/view_admin.html", articles=paginate.items, paginate=paginate)

@admin.route("/email_posts/", methods=["GET"])
@login_required
def view_email_posts():
    page = request.args.get("page", 1, int)
    paginate = Message.query.order_by(Message.id.desc()).paginate(page, 10, False)
    return render_template("mod_admin/email_post.html", posts=paginate.items, paginate=paginate, count=paginate.total)