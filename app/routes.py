import os
from app import app, db
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SearchMovieForm, UserInfoForm, LoginForm
from app.models import User
import tmdbsimple as tmdb
from werkzeug.security import check_password_hash

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')


@app.route('/')
def index():
    form = SearchMovieForm()
    return render_template('index.html', form=form)


@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchMovieForm()
    search = tmdb.Search()
    results = None
    if request.method == 'POST' and form.validate():
        print("HERE")
        title = form.title.data
        response = search.movie(query=title)
        results = search.results
        
    return render_template('search.html', form=form, results=results)


@app.route('/movies/<int:id>')
def movie_detail(id):
    movie = tmdb.Movies(id).info()
    return render_template('movie_detail.html', movie=movie)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(username, email, password)
        
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
        next_page = request.args.get('next')
        if next_page:
            return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have succesfully logged out", 'primary')
    return redirect(url_for('index'))


@app.route('/watchlist')
@login_required
def watchlist():
    watch_list = [tmdb.Movies(m_id).info() for m_id in current_user.watchlist]
    return render_template('watchlist.html', watch_list=watch_list)


@app.route('/add-to-watchlist/<int:movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    current_user.add_to_watchlist(movie_id)
    return redirect(url_for('watchlist'))