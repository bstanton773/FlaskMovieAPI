from app import db
from datetime import datetime


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

    def to_dict(self):
        return {
            'id': self.id,
            'movie_id': self.movie_id,
            'rating': self.rating
        }