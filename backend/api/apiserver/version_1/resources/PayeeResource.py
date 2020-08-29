import json
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask import jsonify, make_response, request
from flask.ext.restful import abort
from werkzeug.datastructures import MultiDict
from flask import current_app as app


#### api module######
from .util.Utils import *

####Application Import######
from common.models.User import *
from common.models.Payee import *

from BridgeObjects import *
from MongoDataStore import *

class Switcher(object):
    @staticmethod
    def invalidMethod(usr,val):
        raise BadRequestError("Invalid payee search operation, please provide payee name, email or phone")
        
    def indirect(self,i):
        method_name='getPayeeBy'+str(i).lower()
        method=getattr(self,method_name, Switcher.invalidMethod)
        return method()
        
    def getPayeeByusername(self):
        return Payee.getPayeeByUserAndPayeeName
        
    def getPayeeByphone(self):
        return Payee.getPayeeByUserAndPayeePhone
        
    def getPayeeByemail(self):
        return Payee.getPayeeByUserAndPayeeEmail


class PayeeResource (Resource):
    method_decorators = [validate_request]

    
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
            iid = request.args.get('username')
            if ( (not iid)):
                raise BadRequestError("Please provide either username to access the Payee list")

        #get it from mongo
        #Get user
        usr = User.getUserByUserName(iid)
        if ( usr != None):
            raw_dict = request.get_json(force=True)
            #attbr
            attbr = raw_dict.get('attribute',None)
            # value
            value = raw_dict.get('value',None)
            if ( attbr and value):
                switch = Switcher()
                func = switch.indirect(attbr)
                result = func(usr,value)
                result_dict = json.loads(result.to_json())
            else
                result = Payee.getAllPayeeByUser(usr)
                result_dict = queryset_to_dict(result)
                
            if ( result == None):
                raise ResourceDoseNotExist("Account for the username {} does not exist",format(iid))
            else:
                return  jsonify(result_dict)
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(iid))

    


    @cross_origin()
    def post(self,id=None):

        raw_dict = request.get_json(force=True)
        #blocking /payee route
        if (not id):
            id = raw_dict.get('username',None)
            if not id:
                raise BadRequestError("Please provide either username to access the payee")
            else:
                del raw_dict['username']
        #/payee/id route
        #Get user
        usr = User.getUserByUserName(id)
        
        if ( usr != None):
            #validate the dict data
            if (not DataModelValidator.check(BridgeObjects.PayeeSchema_,raw_dict)):
                raise BadRequestError("Account model should contains -mandatory payee details")
        
            # Save the new account
            if (not Payee.createPayee(usr, raw_dict)):
                raise InternalError("Failed to create Payee")
        
            # data saved and return id
            result = Payee.getPayeeByUserAndPayeeName(usr,raw_dict['name'])
            if ( result == None):
                raise ResourceDoseNotExist("Payee not found, please try again")
            else:
                return  jsonify(json.loads(result.to_json()))
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))



    @cross_origin()
    def patch(self, id= None):
        
        raw_dict = request.get_json(force=True)
        #blocking /Payee route
        if (not id):
            id = raw_dict.get('username',None)
            if (not id):
                raise BadRequestError("PUT method i.e. create Payee does not support /resource route")
        #/account/id route

        #Get user
        usr = User.getUserByUserName(id)
        
        if ( usr != None):
            
            # getting payee based on attribute provided
            
            #attbr
            attbr = raw_dict.get('attribute',None)
            # value
            value = raw_dict.get('value',None)
            payee = None
            if ( attbr and value):
                switch = Switcher()
                func = switch.indirect(attbr)
                payee = func(usr,value)
            else
                raise BadRequestError("Need to provide attr and value to identify correct payee for user")
                
            result = Payee.addTargetFIOnPayee(usr,raw_dict, {attbr:value})
            if not result :
                    raise ResourceDoseNotExist("Error in reading account, please try to reread again again")
            #get the results
            payee = func(usr,value)
            
            if (not payee):

                raise ResourceDoseNotExist("Error in reading payee details, please try to reread again again")
            else:
                    return  jsonify(json.loads(payee.to_json()))

        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))


    @cross_origin()
    def delete(self, id=None):

        # /payee route
        if (not id):
            id = request.args.get('username',None)
            if (not id):
                raise BadRequestError("DELETE method i.e. delete payee needs username")

        usr = User.getUserByUserName(id)
        
        if ( usr != None):
            
            # getting payee based on attribute provided
            
            #attbr
            attbr = raw_dict.get('attribute',None)
            # value
            value = raw_dict.get('value',None)
            payee = None
            if ( attbr and value):
                result = Payee.deletePayee(usr,{attbr:value})
                if not result :
                    raise InternalError("Failed to delete user")
                else:
                    return jsonify({"status": "success", "username":id})
            else
                raise BadRequestError("Need to provide attr and value to identify correct payee for user")
        else:
            raise ResourceDoesNotExist("User of username {} does not exist".format(id))
