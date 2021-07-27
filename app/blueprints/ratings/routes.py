from . import bp as ratings
from app import db
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import RatingForm
from .models import Rating
from app.blueprints.auth.models import User
import tmdbsimple as tmdb


# Ratings
@ratings.route('/my-ratings')
@login_required
def my_ratings():
    my_ratings = [tmdb.Movies(r.movie_id).info() for r in current_user.ratings]
    for movie in range(len(my_ratings)):
        my_ratings[movie]['rating'] = current_user.ratings[movie].rating
    my_ratings = sorted(my_ratings, key=lambda x: x['rating'], reverse=True)
    return render_template('ratings.html', my_ratings=my_ratings, user=current_user)


@ratings.route('/ratings/<int:user_id>')
@login_required
def follower_ratings(user_id):
    user = User.query.get_or_404(user_id)
    my_ratings = [tmdb.Movies(r.movie_id).info() for r in user.ratings]
    for movie in range(len(my_ratings)):
        my_ratings[movie]['rating'] = user.ratings[movie].rating
    my_ratings = sorted(my_ratings, key=lambda x: x['rating'], reverse=True)
    return render_template('ratings.html', my_ratings=my_ratings, user=user)


@ratings.route('/add-to-my-ratings/<int:movie_id>', methods=['POST'])
@login_required
def add_to_my_ratings(movie_id):
    form = RatingForm()
    if form.validate():
        rating = form.rating.data
        already_rated = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
        if already_rated:
            already_rated.rating = rating
        else:
            new_rating = Rating(current_user.id, movie_id, rating)
            db.session.add(new_rating)
        db.session.commit()

    return redirect(url_for('ratings.my_ratings'))


@ratings.route('/remove-from-my-ratings/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_my_ratings(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    if not rating:
        flash("You are not the owner of this rating", 'danger')
        return redirect(url_for('ratings.my_ratings'))
    db.session.delete(rating)
    db.session.commit()
    return redirect(url_for('ratings.my_ratings'))