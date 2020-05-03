from schema import Schema, And, Use, Optional, SchemaError
from MongoDataStore import *
from ConfigConstants import *
import datetime



"""
Set of Bride objects to synchronize the mongoose documents (javascript) with mongoengine documents (python)
"""


class BridgeObject(object) :
    
    
    
    def __init__(self):
        pass
    
    def check(self,schema, conf):
        try:
            schema.validate(conf)
            return True
        except SchemaError:
            return False
            
    def attributes(self):
        return vars(self)


class User (BridgeObject) :
    # class attr
    # username email name, countrycode, phone,isactive
    Schema_ = Schema({'name': And(Use(str)),
    'username': And(Use(str)),
    'roles': And(Use(str)),
    'email': And(Use(str)),
    'countrycode': And(Use(str)),
    'phone': And(Use(str)),
    'timecreated': And(Use(lambda date: datetime.datetime.strptime(date, "%m/%d/%Y"))),
    'storeValue': And(Use(float))
    'isactive': And(Use(bool))
    },ignore_extra_keys=True)
    
    def __init__(self):
        super(User,self).__init__()
    
    
    
    def setUserObjfromDict (self, inDict):
        if (super(User, self).check(User.Schema_,inDict)):
            self.__dict__.update(inDict)
        else:
            raise ValueError("Unable to extract user object, keys and types mismatch!!!")

    
class Payee (BridgeObject) :
    
    # name, countrycode, phone,address, transfertype, bankname ,branchcode,bankcode,accountno, currency
    Schema_ = Schema({'name': And(Use(str)),
    'address': And(Use(str)),
    'countrycode': And(Use(int)),
    'phone': And(Use(int)),
    'transfertype': And(Use(str)),
    'bankname': And(Use(str)),
    'branchcode': And(Use(str)),
    'bankcode': And(Use(str)),
    'accountno': And(Use(str)),
    'currency': And(Use(str)),
    })
    
    
    def __init__(self,obj,name):
        super(Payee,self).__init__(obj,name)
    
    def setUserObjfromDict (self, inDict):
        if (super(Payee, self).check(Payee.Schema_,inDict)):
            self.__dict__.update(inDict)
        else:
            raise ValueError("Unable to extract Payee object, keys and types mismatch!!!")


class FinancialInstrument (BridgeObject) :

    # name,address, phone, zipcode, instrumenttype, instumentnumber, validdate, verificationcode, currency
    Schema_ = Schema({'name': And(Use(str)),
    'address': And(Use(str)),
    'countrycode': And(Use(int)),
    'phone': And(Use(int)),
    'zipcode': And(Use(int)),
    'instrumenttype': And(Use(str)),
    'instumentnumber': And(Use(str)),
    'validdate': And(Use(lambda date: datetime.datetime.strptime(date, "%m/%d/%Y"))),
    'verificationcode': And(Use(str)),
    'currency': And(Use(str)),
    },ignore_extra_keys=True)
   
    
    def __init__(self,obj,name):
        super(FinancialInstrument,self).__init__(obj,name)
    

    def setUserObjfromDict (self, inDict):
        if (super(FinancialInstrument, self).check(FinancialInstrument.Schema_,inDict)):
            self.__dict__.update(inDict)
        else:
            raise ValueError("Unable to extract FinancialInstrument object, keys and types mismatch!!!")
