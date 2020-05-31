
from mongoengine import *
import datetime

import json, bson
import sys, traceback

from User import *
from ConfigConstants import *
from BridgeObjects import *

#Base Instrument Class
#Cash
class CashInstrument (EmbeddedDocument):
    meta = {'allow_inheritance': True}
    

#Plastic support
#credit card
class DebitCardInstrument (CashInstrument):
    accountnumber = StringField(max_length=20, required=True)
    networkType = StringField(max_length=10,required=True,choice=ConfigConstants.SUPPORTED_CARD_NETWORK)
    verificationcode = StringField(max_length=10)
    validdate = DateTimeField(required=True)
    issuerbank = StringField(max_length=20, required=True)
    

#Bank
class BankInstrument (CashInstrument):
    accountnumber = StringField(max_length=20, required=True)
    accounttype = StringField(max_length=15, required=True,choice=ConfigConstants.BANK_ACNT_TYPE)
    transfertype = StringField(max_length=20, required=True, choice =ConfigConstants.FIN_ID_CODE_TYPES )
    routingcode = StringField(max_length=20, required=True)
    bankname = StringField(max_length=20, required=True)
    

    
class Payee (DynamicDocument):
    
    #FK - Owner of the payee
    user = ReferenceField(User,passthrough=True,reverse_delete_rule=CASCADE,required=True)
    
    # required for AVS verification
    #Name of the use
    name = StringField(max_length=50, required=True,unique=True)
    #Phone no of the user
    phone = StringField(max_length=20, required=True,unique=True)
    # country code
    countrycode = StringField(max_length=3, required=True)
    #address
    address = StringField(max_length=300, required=True)
    #email - dajitesh@gmail.com
    email = EmailField(required=True,unique=True)
    
    currency = StringField(max_length=3, required=True,choice=ConfigConstants.ALL_CURRENCY)
    # Details of the input instruments that will be used for topups
    # type of instruments
    instrumenttype = StringField(max_length=10, required=True,default=ConfigConstants.BANK,choice=ConfigConstants.OUTPUT_INSTRUMENT_TYPES)

    targetinstrument = EmbeddedDocumentField(CashInstrument)
    
    # time created : Time the document 1st saved
    timecreated = DateTimeField()
    timeupdated = DateTimeField()
    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'payee', 'index': ['user','instrumenttype']}

    #Static methods
    #C R U D Operations
    
    #Read
    
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getAllPayeeByUser (usr):
        if (usr):
            try :
                qSet = Payee.objects(user__in=User.objects.filter(id=usr.id))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None

    @staticmethod        
    def getPayeeByUserAndPayeeName (usr,pname):
        if (usr and pname):
            try :
                qSet = Payee.objects(Q(user__in=User.objects.filter(id=usr.id)) & Q(name=pname))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None

    @staticmethod
    def getPayeeByUserAndPayeePhone (usr,ph):
        if (usr and ph):
            try :
                qSet = Payee.objects(Q(user__in=User.objects.filter(id=usr.id)) & Q(phone=ph))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None

    @staticmethod
    def getPayeeByUserAndPayeeEmail (usr,em):
        if (usr and em):
            try :
                qSet = Payee.objects(Q(user__in=User.objects.filter(id=usr.id)) & Q(email=em))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None

    @staticmethod
    def _internalGetPayeeDocByAttribute (usr, **kwargs):
        payee = None
        if ('name' in kwargs.keys()):
            payee = Payee.getPayeeByUserAndPayeeName(usr,kwargs['name'])
        elif ('phone' in kwargs.keys()):
            payee = Payee.getPayeeByUserAndPayeePhone(usr,kwargs['phone'])
        elif ('email' in kwargs.keys()):
            payee = Payee.getPayeeByUserAndPayeeEmail(usr,kwargs['email'])
        else:
            payee = None
        return payee
   
    @staticmethod    
    def getTargetFIFromPayee (usr,**kwargs):
        
        payee = Payee._internalGetPayeeDocByAttribute(usr, **kwargs)
        if (payee != None and payee['targetinstrument']):
            return (payee['targetinstrument']).to_json()
        else:
            return None


    #Create
    
    
    # it will validate with schema and save
    @staticmethod
    def createPayee (usr,thedict):
        if ( usr and thedict and isinstance(thedict, dict) and DataModelValidator.check(PayeeSchema_,thedict)):
            try:
                payee = Payee(**thedict)
                payee.user = usr
                payee.timecreated = datetime.datetime.now()
                payee.timeupdated = payee.timecreated
                payee.save()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False

            
    #Update
    @staticmethod
    def addTargetFIOnPayee(usr,instrumentdict,**kwargs):
        if (usr and  isinstance(instrumentdict, dict)):
            
            payee = Payee._internalGetPayeeDocByAttribute(usr,**kwargs)
            #validate
            if (payee ):
                switcher = {
                    ConfigConstants.CASH: (CashSchema_,globals()["CashInstrument"]()),
                    ConfigConstants.DEBIT: (DebitCardSchema_,globals()["DebitCardInstrument"]()),
                    ConfigConstants.BANK: (BankSchema_,globals()["BankInstrument"]()),
                    
                }
                inskey = str(payee.instrumenttype).lower()
                (genericSchema,basefidocument) = switcher.get(inskey,(None,None))
                if (genericSchema and DataModelValidator.check(genericSchema,instrumentdict )):
                    #join all three dicts
                    udict={**instrumentdict}

                    for key in udict.keys():
                        if key in basefidocument._fields.keys():
                            setattr(basefidocument, key, udict[key])
                            
                    payee.timeupdated = datetime.datetime.now()
                    payee.targetinstrument = basefidocument

                    try:
                        payee.save()
                        return True
                    except:
                        traceback.print_exc()
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
            
    
    #delete
    
    
    # it will delete
    #
    @staticmethod
    def deletePayee (usr,**kwargs):
        if (usr):
            payee = Payee._internalGetPayeeDocByAttribute(usr,**kwargs)
            if ( payee) :
                try:
                    payee.delete()
                    return True
                except:
                    traceback.print_exc()
                    return False
                return True
            else:
                return False
        else:
            return False
    

        
