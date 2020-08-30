#!/usr/bin/env python3
############################################################################################
# Main Processing of App
#
# This file is the meat of the API. The app is initialized, DB is accessed, and config files
# are loaded up. Note that it is in this file that user-defined config files are chosen,
# if they exist.
############################################################################################
import getpass
import pprint
from flask import Flask
from version_1 import v1
from flask_cors import CORS
from flask_mongoengine import MongoEngine


app = Flask(__name__)


#############################################
########## App Configuration
#############################################
app.config.from_object('config.base_settings')

# User Overrides
SETTINGS_BY_USERNAME = {
  'AjiteshDas' : 'devel_user',
}

# Import the file if username matches
custom_settings_file = None
custom_settings_file = SETTINGS_BY_USERNAME.get(getpass.getuser().lower())

if custom_settings_file is not None:
    app.config.from_object('config.{}'.format(custom_settings_file))

pprint.pprint("============================")
pprint.pprint("Final Loaded configuration:")
pprint.pprint(app.config)
pprint.pprint("============================")


############################################
### Flask routes
###########################################
@app.route('/')
def index():
    return "<H1> Greetings </H1>"
@app.route('/hello')
def hello_world():
   return "hello world"
#############################################
########## Blueprints
#############################################
app.register_blueprint(v1, url_prefix='/api/v1')


#############################################
########## Database
#############################################
db = MongoEngine()
db.init_app(app)




def start_ngrok():
    from pyngrok import ngrok

    url = ngrok.connect(5000)
    print(' * Tunnel URL:', url)


#############################################
########## Run
#############################################
if __name__ == '__main__':
    
    if app.config['ENABLE_NGROK_TUNNEL']:
        start_ngrok()
    app.run(host     = app.config['HOST'],
            debug    = app.config['DEBUG'],
            threaded = True,
            port     = app.config['PORT']
    )
