# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from flask import flash, redirect, render_template, request, url_for
from flask import jsonify
from diary.logger import Log
import requests
import json

from diary.database import dao
from diary.model.journal import Journal

blueprint = Blueprint('journalWeb', __name__, static_folder='../static')

@blueprint.route('/')
@blueprint.route('/index')
def indexPage():
    Log.info("enter index page")
    resultList = dao.query(Journal).filter(Journal.is_public == True)
    Log.debug(resultList)
    return render_template('diary/index.html',user = user, journals = resultList)

@blueprint.route('/home')
@login_required
def homePage():
    Log.info("enter home page")
    resultList = dao.query(Journal).all()
    journals = jsonify( results = [result.serialize() for result in resultList])
    Log.debug(journals)
    return render_template('diary/home.html', user = user, journals = resultList)
    
@blueprint.route("/timeline")
def timelinePage():
    return render_template('diary/timeline.html')