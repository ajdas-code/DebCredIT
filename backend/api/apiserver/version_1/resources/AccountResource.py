import json
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import jsonify, make_response, request
from flask_restful import abort
from werkzeug.datastructures import MultiDict
from flask import current_app as app


#### api module######
from Utils import *

####Application Import######
from User import *
from Account import *

from BridgeObjects import *
from MongoDataStore import *




class AccountResource (Resource):
    method_decorators = [validate_request]

    @staticmethod
    def _switcherAccountOperation (opcode):
        def defaultMethod (usr, amnt):
            raise BadRequestError("Unknow opcode {}. Please use add,spend,update or cashback".format(opcode))
        
        switcher={
                'add':Account.addFundToAccount,
                'spend':Account.spendFundFromAccount,
                'update':Account.updateMaxPay,
                'cashback':Account.updateCashBack,
                }
        
        func=switcher.get(i,dafaultMethod)
        return func()
    
    def __init__(self, **kwargs):
        #Resource constructor
        # use this for add_argument settings
        app.logger.debug("{} resource created..".format(__name__))


    @cross_origin()
    def get(self, id=None):
        iid = id
        if (not iid):
            # /account route
            #retrieve args - un and em from query string
            iid = request.args.get('username',None)
            if not iid:
                raise BadRequestError("Please provide either username to access the account")

        #get it from mongo
        #Get user
        usr = User.getUserByUserName(iid)
        if ( usr != None):
            result = Account.getAccountByUser(iid)
            if ( result == None):
                raise ResourceDoseNotExist("Account for the username {} does not exist",format(iid))
            else:
                return  jsonify(json.loads(result.to_json()))
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(iid))



    @cross_origin()
    def post(self,id=None):
        raw_dict = request.get_json(force=True)
        #blocking /account route
        if (not id):
            id = raw_dict.get('username',None)
            if not id:
                raise BadRequestError("Please provide either username to access the account")
            else:
                del raw_dict['username']
        #/account/id route
        #Get user
        usr = User.getUserByUserName(id)
        if ( usr != None):
            #validate the dict data
            if (not DataModelValidator.check(BridgeObjects.AccountSchema_,raw_dict)):
                raise BadRequestError("Account model should contains - amount currency")
        
            # Save the new account
            if (not Account.createAccount(usr, raw_dict)):
                raise InternalError("Failed to create Account")
        
            # data saved and return id
            result = Account.getAccountByUser(usr)
            if ( result == None):
                raise ResourceDoseNotExist("Account not found, please try again")
            else:
                return  jsonify(json.loads(result.to_json()))
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))
            


    @cross_origin()
    def patch(self, id= None):
        raw_dict = request.get_json(force=True)
        #blocking /account route
        if (not id):
            id = raw_dict.get('username',None)
            if (not id):
                raise BadRequestError("PUT method i.e. create account does not support /resource route")
        #/account/id route

        #Get user
        usr = User.getUserByUserName(id)
        if ( usr != None):
            #amount
            amount = float(raw_dict.get('amount','0'))
            # opcode
            func = AccountResource._switcherAccountOperation(raw_dict['opcode'])
            if (func(usr,amount)):
                result = Account.getAccountByUser(usr)
                if ( result == None):
                    raise ResourceDoseNotExist("Error in reading account, please try to reread again again")
                else:
                    return  jsonify(json.loads(result.to_json()))
            else:
                raise BadRequestError("Failed to transact on the account")
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))


    @cross_origin()
    def delete(self, id=None):

        raise BadRequestError("if user is deleted, the account will be deleted as well")
            
