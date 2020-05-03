from ConfigConstants import *
from mongoengine import *
import datetime
from BridgeObject import *
import json
import sys, traceback




class User (DynamicDocument):
    
    #user name e.g dajitesh
    username = StringField(max_length=30, required=True)
    #active account - to stop abuse - default:True
    isactive = BooleanField(default=True)
    #email - dajitesh@gmail.com
    email = EmailField(required=True)
    #roles - user or admin
    roles = StringField(max_length=10,required=True,choices=ConfigContants.ROLE )
    # time created : Time the document 1st saved
    timecreated = DateTimeField(required=True)
    #Name of the use
    name = StringField(max_length=50, required=True)
    #Phone no of the user
    phone = StringField(max_length=20, required=True)
    # country code
    countrycode = StringField(max_length=3, required=True)
    #StoreValue : amount
    storeValue = DecimalField(min_value=0, force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True,default=0.00)
    
    #active account - to stop abuse - default:True
    isKYCDone = BooleanField(default=True)
    kycdocumentfilename = StringField(max_length=30)
    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'user', 'index': ['username','email']}

    #Static methods
    #C R U D Operations
    
    #Read
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getUser (criteria):
        query= {}
        user = User()
        if (criteria && isinstance(criteria, dict) ):
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
    
    #Create
    # it will validate with schema and save
    @staticmethod
    def createUser (thedict):
        try:
            dataObj = BridgeObject.User()
            dataObj.setUserObjfromDict(thedict)
            user = User(**thedict)
            user.save()
            return True
        except:
            traceback.print_exc()
            return False
    
    #Update
    # it will reload, validate and update
    @staticmethod
    def updateUser (udict):
        if (criteria && isinstance(udict, dict) ):
            user = User()
            for key in udict.keys():
                if key not in [k for k,v in user._fields.iteritems()]
                    del udict[key]
            for key in udict.keys():
                setattr(user, key, udict[key])
            try:
                user.modify(udict)
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False
    
    #delete
    # it will delete
    #
    @staticmethod
    def deleteUser (criteria):
        
        try:
            #get the user documents
            querySet = getUser(criteria)
            #querySet.delete()
            if (querySet):
                for item in querySet:
                    item.delete()
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False

        