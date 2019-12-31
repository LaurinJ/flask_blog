from flask import Flask
from flask import render_template, url_for, request, redirect, flash,session
from mdblog.models import db, Article
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, IntegerField, SubmitField, FileField, SelectField, widgets
from wtforms import TextAreaField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo
from werkzeug.utils import secure_filename
from mdblog.models import Article, Newletter, Message, User

import os

flask_app = Flask(__name__)
flask_app.config.from_pyfile("/vagrant/configs/default.py")
db.init_app(flask_app)


class ArticleForm(FlaskForm):
    title = StringField("title", validators=[InputRequired()])
    content = TextAreaField("content", validators=[InputRequired()])
    reading_time = IntegerField("reading_time", widget=widgets.Input(input_type="number") , validators=[InputRequired()])
    category = SelectField("category", choices=[("Events", "Events"), ("Politics", "Politics"), ("Business", "Business"),
                                                ("Health", "Health"), ("Desing", "Desing"), ("Sport", "Sport")])
    image = FileField("image", validators=[FileRequired()])
    submit = SubmitField("Save")

class NewsletterForm(FlaskForm):
    email = StringField("email", widget=widgets.Input(input_type="email"),
                        render_kw=dict(class_="form-control", placeholder="Enter your email"),
                        validators=[InputRequired(), Email()])

class ContactForm(FlaskForm):
    first_name = StringField("First Name", render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired()])
    last_name = StringField("Last Name", render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired()])
    email = StringField("Email Address", widget=widgets.Input(input_type="email"),
                        render_kw=dict(class_ = "form-control form-control-lg"), validators=[InputRequired(), Email()])
    tel_number = IntegerField("Tel. Number", render_kw=dict(class_ = "form-control form-control-lg"),
                              widget=widgets.Input(input_type="number"), validators=[InputRequired()])
    message = TextAreaField("Message", render_kw=dict(class_ = "form-control", cols="30", rows="10"), validators=[InputRequired()])
    submit = SubmitField("Send Message", render_kw=dict(class_ = "btn btn-primary py-3 px-5"))

class LoginForm(FlaskForm):
    username = StringField("Username", render_kw=dict(placeholder = "Username"), validators=[InputRequired()])
    password = PasswordField("Password", render_kw=dict(placeholder = "Password"), validators=[InputRequired()])
    submit = SubmitField("Login", render_kw=dict(class_ = "button"))

class RegisterForm(FlaskForm):
    username = StringField("Username", render_kw=dict(placeholder = "Username"), validators=[InputRequired()])
    password = PasswordField("Password", render_kw=dict(placeholder = "Password"), validators=[InputRequired()])
    confirm_password = PasswordField("Confirm_password",  render_kw=dict(placeholder = "Confirm password"),
                                      validators=[InputRequired(), EqualTo("password")])
    email = StringField("Email", render_kw=dict(placeholder = "Email"), validators=[InputRequired(), Email()])
    submit = SubmitField("Register", render_kw=dict(class_ = "button"))

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old password", render_kw=dict(placeholder="Old password"), validators=[InputRequired()])
    new_password = PasswordField("New password", render_kw=dict(placeholder="New password"), validators=[InputRequired()])
    submit = SubmitField("Change", render_kw=dict(class_="button"))

class ChangeImageForm(FlaskForm):
    image = FileField("New image", validators=[FileRequired()])
    submit = SubmitField("Change", render_kw=dict(class_="button"))

@flask_app.route("/")
def index():
    page = request.args.get("page", 1, int)
    editors = Article.query.order_by(Article.id.desc()).limit(7)
    # trends = Article.query.order_by(Article.id.desc()).limit(4)
    politics = Article.query.filter_by(category="Politics").order_by(Article.id.desc()).limit(3)
    business = Article.query.filter_by(category="Business").order_by(Article.id.desc()).limit(3)
    paginate = Article.query.order_by(Article.id.desc()).paginate(page, 3, False)
    return render_template("home.html", politics=politics, business=business,
                           new_articles=paginate.items, paginate=paginate, editors=editors)

@flask_app.route("/add/", methods=["GET", "POST"])
def add():
    form = ArticleForm()
    if form.validate_on_submit():
        file = form.image.data
        name = secure_filename(file.filename)
        file.save(os.path.join(flask_app.config["UPLOAD_FOLDER"], name))
        article = Article(
            title = form.title.data,
            content = form.content.data,
            reading_time = form.reading_time.data,
            category = form.category.data,
            image = name
        )
        db.session.add(article)
        db.session.commit()
        flash("Successful", "alert alert-success text-center")
        return render_template("add.html", form=form)
    return render_template("add.html", form=form)

