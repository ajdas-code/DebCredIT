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
from BridgeObjects import *
from MongoDataStore import *



class UserResource (Resource):
    method_decorators = [validate_request]
    
    def __init__(self, **kwargs):
        #Resource constructor
        # use this for add_argument settings
        app.logger.debug("{} resource created..".format(__name__))


    
    
    @cross_origin()
    def get(self, id=None):

        if (id):
            # /user/id route
            result = User.getUserByUserName(un)
            if ( result == None):
                raise ResourceDoseNotExist("User does not exist")
            else:
                return  jsonify(json.loads(result.to_json()))
        else:
            # /user route
            #retrieve args - un and em from query string
            un = request.args.get('username',None)
            em = request.args.get('email',None)
        
            if ( (not un) and (not em)):
                #get all users. Really??
                #raise BadRequestError("Please provide either username or email id of the user")
                qSet = User.getUserByCriteria({})
                if ( qSet ):
                    return jsonify(queryset_to_dict(qSet))
                else:
                    raise ResourceDoseNotExist("No Users found")

            #get it from mongo
            if (un):
                result = User.getUserByUserName(un)
            else:
                result = User.getUserByEmail(em)
            if ( result == None):
                raise ResourceDoseNotExist("User does not exist")
            else:
                return  jsonify(json.loads(result.to_json()))

    @cross_origin()
    def post(self,id=None):

        # /user/id route
        if (id):
            username = id

        #/user route
        raw_dict = request.get_json(force=True)
        if (id):
            raw_dict.update({'username':username})
            
        #validate the dict data
        if (not DataModelValidator.check(BridgeObjects.UserSchema_,raw_dict)):
            raise BadRequestError("User model should contains - username, email, and roles")
        
        # Save the new user
        if (not User.createUser(raw_dict)):
            raise InternalError("Failed to save user")
        
        # data saved and return id
        result = User.getUserByUserName(raw_dict['username'])
        if ( result == None):
            raise ResourceDoseNotExist("User not saved, please try again")
        else:
            return  jsonify(json.loads(result.to_json()))


    @cross_origin()
    def patch(self, id= None):
        raw_dict = request.get_json(force=True)
        # /user route
        if (not id):
            id = raw_dict.get('username',None)
            if not id:
                raise BadRequestError("User update should contains - username, ")
        
        ret = User.updateUserByUserName(id,raw_dict)
        
        if (not ret):
            raise InternalError("Failed to Update user")
        else:
            return jsonify({"status": "success", "username":id})

    @cross_origin()
    def delete(self, id=None):
        # /user route
        if (not id):
            id = request.args.get('username',None)
            if (not id):
                raise BadRequestError("DELETE method i.e. delete user does not support /resource route")
            
        ret = User.deleteUserByUserName(id)
        if (not ret):
            raise InternalError("Failed to delete user")
        else:
            return jsonify({"status": "success", "username":id})


