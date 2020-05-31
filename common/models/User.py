import datetime
import pytz
import json
import sys, traceback

from mongoengine import *
from BridgeObjects import *
from ConfigConstants import *

class User (DynamicDocument):
    
    #user name e.g dajitesh
    username = StringField(max_length=30, required=True,unique=True)
    #active account - to stop abuse - default:True
    isactive = BooleanField(default=True)
    #email - dajitesh@gmail.com
    email = EmailField(required=True,unique=True)
    #roles - user or admin
    roles = StringField(max_length=10,required=True,choices=ConfigConstants.ROLE )
    # time created : Time the document 1st saved
    timecreated = DateTimeField()
    # time created : Time the document 1st saved
    timeupdated = DateTimeField()
    
    #active account - to stop abuse - default:True
    isKYCdone = BooleanField(default=True)

    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'user', 'index': ['username','email']}


    #----------------------------------------
    # Internal method
    #---------------------------------------
    @staticmethod
    def internalupdateuser (user, udict):
        if (udict and isinstance(udict, dict)):
            if (user):
                for key in udict.keys():
                    if key not in [k for k,v in user._fields.items()]:
                        del udict[key]
                for key in udict.keys():
                    setattr(user, key, udict[key])
                user.timeupdated = datetime.datetime.now()
                try:
                    user.save()
                    return True
                except:
                    traceback.print_exc()
                    return False
            else:
                return False
        else:
            return False

    #----------------------------------------
    # Internal method
    #---------------------------------------
    @staticmethod
    def _internaldeleteuser (user):
        
        try:
            if (user):
                user.delete()
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False



    #Static methods
    #C R U D Operations
    
    #Read
    
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    #query by criteria ==>> Returns User Document QuerySet to 'iter' over
    # using non unique criteria --> [isactive,roles,and isKYCdone]
    @staticmethod
    def getUserByCriteria (criteria):
        query= {}
        user = User()
        if (criteria and isinstance(criteria, dict) ):
            query = criteria.deepcopy()
            for field_name in query.keys():
                if field_name not in user._fields:
                    del query[field_name]
            try :
                qSet = user.objects(__raw__=query)
                print("Get User Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None
    #query by id (unique)==>> Returns User Document object
    @staticmethod
    def getUserById ( objid):
        if (objid):
            return User.objects(id=objid).first()
        return None
    #query by username (unique) ==>> Returns User Document object
    @staticmethod
    def getUserByUserName ( uname):
        if (uname):
            return User.objects(username=uname).first()
        return None
    #query by email (unique) ==>> Returns User Document object
    @staticmethod
    def getUserByEmail ( em):
        if (em):
            return User.objects(email=em).first()
        return None
        
    #Create
    
    
    # it will validate with schema and save
    @staticmethod
    def createUser (thedict):
        if ( thedict and isinstance(thedict, dict) and DataModelValidator.check(UserSchema_,thedict)):
            try:
                user = User(**thedict)
                user.timecreated = datetime.datetime.now()
                user.timeupdated = user.timecreated
                user.save()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False
    #Update
    
    
    # it will reload, validate and update
    @staticmethod
    def updateUserById (objid, udict):
        if (objid and isinstance(udict, dict) ):
            #user = User.objects(pk=objid).first()
            return User.internalupdateuser(User.getUserById(objid), udict)
        else:
            return False
    @staticmethod
    def updateUserByUserName (uname, udict):
        if (uname and isinstance(udict, dict) ):
            return User.internalupdateuser(User.getUserByUserName(uname), udict)
        else:
            return False
    @staticmethod
    def updateUserByEmail (em, udict):
        if (em and isinstance(udict, dict) ):
            return User.internalupdateuser(User.getUserByEmail(em), udict)
        else:
            return False

    
    #delete
    
    
    # it will delete
    #
    @staticmethod
    def deleteUserById (objid):
        if (objid  ):
            #user = User.objects(pk=objid).first()
            return User._internaldeleteuser(User.getUserById(objid))
        else:
            return False
    @staticmethod
    def deleteUserByUserName (uname):
        if (uname  ):
            return User._internaldeleteuser(User.getUserByUserName(uname))
        else:
            return False
    @staticmethod
    def deleteUserByEmail (em):
        if (em  ):
            return User._internaldeleteuser(User.getUserByEmail(em))
        else:
            return False
    


        
