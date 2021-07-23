from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired

class SearchMovieForm(FlaskForm):
    title = StringField('Movie Title')
    providers = SelectMultipleField('Streaming Providers', choices=[
        ('9', 'Amazon Prime'), 
        ('337', 'Disney +'), 
        ('384', 'HBO Max'), 
        ('15', 'Hulu'), 
        ('8', 'Netflix'), 
        ('531', 'Paramount +'), 
        ('386', 'Peacock'),
        ('387', 'Peacock Premium'),
        ('37', 'Showtime'), 
        ('43', 'Starz')
    ])
    genres = SelectMultipleField('Genres', choices=[
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Animation', 'Animation'),
        ('Anime', 'Anime'),
        ('Comedy', 'Comedy'),
        ('Comic', 'Comic'),
        ('Crime', 'Crime'),
        ('Disaster', 'Disaster'),
        ('Drama', 'Drama'),
        ('Dramedy', 'Dramedy'),
        ('Fantasy', 'Fantasy'),
        ('Horror', 'Horror'),
        ('Musical', 'Musical'),
        ('Mystery', 'Mystery'),
        ('RomCom', 'RomCom'),
        ('Romance', 'Romance'),
        ('Sci-Fi', 'Sci-Fi'),
        ('Sports', 'Sports'),
        ('Thriller', 'Thriller'),
        ('Western', 'Western')
    ])
    runtime = SelectField('Runtime <', choices=[(i, i) for i in range(242,0,-1)])
    rating = SelectField('Rating >', choices=[(i,i) for i in range(100)])
    submit = SubmitField()