from flask_cors import CORS
from flask_restful import Api
from flask import Blueprint, abort, jsonify
from version_1.resources.UserResource import UserResource
from version_1.resources.AccountResource import AccountResource
from version_1.resources.PayeeResource import PayeeResource
from version_1.resources.WalletResource import WalletResource
from util.Utils import *

# Declare the blueprint
v1 = Blueprint('v1', __name__)

# Set up cross-scripting allowed
#CORS(app, origins="http://127.0.0.1:8080", allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],supports_credentials=True)
#CORS(app, resources={r"/v1/*": {"origins": "http://127.0.0.1:8080","allow_headers":["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],"supports_credentials" : True}})
CORS(v1,resources={r"/*": {"origins": "*"}})

# Custom Api to render application error gracefully

class CustomApi(Api):

    def handle_error(self, e):
        code = getattr(e, 'code', 500)
        message = getattr(e, 'message', 'Internal Server Error')
        to_dict = getattr(e, 'to_dict', None)

        if code == 500:
            logger.exception(e)

        if to_dict:
            data = to_dict()
        else:
            data = {'code': code, 'message': message}

        return self.make_response(data, code)
    
        
# Set up the API and init the blueprint
api = CustomApi(default_mediatype='application/json')
api.init_app(v1)

# Set the default route
@v1.route('/')
def show():
    return 'Hello World'

#############################################
########## Resources to Add
#############################################


# Users
api.add_resource(UserResource, '/user','/user/<string:username>')

# Account
api.add_resource(AccountResource, '/account','/account/<string:username>')

# Payee
api.add_resource(PayeeResource, '/payee','/payee/<string:username>')

# Wallet
api.add_resource(WalletResource, '/wallet', '/wallet/<string:username>')
