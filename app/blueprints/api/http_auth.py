from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.blueprints.auth.models import User
from datetime import datetime

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return {
            'status': 'error',
            'message': 'Incorrect Username or Password'
        }, status    

@token_auth.verify_token
def verify(token):
    user = User.query.filter_by(token=token).first()
    if user and user.token_expiration > datetime.utcnow():
        return user