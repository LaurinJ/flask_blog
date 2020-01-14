from flask import Blueprint, redirect, request, render_template, url_for
from mdblog.models import Article, User

blog = Blueprint("blog", __name__)

@blog.route("/article/<int:art_id>/", methods=["GET"])
def view_article(art_id):
    article = Article.query.filter_by(id=art_id).first()
    if article:
        return render_template("mod_blog/article_single.html", article=article)
    return redirect(url_for("index"))

@blog.route("/category/", methods=["GET"])
def view_category():
    category = request.args.get("category", "New", str)
    page = request.args.get("page", 1, int)
    if category == "New":
        paginate = Article.query.order_by(Article.id.desc()).paginate(page, 8, False)
    else:
        paginate = Article.query.filter_by(category=category).order_by(Article.id.desc()).paginate(page, 8, False)
    if paginate:
        return render_template("mod_blog/category.html", articles=paginate.items, paginate=paginate, title=category)
    return redirect(url_for("mod_main/index"))

@blog.route("/author/", methods=["GET"])
def view_author():
    author = request.args.get("author", False, str)
    page = request.args.get("page", 1, int)
    user = User.query.filter_by(username=author).first()
    if author and user:
        paginate = Article.query.filter_by(user_id=user.id).order_by(Article.id.desc()).paginate(page, 8, False)
        return render_template("mod_blog/author_articles.html", articles=paginate.items, paginate=paginate, title=author)
    return render_template("404.html")