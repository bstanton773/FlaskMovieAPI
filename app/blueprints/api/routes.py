from app.blueprints.auth.models import User
from app.blueprints.movies.wrappers import MovieRankings
from . import bp as api
from flask import jsonify, request, url_for
from app.blueprints.api.http_auth import basic_auth, token_auth

@api.route('/')
@basic_auth.login_required
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Welcome to the API'
    })

###################
# API USER ROUTES #
###################

# Get all users
@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


# Get single user
@api.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    return jsonify(user.to_dict())


# Create new user
@api.route('/users', methods=['POST'])
def creat_user():
    data = request.json
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing data'
        }), 400
    username = data['username']
    email = data['email']
    password = data['password']
    check_user = User.query.filter((User.username==username)|(User.email==email)).first()
    if check_user:
        return jsonify({
            'status': 'error',
            'message': 'User already exists'
        }), 400
    new_user = User(username, email, password)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


# Update user
@api.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    data = request.json
    user.from_dict(data)
    user.save()
    return jsonify(user.to_dict())

# Delete user
@api.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'User not found'
        }), 404
    user.delete()
    return jsonify({
        'status': 'ok',
        'message': 'User deleted'
    })

# Get token
@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({
        'token': token,
        'token_expiration': user.token_expiration
        })


# Get me
@api.route('/me')
@token_auth.login_required
def get_me():
    user = token_auth.current_user()
    return jsonify(user.to_dict())

####################
# API MOVIE ROUTES #
####################

# Movie Wrapper
movie_rank = MovieRankings()

# Main Movie route
@api.route('/movies', methods=['GET'])
def get_movies():
    data = request.args
    search = data.get('search', '')
    page = int(data.get('page', 1)) - 1
    providers = data.get('providers', '').split(', ')
    genres = data.get('genres', '').split(', ')
    min_year = data.get('minYear', '1960')
    max_year = data.get('maxYear', '2021')
    sort_by = data.get('sortBy', 'rating@ASC')
    years = [y for y in range(int(min_year), int(max_year)+1)]
    movies = movie_rank.search_all(q=search, providers=providers, genres=genres, years=years, skip=page, sort=sort_by)[0]
    return jsonify(movies)


# Get single movie
@api.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie_info = movie_rank.get_movie_info(movie_id)
    if not movie_info:
        return jsonify({
            'status': 'error',
            'message': 'Movie not found'
        }), 404
    movie = {
        'movie_info': movie_info[0],
        'providers': movie_info[1],
        'recommendations': movie_info[2]
    }
    return jsonify(movie)


########################
# API WATCHLIST ROUTES #
########################

@api.route('/watchlist')
@token_auth.login_required
def get_watchlist():
    current_user = token_auth.current_user()
    watch_list = [movie_rank.get_movie_info(m_id)[0] for m_id in current_user.watchlist]
    return jsonify(watch_list)


@api.route('/add-to-watchlist/<int:movie_id>', methods=['POST'])
@token_auth.login_required
def add_to_watchlist(movie_id):
    current_user = token_auth.current_user()
    current_user.add_to_watchlist(movie_id)
    return jsonify({
            'status': 'success',
            'message': 'Your watchlist has been updated'
        })


@api.route('/remove-from-watchlist/<int:movie_id>', methods=['DELETE'])
@token_auth.login_required
def remove_from_watchlist(movie_id):
    current_user = token_auth.current_user()
    current_user.remove_from_watchlist(movie_id)
    return jsonify({
            'status': 'success',
            'message': 'Your watchlist has been updated'
        })


########################
# API RATINGS ROUTES #
########################

@api.route('/my-ratings')
@token_auth.login_required
def get_my_ratings():
    current_user = token_auth.current_user()
    my_ratings = [movie_rank.get_movie_info(r.movie_id)[0] for r in current_user.ratings]
    for movie in range(len(my_ratings)):
        my_ratings[movie]['rating'] = current_user.ratings[movie].rating
    my_ratings = sorted(my_ratings, key=lambda x: x['rating'], reverse=True)
    return jsonify(my_ratings)


@api.route('/add-to-my-ratings/<int:movie_id>', methods=['POST'])
@token_auth.login_required
def add_to_my_ratings(movie_id):
    current_user = token_auth.current_user()
    current_user.add_to_my_ratings(movie_id)
    return jsonify({
            'status': 'success',
            'message': 'Your my-ratings has been updated'
        })


@api.route('/remove-from-my-ratings/<int:movie_id>', methods=['DELETE'])
@token_auth.login_required
def remove_from_my_ratings(movie_id):
    current_user = token_auth.current_user()
    current_user.remove_from_my_ratings(movie_id)
    return jsonify({
            'status': 'success',
            'message': 'Your my-ratings has been updated'
        })
