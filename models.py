from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(50), default='active')
    reset_token = db.Column(db.String(100), nullable=True)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, default=0.0)
    cover = db.Column(db.String(255), nullable=True)
    pdfs = db.Column(db.String(255), nullable=True)
    total_pages = db.Column(db.Integer, default=0)


class ReadingProgress(db.Model):
    __tablename__ = 'reading_progress'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    current_page = db.Column(db.Integer, default=1)
    total_pages = db.Column(db.Integer, default=0)

class Profile(db.Model):
    __tablename__ = 'profile'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    profile_photo = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)

class ContactUs(db.Model):
    __tablename__ = 'contact_us'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user_email = db.Column(db.String(150), primary_key=True)
    problem = db.Column(db.Text, primary_key=True)

class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    activity_type = db.Column(db.String(100), primary_key=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, primary_key=True)

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    badge_name = db.Column(db.String(100), primary_key=True)
    badge_icon = db.Column(db.String(255), nullable=True)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, accepted, declined
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_requests')

class ReadingInvite(db.Model):
    __tablename__ = 'reading_invites'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    book = db.relationship('Book', foreign_keys=[book_id])