@flask_app.route("/article/<int:art_id>/", methods=["GET"])
def view_article(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("article_single.html", article=article)
    return redirect(url_for("index"))

@flask_app.route("/category/", methods=["GET"])
def view_category():
    category = request.args.get("category", "New", str)
    page = request.args.get("page", 1, int)
    if category == "New":
        paginate = Article.query.order_by(Article.id.desc()).paginate(page, 8, False)
    else:
        paginate = Article.query.filter_by(category=category).order_by(Article.id.desc()).paginate(page, 8, False)
    if paginate:
        return render_template("category.html", articles=paginate.items, paginate=paginate, title=category)
    return redirect(url_for("index"))

@flask_app.route("/newletter/", methods=["POST"])
def new_letter():
    form = NewsletterForm()
    if form.validate_on_submit():
        email = Newletter.query.filter_by(email=form.email.data).first()
        if email:
            flash("Email is busy")
            return redirect(url_for("index"))
        newletter = Newletter(email = form.email.data)
        db.session.add(newletter)
        db.session.commit()
        flash("New letter successful", "alert alert-success text-center")
        return redirect(url_for("index"))
    return redirect(url_for("index"))

@flask_app.route("/contact/", methods=["GET", "POST"])
def view_contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(first_name = form.first_name.data,
                          last_name = form.last_name.data,
                          email = form.email.data,
                          tel_number = form.tel_number.data,
                          message = form.message.data)
        db.session.add(message)
        db.session.commit()
        flash("The query is sent", "alert alert-success text-center")
        return redirect(url_for("view_contact"))
    return render_template("contact.html", form=form)

@flask_app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.get_password(form.password.data):
            session["user"] = form.username.data
            flash("You have successfully logged", "alert alert-success text-center")
            return redirect(url_for("index"))
        flash("Username or password is wrong", "alert alert-danger text-center")
    return render_template("login.html", form=form)

@flask_app.route("/logout/", methods=["GET"])
def logout():
    if "user" in session:
        session.pop("user")
        return redirect(url_for("login"))
    return redirect(url_for("login"))

@flask_app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("Username is busy","alert alert-danger text-center")
            return render_template("register.html", form=form)
        user = User(username = form.username.data,
                    email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered", "alert alert-success text-center")
        return redirect(url_for("login"))
    else:
        for field, error in form.errors.items():
            flash("{} -- {}".format(field, error), "alert alert-danger text-center")
            return render_template("register.html", form=form)
    return render_template("register.html", form=form)

@flask_app.route("/change_password/", methods=["GET", "POST"])
def change_password():
    if "user" not in session:
        return redirect(url_for("login"))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        username = "admin"
        user = User.query.filter_by(username=username).first()
        if user and user.get_password(form.old_password.data):
            user.set_password(form.new_password.data)
            print(user.username)
            db.session.add(user)
            db.session.commit()
            flash("Password successfully changed", "alert alert-success text-center")
            return redirect(url_for("view_admin"))
        flash("Old password is wrong", "alert alert-danger text-center")
    return render_template("change_password.html", form=form)

@flask_app.route("/admin/", methods=["GET"])
def view_admin():
    page = request.args.get("page", 1, int)
    user = User.query.filter_by(username=session["user"]).first()
    paginate = Article.query.filter_by(user_id=user.id).order_by(Article.id.desc()).paginate(page, 8, False)
    return render_template("view_admin.html", articles=paginate.items, paginate=paginate)

@flask_app.route("/change_image/", methods=["GET", "POST"])
def change_image():
    form = ChangeImageForm()
    user = User.query.filter_by(username=session["user"]).first()
    if form.validate_on_submit() and user:
        image = form.image.data
        image_name = secure_filename(image.filename)
        name = str(user.id) + user.username + image_name
        print(name)
        user.image = name
        db.session.commit()
        image.save(os.path.join(flask_app.config["UPLOAD_PROFILE_FOLDER"], name))
        flash("Profile image successfully changed", "alert alert-success text-center")
        return redirect(url_for("view_admin"))
    return render_template("change_profile_image.html", form=form, current_user=user)

@flask_app.context_processor
def con_form_tre():
    form1 = NewsletterForm()
    trends = Article.query.order_by(Article.id.desc()).limit(4)
    return {"trends": trends, "form1": form1}