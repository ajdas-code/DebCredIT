############################################################################################
# Template for User-Specific Configuration
#
# Here a developer can specify machine-specific settings to override the base settings
# found in the base_settings.py file of the config directory.
#
# NOTE: If someone is going to declare specific settings here, he/she will need to make sure
# to add the corresponding unix username (or change how settings are imported) to the
# main.py file in order to make sure that the settings are overriden.
############################################################################################

from datetime import timedelta

#############################################
########## User-Level Settings
#############################################

# Flask Core Settings
ENV        = 'development'
DEBUG      = True


# Application Setting
# NGROK
ENABLE_NGROK_TUNNEL = False

# Database Settings

MONGODB_SETTINGS = {
    'db': 'kitchensink',
    'username':'testuser',
    'password':'testuser',
    'host': 'mongodb+srv://testuser:testuser@kitchensink-lzcqm.mongodb.net/test?retryWrites=true&w=majority',
    'port': 27017,
    'connect': True,
}



# Mail Settings
MAIL_SERVER   = 'smtp.zohomail.com'
MAIL_PORT     = 465
MAIL_USE_SSL  = True
MAIL_USERNAME = 'dajitesh'
MAIL_PASSWORD = 'password'


# Security Settings
# # https://pythonhosted.org/Flask-Security/configuration.html
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
