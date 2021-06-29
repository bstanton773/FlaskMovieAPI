from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, SelectMultipleField
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
    runtime = IntegerField('Runtime', default='242')
    submit = SubmitField()


class SearchUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField()


class UserInfoForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField()


class RatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('Rate')
