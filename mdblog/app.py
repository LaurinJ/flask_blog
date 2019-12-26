from flask import Flask
from flask import render_template, url_for, flash
from mdblog.models import db, Article
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, IntegerField, SubmitField, FileField, SelectField, widgets, TextAreaField
from wtforms.validators import InputRequired
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

@flask_app.route("/")
def index():
    image = url_for("static", filename="images/big_img_1.jpg")
    politics = Article.query.filter_by(category="Politics").paginate(1, 3, False)
    business = Article.query.filter_by(category="Business").paginate(1, 3, False)
    return render_template("home.html", image=image, politics=politics.items, business=business.items)

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