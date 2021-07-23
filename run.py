from app import create_app, db
from app.blueprints.auth.models import User
from app.blueprints.ratings.models import Rating
import tmdbsimple
from app.wrappers import MovieRankings

app = create_app()

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Rating': Rating, 'tmdb': tmdbsimple, 'm': MovieRankings()}