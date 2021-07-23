from flask import Blueprint

bp = Blueprint('watchlist', __name__, url_prefix='/watchlist')

from . import routes