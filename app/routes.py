from app import app
from flask import render_template, request
from app.forms import SearchMovieForm
import tmdbsimple as tmdb
import os

tmdb.API_KEY = os.environ.get('TMDB_API_KEY')

@app.route('/')
def index():
    form = SearchMovieForm()
    return render_template('index.html', form=form)

@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchMovieForm()
    search = tmdb.Search()
    results = None
    if request.method == 'POST' and form.validate():
        print("HERE")
        title = form.title.data
        response = search.movie(query=title)
        results = search.results
        
    return render_template('search.html', form=form, results=results)