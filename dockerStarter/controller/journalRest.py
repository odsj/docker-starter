# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import flash, redirect, render_template, request, url_for
from flask import jsonify

from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user

from dockerStarter.database import dao
from dockerStarter.logger import Log
from dockerStarter.model.journal import Journal

from datetime import datetime
import json

blueprint = Blueprint('journalRest', __name__, static_folder='../static')


'''
Rest CRUD 
'''
@blueprint.route('/rest/journal', methods=['POST'])
def createJournal():
    createRequestContext = request.data
    
    # Get Create Journal Parameter
    try:
        requestParsedData = json.loads(createRequestContext)
        title   = requestParsedData['diaryTitle']
        context = requestParsedData['diaryContext']
        tags    = requestParsedData['diaryTags']
    except KeyError:
        return jsonify(results={'message':'Key is not vaild'})
        
    writer = user.username
    date   = datetime.now()
        
    writeToDb(writer, title, context, tags, date)
        
    return jsonify(results=createRequestContext)
    
@blueprint.route('/rest/journals', methods=['GET'])
def getAllJournal():
    resultList = dao.query(Journal).all()
    return jsonify( results = [result.serialize() for result in resultList])

@blueprint.route('/rest/journals', methods=['PUT'])
def updateJournal():
    return None
    
@blueprint.route('/rest/journals', methods=['DELETE'])
def deleteJournal():
    return None

'''
Internal Logic Part
'''
def writeToDb(writer, title, context, tags, date):
    validationDiaryRequest(writer, title, context, tags, date)
    saveResult = saveToDb(writer, title, context, tags, date);
    return saveResult
    
def validationDiaryRequest(writer, title, context, tags, date):
    if ( writer == None or title == None or context == None or date == None):
        raise TypeError("Request Data is not vaild")
    #if date <= "1970-01-01":
    #    raise ValueError("Date is not Vaild")

def saveToDb(writer, title, context, tags, date):
    from diary.database import dao
    journal = Journal(writer, title, context, tags, date, True)
    dao.add(journal)
    dao.commit()
        
    Log.debug(journal) 
    return journal
