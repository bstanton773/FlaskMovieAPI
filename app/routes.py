import os
from flask import current_app as app, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.forms import SearchMovieForm, SearchUserForm
from app.blueprints.auth.models import User
from app.blueprints.ratings.forms import RatingForm
from app.wrappers import MovieRankings
import tmdbsimple as tmdb


tmdb.API_KEY = os.environ.get('TMDB_API_KEY')
movie_rank = MovieRankings()

# MAIN

@app.route('/', methods=['GET', 'POST'])
def index():
    movies = movie_rank.search_all(q='')[0]
    form = SearchMovieForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        providers = '@'.join(form.providers.data)
        genres = '@'.join(form.genres.data)
        runtime = form.runtime.data
        ratingrange = f'{form.rating.data}@100'
        movies = movie_rank.search_all(q=title, providers=providers, genres=genres, runtime=runtime, ratingrange=ratingrange)[0]
    return render_template('index.html', form=form, movies=movies)


# Movie
@app.route('/movies/<int:id>')
def movie_detail(id):
    movie = tmdb.Movies(id).info()
    form = RatingForm()
    user_ratings = []
    if current_user.is_authenticated:
        user_ratings = [r.movie_id for r in current_user.ratings]
    return render_template('movie_detail.html', movie=movie, form=form, user_ratings=user_ratings)



@app.route('/search-users', methods=['GET','POST'])
@login_required
def search_users():
    form = SearchUserForm()
    users = current_user.followed.all()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        search = f"%{username}%"
        users = User.query.filter(User.username.ilike(search)).all()
        
    return render_template('search_users.html', form=form, users=users)


@app.route('/follow')
@login_required
def follow():
    user_id = request.args.get('user_id')
    u = User.query.get(user_id)

    current_user.follow(u)
    flash(f'You have followed {u.username}', 'success')
    return redirect(url_for('search_users'))


@app.route('/unfollow')
@login_required
def unfollow():
    user_id = request.args.get('user_id')
    u = User.query.get(user_id)

    current_user.unfollow(u)
    flash(f'You have unfollowed {u.username}', 'info')
    return redirect(url_for('search_users'))


# @app.route('/following')
# def following():
#     users = current_user.followed.all()
#     return render_template('search_users')

########################
# I think this can go! #
########################    
# @app.route('/search', methods=['GET','POST'])
# def search():
#     form = SearchMovieForm()
#     results = None
#     if request.method == 'POST' and form.validate():
#         title = form.title.data
#         results = movie_rank.search_all(q=title)[0]
#     return render_template('search.html', form=form, results=results)