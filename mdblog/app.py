from flask import Flask
from flask import render_template, url_for, request, redirect, flash
from mdblog.models import db, Article
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, IntegerField, SubmitField, FileField, SelectField, widgets, TextAreaField
from wtforms.validators import InputRequired, Email
from werkzeug.utils import secure_filename
from mdblog.models import Article

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
                        render_kw=dict(class_="form-control", placeholder="Enter your email"), validators=[InputRequired(), Email()])

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
        flash("Successful")
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


@flask_app.context_processor
def con_form_tre():
    form = NewsletterForm()
    trends = Article.query.order_by(Article.id.desc()).limit(4)
    return {"trends": trends, "form": form}