from app import db, login
# from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
# from flask_login import UserMixin
# from flask_sqlalchemy import BaseQuery


# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )


# @login.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# class UserQuery(BaseQuery):
#     # def get_active(self):
#     #     return self.filter(self.username=='bstanton773')
#     pass

# class User(db.Model, UserMixin):
#     query_class = UserQuery
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), nullable=False, unique=True)
#     email = db.Column(db.String(150), nullable=False, unique=True)
#     password = db.Column(db.String(256), nullable=False)
#     watchlist = db.Column(db.ARRAY(db.Integer), default=[])
#     ratings = db.relationship('Rating', backref='user', lazy=True)
#     followed = db.relationship(
#         'User', secondary=followers,
#         primaryjoin=(followers.c.follower_id == id),
#         secondaryjoin=(followers.c.followed_id == id),
#         backref=db.backref('followers', lazy='dynamic'),
#         lazy='dynamic'
#     )

#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.password = generate_password_hash(password)

#     def __repr__(self):
#         return f'<User {self.id} | {self.username} >'

#     def follow(self, user):
#         if not self.is_following(user):
#             self.followed.append(user)
#             db.session.commit()

#     def unfollow(self, user):
#         if self.is_following(user):
#             self.followed.remove(user)
#             db.session.commit()

#     def is_following(self, user):
#         return self.followed.filter(followers.c.followed_id == user.id).count() > 0

#     def add_to_watchlist(self, movie_id):
#         if movie_id not in self.watchlist:
#             self.watchlist = self.watchlist + [movie_id]
#             db.session.commit()

#     def remove_from_watchlist(self, movie_id):
#         self.watchlist = [m_id for m_id in self.watchlist if m_id != movie_id]
#         db.session.commit()


# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     movie_id = db.Column(db.Integer, nullable=False)
#     rating = db.Column(db.Integer, nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#     def __init__(self, user_id, movie_id, rating):
#         self.user_id = user_id
#         self.movie_id = movie_id
#         self.rating = rating

#     def __repr__(self):
#         return f'<Rating {self.id} | {self.movie_id}>'

