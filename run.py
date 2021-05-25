from app import app, db
from app.models import User, Rating
import tmdbsimple
from app.wrappers import MovieRankings

if __name__ == "__main__":
    app.run(debug=True)

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Rating': Rating, 'tmdb': tmdbsimple, 'm': MovieRankings()}