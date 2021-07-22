import os
from app import db
from flask import current_app as app, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SearchMovieForm, SearchUserForm, UserInfoForm, LoginForm, RatingForm
from app.models import User, Rating
from app.wrappers import MovieRankings
import tmdbsimple as tmdb
from werkzeug.security import check_password_hash

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

# Movie
@app.route('/movies/<int:id>')
def movie_detail(id):
    movie = tmdb.Movies(id).info()
    form = RatingForm()
    user_ratings = []
    if current_user.is_authenticated:
        user_ratings = [r.movie_id for r in current_user.ratings]
    return render_template('movie_detail.html', movie=movie, form=form, user_ratings=user_ratings)

# Auth
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(username, email, password)
        check_user = User.query.filter((User.username==username)|(User.email==email)).first()
        if check_user:
            flash("That username or email is already in use", 'warning')
            return redirect('signup')
        # create a new instance of User
        new_user = User(username, email, password)
        # add new instance to our database
        db.session.add(new_user)
        # commit database
        db.session.commit()

        # Send email to new user

        flash("You have succesfully signed up!", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Email/Password. Please try again", 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        # next_page = request.args.get('next')
        # if next_page:
        #     return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have succesfully logged out", 'primary')
    return redirect(url_for('index'))

# Watchlist
@app.route('/watchlist')
@login_required
def watchlist():
    watch_list = [tmdb.Movies(m_id).info() for m_id in current_user.watchlist]
    return render_template('watchlist.html', watch_list=watch_list)


@app.route('/watchlist/<int:user_id>')
@login_required
def follower_watchlist(user_id):
    user = User.query.get_or_404(user_id)
    watch_list = [tmdb.Movies(m_id).info() for m_id in user.watchlist]
    return render_template('watchlist.html', watch_list=watch_list, user=user)


@app.route('/compare-watchlist/<int:user_id>')
@login_required
def compare_watchlist(user_id):
    user = User.query.get_or_404(user_id)
    combined_watch_list = set(user.watchlist) & set(current_user.watchlist)
    watch_list = [tmdb.Movies(m_id).info() for m_id in combined_watch_list]
    return render_template('watchlist.html', watch_list=watch_list, user=user)


@app.route('/add-to-watchlist/<int:movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    current_user.add_to_watchlist(movie_id)
    return redirect(url_for('watchlist'))


@app.route('/remove-from-watchlist/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_watchlist(movie_id):
    current_user.remove_from_watchlist(movie_id)
    return redirect(url_for('watchlist'))

# Ratings
@app.route('/my-ratings')
@login_required
def my_ratings():
    my_ratings = [tmdb.Movies(r.movie_id).info() for r in current_user.ratings]
    for movie in range(len(my_ratings)):
        my_ratings[movie]['rating'] = current_user.ratings[movie].rating
    my_ratings = sorted(my_ratings, key=lambda x: x['rating'], reverse=True)
    return render_template('ratings.html', my_ratings=my_ratings, user=current_user)


@app.route('/ratings/<int:user_id>')
@login_required
def follower_ratings(user_id):
    user = User.query.get_or_404(user_id)
    my_ratings = [tmdb.Movies(r.movie_id).info() for r in user.ratings]
    for movie in range(len(my_ratings)):
        my_ratings[movie]['rating'] = user.ratings[movie].rating
    my_ratings = sorted(my_ratings, key=lambda x: x['rating'], reverse=True)
    return render_template('ratings.html', my_ratings=my_ratings, user=user)


@app.route('/add-to-my-ratings/<int:movie_id>', methods=['POST'])
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

    return redirect(url_for('my_ratings'))


@app.route('/remove-from-my-ratings/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_my_ratings(movie_id):
    rating = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    if not rating:
        flash("You are not the owner of this rating", 'danger')
        return redirect(url_for('my_ratings'))
    db.session.delete(rating)
    db.session.commit()
    return redirect(url_for('my_ratings'))


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