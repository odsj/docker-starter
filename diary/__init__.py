import os
from flask import Flask
from diary.settings import ProdConfig
from diary.assets import assets
from flask import render_template
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user

def create_app(config_object=ProdConfig):
    diary_app = Flask(__name__.split('.')[0])
    diary_app.config.from_object(config_object)

    #diary.error_handler_spec[None][404] = not_found
    #diary.error_handler_spec[None][500] = server_error
    register_database(diary_app)
    register_blueprints(diary_app)
    register_extensions(diary_app)
    register_logger(diary_app)
    register_stormpath(diary_app)
    
    register_errorhandlers(diary_app)
    return diary_app

def register_database(diary):
    from diary.database import DBManager
    db_filepath = os.path.join(diary.root_path, 
                               diary.config['DB_FILE_PATH'])
    db_url = diary.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(diary.config['DB_LOG_FLAG']))    
    DBManager.init_db()
    

def register_extensions(diary):
    assets.init_app(diary)

def register_logger(diary):
    from diary.logger import Log
    log_filepath = os.path.join(diary.root_path,
                   diary.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)

def register_stormpath(diary_app):
    diary_app.config['DEBUG'] = True
    diary_app.config['SECRET_KEY'] = '3WotnDW3JOwjnkXWnmot/yX6dKgQSDHDWAEPHW5a5F8'
    diary_app.config['STORMPATH_API_KEY_FILE']='./diary/apiKey.properties'
    diary_app.config['STORMPATH_APPLICATION']='Diary'
    diary_app.config['STORMPATH_ENABLE_LOGIN'] = True
    diary_app.config['STORMPATH_ENABLE_USERNAME'] = True
    diary_app.config['STORMPATH_ENABLE_REGISTRATION'] = True
    diary_app.config['STORMPATH_ENABLE_LOGOUT'] = True
    stormpath_manager = StormpathManager(diary_app)

def register_errorhandlers(diary):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        diary.errorhandler(errcode)(render_error)


def register_blueprints(diary):
    from diary.controller import *

    """Register Flask blueprints."""
    diary.register_blueprint(journalRest.blueprint)
    diary.register_blueprint(journalWeb.blueprint)

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500
