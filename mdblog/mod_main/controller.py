from flask import Blueprint, request, redirect, render_template, url_for, flash
from mdblog.models import db, Article, Newletter, Message
from .forms import NewsletterForm, SearchForm, ContactForm

main = Blueprint("main", __name__)

@main.route("/")
def index():
    page = request.args.get("page", 1, int)
    editors = Article.query.order_by(Article.id.desc()).limit(7)
    # trends = Article.query.order_by(Article.id.desc()).limit(4)
    politics = Article.query.filter_by(category="Politics").order_by(Article.id.desc()).limit(3)
    business = Article.query.filter_by(category="Business").order_by(Article.id.desc()).limit(3)
    paginate = Article.query.order_by(Article.id.desc()).paginate(page, 3, False)
    return render_template("mod_main/home.html", politics=politics, business=business,
                           new_articles=paginate.items, paginate=paginate, editors=editors)

@main.route("/search/", methods=["GET", "POST"])
def search():
    page = request.args.get("page", 1, int)
    search_get = request.args.get("search", False, str)
    form = SearchForm()
    tag = form.search.data
    if tag:
        search = "%{}%".format(tag)
    else:
        tag = search_get
        search = "%{}%".format(search_get)
    paginate = Article.query.filter(Article.title.like(search)).paginate(page, 8, False)
    if paginate:
        return render_template("mod_main/view_search.html", articles=paginate.items, paginate=paginate, search=tag)
    return redirect(url_for("error_404"))

@main.route("/newletter/", methods=["POST"])
def new_letter():
    form = NewsletterForm()
    if form.validate_on_submit():
        email = Newletter.query.filter_by(email=form.email.data).first()
        if email:
            flash("Email is busy")
            return redirect(url_for("main.index"))
        newletter = Newletter(email = form.email.data)
        db.session.add(newletter)
        db.session.commit()
        flash("New letter successful", "alert alert-success text-center")
        return redirect(url_for("main.index"))
    return redirect(url_for("main.index"))

@main.route("/contact/", methods=["GET", "POST"])
def view_contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = Message(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          email=form.email.data,
                          tel_number=form.tel_number.data,
                          message=form.message.data)
        db.session.add(message)
        db.session.commit()
        flash("The query is sent", "alert alert-success text-center")
        return redirect(url_for("main.view_contact"))
    return render_template("mod_main/contact.html", form=form)