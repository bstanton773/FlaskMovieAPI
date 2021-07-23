from . import bp as main
from flask import render_template, request
from app.blueprints.movies.forms import SearchMovieForm
from app.blueprints.movies.wrappers import MovieRankings


movie_rank = MovieRankings()

# MAIN

@main.route('/', methods=['GET', 'POST'])
def index():
    movies = movie_rank.search_all(q='')[0]
    form = SearchMovieForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        providers = '@'.join(form.providers.data)
        genres = '@'.join(form.genres.data)
        runtime = form.runtime.data
        ratingrange = f'{form.rating.data}@100'
        movies = movie_rank.search_all(q=title, providers=providers, genres=genres, runtime=runtime, ratingrange=ratingrange)[0]
    return render_template('index.html', form=form, movies=movies)