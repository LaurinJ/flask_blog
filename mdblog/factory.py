from flask import Flask
from .models import db, Article
from flask import render_template
from .mod_main.forms import SearchForm, NewsletterForm
from mdblog import login_manager

from .mod_admin import admin
from .mod_blog import blog
from .mod_main import main

import os

def create_flask_app():
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile("/vagrant/configs/default.py")
    db.init_app(flask_app)

    login_manager.init_app(flask_app)
    flask_app.register_blueprint(admin)
    flask_app.register_blueprint(blog)
    flask_app.register_blueprint(main)

    @flask_app.errorhandler(404)
    def error_404(error):
        return render_template("404.html"), 404

    @flask_app.context_processor
    def con_form_tre():
        form_search = SearchForm()
        form_new_email = NewsletterForm()
        trends = Article.query.order_by(Article.id.desc()).limit(4)
        return {"trends": trends, "form_new_email": form_new_email, "form_search": form_search}

    return flask_app