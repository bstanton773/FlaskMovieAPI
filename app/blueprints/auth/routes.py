from flask import request, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from . import bp as auth
from .forms import UserInfoForm, LoginForm, SearchUserForm
from .models import User
from werkzeug.security import check_password_hash

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # print(username, email, password)
        check_user = User.query.filter((User.username==username)|(User.email==email)).first()
        if check_user:
            flash("That username or email is already in use", 'warning')
            return redirect('signup')
        # create a new instance of User
        new_user = User(username, email, password)
        # add new instance to our database
        db.session.add(new_user)
        # commit database
        db.session.commit()

        # Send email to new user

        flash("You have succesfully signed up!", "success")
        return redirect(url_for('main.index'))
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Email/Password. Please try again", 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        # next_page = request.args.get('next')
        # if next_page:
        #     return redirect(url_for(next_page.lstrip('/')))
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have succesfully logged out", 'primary')
    return redirect(url_for('main.index'))


@auth.route('/search-users', methods=['GET','POST'])
@login_required
def search_users():
    form = SearchUserForm()
    users = current_user.followed.all()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        search = f"%{username}%"
        users = User.query.filter(User.username.ilike(search)).all()
        
    return render_template('search_users.html', form=form, users=users)


@auth.route('/follow')
@login_required
def follow():
    user_id = request.args.get('user_id')
    u = User.query.get(user_id)

    current_user.follow(u)
    flash(f'You have followed {u.username}', 'success')
    return redirect(url_for('auth.search_users'))


@auth.route('/unfollow')
@login_required
def unfollow():
    user_id = request.args.get('user_id')
    u = User.query.get(user_id)

    current_user.unfollow(u)
    flash(f'You have unfollowed {u.username}', 'info')
    return redirect(url_for('auth.search_users'))