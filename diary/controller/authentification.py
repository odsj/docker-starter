# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from flask import flash, redirect, render_template, request, url_for
from diary.logger import Log

blueprint = Blueprint('authenitification', __name__, static_folder='../static')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
 
    if request.method == 'POST':
        print("POST")
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
                         )
            login_user(_user, remember=True)
            flash('You were logged in.')
 
            return redirect(url_for('public.home'))
        except StormpathError as err:
            error = err.message
            print(error)
 
    return render_template('common/login.html', error=error)
