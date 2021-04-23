from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_login import UserMixin


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    watchlist = db.Column(db.ARRAY(db.Integer), default=[])
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.id} | {self.username} >'

    def add_to_watchlist(self, movie_id):
        if movie_id not in self.watchlist:
            self.watchlist = self.watchlist + [movie_id]
            db.session.commit()

    def remove_from_watchlist(self, movie_id):
        self.watchlist = [m_id for m_id in self.watchlist if m_id != movie_id]
        db.session.commit()


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, user_id, movie_id, rating):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating

    def __repr__(self):
        return f'<Rating {self.id} | {self.movie_id}>'