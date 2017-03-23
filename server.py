import os

from flask.helpers import get_debug_flag

from diary import create_app
from diary.settings import DevConfig, ProdConfig

#CONFIG = DevConfig if get_debug_flag() else ProdConfig
CONFIG = DevConfig
# app = create_app(CONFIG)
# app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))



import sys

from diary import create_app

reload(sys)
sys.setdefaultencoding('utf-8')

application = create_app(CONFIG)    

if __name__ == '__main__':
    print "starting test server..."
    application.run(host='0.0.0.0', port=8080, debug=True)