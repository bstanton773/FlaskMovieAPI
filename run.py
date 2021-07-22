from app import create_app, db
from app.models import User, Rating
import tmdbsimple
from app.wrappers import MovieRankings

app = create_app()

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Rating': Rating, 'tmdb': tmdbsimple, 'm': MovieRankings()}