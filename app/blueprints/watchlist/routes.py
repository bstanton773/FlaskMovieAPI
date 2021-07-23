from . import bp as watchlist
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.auth.models import User
import tmdbsimple as tmdb


@watchlist.route('/my-watchlist')
@login_required
def my_watchlist():
    watch_list = [tmdb.Movies(m_id).info() for m_id in current_user.watchlist]
    return render_template('watchlist.html', watch_list=watch_list, user=current_user)


@watchlist.route('/watchlist/<int:user_id>')
@login_required
def follower_watchlist(user_id):
    user = User.query.get_or_404(user_id)
    watch_list = [tmdb.Movies(m_id).info() for m_id in user.watchlist]
    return render_template('watchlist.html', watch_list=watch_list, user=user)


@watchlist.route('/compare-watchlist/<int:user_id>')
@login_required
def compare_watchlist(user_id):
    user = User.query.get_or_404(user_id)
    combined_watch_list = set(user.watchlist) & set(current_user.watchlist)
    watch_list = [tmdb.Movies(m_id).info() for m_id in combined_watch_list]
    return render_template('watchlist.html', watch_list=watch_list, user=user)


@watchlist.route('/add-to-watchlist/<int:movie_id>', methods=['POST'])
@login_required
def add_to_watchlist(movie_id):
    current_user.add_to_watchlist(movie_id)
    return redirect(url_for('watchlist.my_watchlist'))


@watchlist.route('/remove-from-watchlist/<int:movie_id>', methods=['POST'])
@login_required
def remove_from_watchlist(movie_id):
    current_user.remove_from_watchlist(movie_id)
    return redirect(url_for('watchlist.my_watchlist'))
