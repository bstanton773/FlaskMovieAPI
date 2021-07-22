from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

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


class SearchUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField()


# class UserInfoForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField()


# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField()


class RatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Rate')
