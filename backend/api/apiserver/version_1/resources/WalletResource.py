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
from FinancialInstrument import *

from BridgeObjects import *
from MongoDataStore import *




class WalletResource (Resource):
    method_decorators = [validate_request]

    
    def __init__(self, **kwargs):
        #Resource constructor
        # use this for add_argument settings
        app.logger.debug("{} resource created..".format(__name__))


    @cross_origin()
    def get(self, id=None):
        id = id
        if (not id):
            # /account route
            #retrieve args - un and em from query string
            id = request.args.get('username')
            if ( (not id)):
                raise BadRequestError("Please provide either username to access the Payee list")

        #get it from mongo
        #Get user
        usr = User.getUserByUserName(id)
        if ( usr != None):
            result = Wallet.getWalletByUser(usr)
            primaryFIDict = Wallet.getPrimaryFIFromWallet(usr)
            otherFIDict = Wallet.getOtherFIsFromWallet(usr)
            if ( result == None):
                raise ResourceDoseNotExist("Wallet for the username {} does not exist",format(iid))
            else:
                result_dict = json.loads(result.to_json())
                if primaryFIDict:
                    result_dict.updte({"primary_fi": primaryFIDict})
                if otherFIDict:
                    result_dict.updte({"other_fis": otherFIDict})
                return  jsonify(result_dict)
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(iid))

    


    @cross_origin()
    def post(self,id=None):

        raw_dict = request.get_json(force=True)
        #blocking /wallet route
        if (not id):
            id = raw_dict.get('username',None)
            if not id:
                raise BadRequestError("Please provide either username to access the payee")
            else:
                del raw_dict['username']
        #Get user
        usr = User.getUserByUserName(id)
        
        if ( usr != None):

            if (not Wallet.createWallet(usr)):
                raise InternalError("Failed to create Wallet")
        
            # data saved and return id
            result = Wallet.getWalletByUser(usr)
            if ( result == None):
                raise ResourceDoseNotExist("Wallet not found, please try again")
            else:
                return  jsonify(json.loads(result.to_json()))
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))



    @cross_origin()
    def patch(self, id= None):
        
        raw_dict = request.get_json(force=True)
        #blocking /Wallet route
        if (not id):
            id = raw_dict.get('username',None)
            if (not id):
                raise BadRequestError("PUT method i.e. create Wallet does not support /resource route")
        #/wallet/id route

        #Get user
        usr = User.getUserByUserName(id)
        
        if ( usr != None):
            
            # getting payee based on attribute provided
            
            #profile
            fiUserProfile_dict = raw_dict.get('profile',None)
            # fi Type
            fiType_dict = raw_dict.get('type',None)
            # instrument details
            instrument_dict = raw_dict.get('instrument',None)
            
            if ( (not fiUserProfile_dict) or (not fiType_dict) or (not instrument_dict ) or
                (not isinstance(fiUserProfile_dict,dict)) or (not isinstance(fiUserProfile_dict,dict)) or (not isinstance(fiUserProfile_dict,dict)) ):
                raise BadRequestError("Missing input")

                
            result = Wallet.addPrimaryFIOnWallet(usr,fiUserProfile_dict,fiType_dict, instrument_dict)
            if not result :
                    raise ResourceDoseNotExist("Error in FI to wallet")
            else:
                    return  jsonify({"status": "success", "username":id})

        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))


    @cross_origin()
    def delete(self, id=None):

        # /payee route
        if (not id):
            id = request.args.get('username',None)
            if (not id):
                raise BadRequestError("DELETE method i.e. delete FI from Waller needs username")

        usr = User.getUserByUserName(id)
        
        if ( usr != None):
            result = Wallet.deletePrimaryFIOnWallet(usr)
            if not result :
                raise InternalError("Failed to delete FI from User {}".format(id))
            else:
                return jsonify({"status": "success", "username":id})
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))
