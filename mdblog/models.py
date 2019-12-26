from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import current_timestamp

db = SQLAlchemy()

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String, nullable=False)
    content = db.Column( db.String, nullable=False)
    category = db.Column(db.String, nullable=False, default="Events")
    image = db.Column(db.String, default="default.jpg")
    reading_time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.Integer, default=current_timestamp())