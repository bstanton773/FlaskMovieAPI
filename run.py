from app import create_app, db
from app.blueprints.auth.models import User
from app.blueprints.movies.wrappers import MovieRankings
from app.blueprints.ratings.models import Rating
import tmdbsimple

app = create_app()

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Rating': Rating, 'tmdb': tmdbsimple, 'm': MovieRankings()}