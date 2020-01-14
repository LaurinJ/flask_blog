from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import current_timestamp
from werkzeug.security import check_password_hash, generate_password_hash
from mdblog import login_manager
from flask_login import UserMixin

db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable=False)
    content = db.Column( db.String, nullable=False)
    category = db.Column(db.String, nullable=False, default="Events")
    image = db.Column(db.String, default="default.jpg")
    reading_time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Integer, default=current_timestamp())

class Newletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    tel_number = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String, nullable=False)
    sending_time = db.Column(db.Integer, default=current_timestamp())
    status = db.Column(db.BOOLEAN, default=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_rel = db.relationship("Article", backref='author')
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String)
    image = db.Column(db.String, default="default.jpg")
    created_at = db.Column(db.DateTime, default=current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)