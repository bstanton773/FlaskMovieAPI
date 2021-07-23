from . import bp as movies
from flask import render_template
from flask_login import current_user
import tmdbsimple as tmdb
from app.blueprints.ratings.forms import RatingForm

@movies.route('/<int:id>')
def movie_detail(id):
    movie = tmdb.Movies(id).info()
    form = RatingForm()
    user_ratings = []
    if current_user.is_authenticated:
        user_ratings = [r.movie_id for r in current_user.ratings]
    return render_template('movie_detail.html', movie=movie, form=form, user_ratings=user_ratings)