import os
from flask import Flask
from dockerStarter.settings import ProdConfig
from dockerStarter.assets import assets
from flask import render_template
from flask_stormpath import StormpathError, StormpathManager, User, login_required, login_user, logout_user, user

def create_app(config_object=ProdConfig):
    dockerStarter = Flask(__name__.split('.')[0])
    dockerStarter.config.from_object(config_object)

    #dockerStarter.error_handler_spec[None][404] = not_found
    #dockerStarter.error_handler_spec[None][500] = server_error
    register_database(dockerStarter)
    register_blueprints(dockerStarter)
    register_extensions(dockerStarter)
    register_logger(dockerStarter)
    register_stormpath(dockerStarter)
    
    register_errorhandlers(dockerStarter)
    return dockerStarter

def register_database(dockerStarter):
    from dockerStarter.database import DBManager
    db_filepath = os.path.join(dockerStarter.root_path, 
                               dockerStarter.config['DB_FILE_PATH'])
    db_url = dockerStarter.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(dockerStarter.config['DB_LOG_FLAG']))    
    DBManager.init_db()
    

def register_extensions(dockerStarter):
    assets.init_app(dockerStarter)

def register_logger(dockerStarter):
    from dockerStarter.logger import Log
    log_filepath = os.path.join(dockerStarter.root_path,
                   dockerStarter.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)

def register_stormpath(dockerStarter):
    dockerStarter.config['DEBUG'] = True
    dockerStarter.config['SECRET_KEY'] = '3WotnDW3JOwjnkXWnmot/yX6dKgQSDHDWAEPHW5a5F8'
    dockerStarter.config['STORMPATH_API_KEY_FILE']='./dockerStarter.apiKey.properties'
    dockerStarter.config['STORMPATH_APPLICATION']='Diary'
    dockerStarter.config['STORMPATH_ENABLE_LOGIN'] = True
    dockerStarter.config['STORMPATH_ENABLE_USERNAME'] = True
    dockerStarter.config['STORMPATH_ENABLE_REGISTRATION'] = True
    dockerStarter.config['STORMPATH_ENABLE_LOGOUT'] = True
    stormpath_manager = StormpathManager(dockerStarter)

def register_errorhandlers(dockerStarter):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        dockerStarter.errorhandler(errcode)(render_error)


def register_blueprints(dockerStarter):
    from dockerStarter.controller import *

    """Register Flask blueprints."""
    dockerStarter.register_blueprint(journalRest.blueprint)
    dockerStarter.register_blueprint(journalWeb.blueprint)

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500
