"""
 This file contains methods and classes to reduces boiler plate code
"""
import flask
from functools import wraps
from flask import jsonify, make_response, request
from flask_restful import abort
from flask import current_app as app

from mongoengine import *
from mongoengine.queryset import *

##################################################
# Auth Logging framework, custom made
# Todo: Flask framework
# TBD
##################################################

def validate_request(f):
  @wraps(f)
  def decorated_function(*args, **kws):
    # Do something with your request here
    data = request.cookies.get('sid-aqua',None)
    app.logger.debug("cookie data: {}  extracted..".format(data))
    
    if not data:
      flask.abort(404)
    return f(*args, **kws)
  return decorated_function
  
##################################################
# Cross scripting validation
#
##################################################
#Usage:
# @cross_origin() --> to allow all cross domain access
# @cross_origin(origin="192.168.1.100") --> allow only 192.168.1.100 access
def cross_origin(origin="*"):
    def cross_origin(func):
        @wraps(func)
        def _decoration(*args, **kwargs):
            ret = func(*args, **kwargs)
            _cross_origin_header = {"Access-Control-Allow-Origin": origin,
                                    "Access-Control-Allow-Headers":
                                        "Origin, X-Requested-With, Content-Type, Accept"}
            if isinstance(ret, tuple):
                if len(ret) == 2 and isinstance(ret[0], dict) and isinstance(ret[1], int):
                    # this is for handle response like: ```{'status': 1, "data":"ok"}, 200```
                    return ret[0], ret[1], _cross_origin_header
                elif isinstance(ret, basestring):
                    response = make_response(ret)
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return response
                elif isinstance(ret, Response):
                    ret.headers["Access-Control-Allow-Origin"] = origin
                    ret.headers["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
                    return ret
                else:
                    raise ValueError("Cannot handle cross origin, because the return value is not matched!")
            return ret

        return _decoration

    return cross_origin


#############################################################
# Custom : Data obj marshalling
# Note: Try to use marshmellow module here
# TBD
#############################################################
def mongo_to_dict(obj):
    return_data = []

    if isinstance(obj, Document):
        return_data.append(("id",str(obj.id)))

    for field_name in obj._fields:

        if field_name in ("id",):
            continue

        data = obj._data[field_name]

        if isinstance(obj._fields[field_name], DateTimeField):
            return_data.append((field_name, str(data.isoformat())))
        elif isinstance(obj._fields[field_name], StringField):
            return_data.append((field_name, str(data)))
        elif isinstance(obj._fields[field_name], FloatField):
            return_data.append((field_name, float(data)))
        elif isinstance(obj._fields[field_name], IntField):
            return_data.append((field_name, int(data)))
        elif isinstance(obj._fields[field_name], ListField):
            return_data.append((field_name, data))
        elif isinstance(obj._fields[field_name], EmbeddedDocumentField):
            return_data.append((field_name, mongo_to_dict(data)))

    return dict(return_data)

def queryset_to_dict (qSet):
    if not qSet:
        return None
    adict = {'data':[json.loads(ob.to_json()) for ob in qset]}
    return adict
    
###########################################################
# Error Handler
# Custom application exceptions
#
##########################################################

class APIException(Exception):
    
    def __init__(self, message=None, payload=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        else:
            self.message = self.default_message

        self.payload = payload

    def to_dict(self):
        """
        Call this in the the error handler to serialize the
        error for the json-encoded http response body.
        """
        payload = dict(self.payload or ())
        payload['message'] = self.message
        payload['code'] = self.code
        return payload

class ResourceDoseNotExist(APIException):
    """Custom exception when resource is not found."""
    code = 404
    default_message = 'Resource not found'


class InternalError (APIException):
    """Custom exception when internal error occurs."""
    code = 500
    default_message = 'Internal Server Error'

class BadRequestError(APIException):
    """Custom exception when internal error occurs."""
    code = 400
    default_message = 'Bad Request'
