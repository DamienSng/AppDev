from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    username = db.Column(db.String(150), unique=True, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    preferences = db.relationship('Preference', backref='user', passive_deletes=True)

    def get_id(self):
        return self.username


class Staff(db.Model, UserMixin):
    __tablename__ = 'staff'
    username = db.Column(db.String(150), unique=True, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    def get_id(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String(150), db.ForeignKey('user.username', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String(150), db.ForeignKey('user.username', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.String(150), db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.String(150), db.ForeignKey('user.username', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.String(150), db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Preference(db.Model):
    username = db.Column(db.String(150), db.ForeignKey('user.username', ondelete="CASCADE"), primary_key=True, nullable=False)
    top_preferences = db.Column(db.String(150), nullable=False)
    top_cuisines = db.Column(db.String(150), nullable=False)
    dietary_restrictions = db.Column(db.String(150), nullable=False)
