from app.blueprints.auth.models import User
from app.blueprints.movies.wrappers import MovieRankings
from . import bp as api
from flask import jsonify, request, url_for

@api.route('/')
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
    providers = data.get('providers', '')
    genres = data.get('genres', '')
    movies = movie_rank.search_all(q=search, providers=providers.split(', '), genres=genres)[0]
    return jsonify(movies)
    