from flask import Blueprint

bp = Blueprint('ratings', __name__, url_prefix='/ratings')

from . import routes, models