############################################################################################
# Global Configurations - Base
#
# This file holds base global configurations for the API. In order to accomodate for
# multiple developers working on this project, this base config file is set up in order to
# have certain settings (production settings) be default. After those default settings are
# put into place, a check is made on the name of the user running the code, in the main.py
# file, and if it matches explicitly-declared users, the settings can be overridden by user-
# defined files that are housed in this same directory.
############################################################################################

from datetime import timedelta

#############################################
########## Base (Production) Settings
#############################################

# Flask Core Settings
APP_NAME   = "DebCredIT_Api_Server"
ENV        = 'production'
DEBUG      = False
HOST       = '127.0.0.1'
PORT       = 5000
SECRET_KEY = "b\'_5#y2L\"F4Q8z\n\xec]/'"
#TESTING    = False
#PROPAGATE_EXCEPTIONS = True
#PRESERVE_CONTEXT_ON_EXCEPTION = True
#TRAP_HTTP_EXCEPTIONS = False
SESSION_COOKIE_NAME = 'debcredit_session'
#SESSION_COOKIE_DOMAIN = None
#SESSION_COOKIE_PATH = None
SESSION_COOKIE_HTTPONLY = True

# Application Setting
# NGROK
ENABLE_NGROK_TUNNEL = True

# Database Settings

MONGODB_SETTINGS = {
    'db': 'DebCredIt',
    'username':'dajitesh',
    'password':'suku555',
    'host': 'mongodb://dajitesh:suku555@debcredit-shard-00-00-jdcns.mongodb.net:27017,debcredit-shard-00-01-jdcns.mongodb.net:27017,debcredit-shard-00-02-jdcns.mongodb.net:27017/test?ssl=true&replicaSet=DebCredIt-shard-0&authSource=admin&retryWrites=true&w=majority',
    'port': 27017,
    'connect': True,
}



# Mail Settings
MAIL_SERVER   = 'smtp.example.com'
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'


# Security Settings
# https://pythonhosted.org/Flask-Security/configuration.html
# https://pythonhosted.org/Flask-JWT/
JWT_EXPIRATION_DELTA           = timedelta(days=30)
JWT_AUTH_URL_RULE              = '/api/v1/auth'
JWT_AUTH_USERNAME_KEY          = 'ownername'
JWT_AUTH_PASSWORD_KEY          = 'ownerpassword'
SECURITY_CONFIRMABLE           = True
SECURITY_TRACKABLE             = True
SECURITY_REGISTERABLE          = True
SECURITY_RECOVERABLE           = True
SECURITY_PASSWORD_HASH         = 'sha512_crypt'
SECURITY_PASSWORD_SALT         = 'add_salt'
