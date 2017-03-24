# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user
from flask import flash, redirect, render_template, request, url_for
from flask import jsonify
from dockerStarter.logger import Log

from dockerStarter.service.amandaBackup import showBackupResult

import commands
import requests
import json

from dockerStarter.database import dao
from dockerStarter.model.journal import Journal

blueprint = Blueprint('journalWeb', __name__, static_folder='../static')

@blueprint.route('/')
@blueprint.route('/index')
def indexPage():
    Log.info("enter index page")
    resultList = dao.query(Journal).filter(Journal.is_public == True)
    Log.debug(resultList)

    dockerInfos = getDockerImages()

    return render_template('dockerStarter/index.html',
                           user = user,
                           journals = resultList,
                           images = dockerInfos)

@blueprint.route('/dockerImages')
def showDockerImages():
    Log.info("enter dockerImages page")

    dockerInfos = getDockerImages()

    return render_template('dockerStarter/images.html',
                           user = user,
                           images = dockerInfos)

@blueprint.route('/dockerContainers')
def showDockerContainers():
    Log.info("enter dockerContainers page")

    dockerInfos = getDockerContainers()

    return render_template('dockerStarter/containers.html',
                           user = user,
                           images = dockerInfos)

@blueprint.route('/backupResult')
def showBackupResults():
    Log.info("enter backupResult page")

    backupInfos = showBackupResult()

    return render_template('dockerStarter/backups.html',
                           user = user,
                           backupInfos = backupInfos)

def getDockerImages():
    """
    REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
    rastasheep/ubuntu-sshd   latest              07e63bce704c        2 weeks ago         252 MB

    """
    status, dockerImages = commands.getstatusoutput('sudo docker images')
    dockerImagesSplitRows = dockerImages.split('\n')[1:]
    dockerInfos = []

    for line in dockerImagesSplitRows:
        dockerImagesSplitSpace = line.split()

        dockerInfo = {}

        try:
            dockerInfo['dockerRepository'] = dockerImagesSplitSpace[0]
            dockerInfo['dockerTag'] = dockerImagesSplitSpace[1]
            dockerInfo['dockerImageId'] = dockerImagesSplitSpace[2]
            dockerInfo['dockerCreated'] = " ".join(dockerImagesSplitSpace[-5:-2])
            dockerInfo['dockerSize'] = " ".join(dockerImagesSplitSpace[-2:])

            dockerInfos.append(dockerInfo)
        except IndexError, e:
            print e.message

    return dockerInfos

def getDockerContainers():
    """
    CONTAINER ID        IMAGE                    COMMAND               CREATED             STATUS              PORTS                   NAMES
    05638d664383        rastasheep/ubuntu-sshd   "/usr/sbin/sshd -D"   6 seconds ago       Up 5 seconds        0.0.0.0:32769->22/tcp   ubuntu2
    dda453e95a96        rastasheep/ubuntu-sshd   "/usr/sbin/sshd -D"   10 seconds ago      Up 9 seconds        0.0.0.0:32768->22/tcp   ubuntu1
    """
    status, dockerContainers = commands.getstatusoutput('sudo docker ps -a')
    dockerContainersSplitRows = dockerContainers.split('\n')[1:]
    dockerInfos = []

    for line in dockerContainersSplitRows:
        dockerContainersSplitSpace = line.split()

        dockerInfo = {}

        try:
            dockerInfo['containerId'] = dockerContainersSplitSpace[0]
            dockerInfo['image'] = dockerContainersSplitSpace[1]
            dockerInfo['command'] = dockerContainersSplitSpace[2]
            dockerInfo['created'] = " ".join(dockerContainersSplitSpace[2:-8])
            dockerInfo['status'] = " ".join(dockerContainersSplitSpace[-5:-2])
            dockerInfo['ports'] = dockerContainersSplitSpace[-2]
            dockerInfo['names'] = dockerContainersSplitSpace[-1]

            dockerInfos.append(dockerInfo)
        except IndexError, e:
            print e.message

    return dockerInfos


@blueprint.route('/home')
@login_required
def homePage():
    Log.info("enter home page")
    resultList = dao.query(Journal).all()
    journals = jsonify( results = [result.serialize() for result in resultList])
    Log.debug(journals)
    return render_template('dockerStarter/home.html', user = user, journals = resultList)
    
@blueprint.route("/timeline")
def timelinePage():
    return render_template('dockerStarter/timeline.html')
