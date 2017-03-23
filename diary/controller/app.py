# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from flask import flash, redirect, render_template, request, url_for
from diary.logger import Log

blueprint = Blueprint('public', __name__, static_folder='../static')

@blueprint.route('/', methods=['GET', 'POST'])
def home():
    Log.debug('Enter Home')
    return render_template('common/home.html')

@blueprint.route('/secret', methods=['GET'])
@login_required
def secret():
    return 'secret'
