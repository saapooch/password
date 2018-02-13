# project/server/main/views.py

import os
from flask import render_template, Blueprint, request, flash, redirect, url_for, current_app
from app.server.user.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from app.server import db, models, bcrypt
import flask_whooshalchemy

basedir = os.path.abspath(os.path.dirname(__file__))
user_blueprint = Blueprint('user', __name__,)

@user_blueprint.route("/", methods=['GET', 'POST'])
def main():
    return render_template('user/main.html')

@user_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        try:
            user = db.session.query(models.User).filter_by(username=form.username.data).first()
        except:
            user = None
        if user and bcrypt.check_password_hash(
                user.password, request.form['password']):
            login_user(user)
            flash('You are logged in. Welcome!', 'success')
            return redirect(url_for('account.main', user=user))
        else:
            flash('Invalid email and/or password.', 'danger')
            return render_template('user/login.html', form=form)
    return render_template('user/login.html', form = form)

@user_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = models.User(
            username = form.username.data,
            email=form.email.data,
            password=form.password.data,
            admin= False
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('You are logged in. Welcome to SafeNet!', 'success')
        return redirect(url_for('account.main', user=user))

    return render_template('user/register.html', form = form)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out. Bye!', 'success')
    return redirect(url_for('user.main'))
