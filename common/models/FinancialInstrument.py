from mongoengine import *
import datetime,pprint
import json, bson
import sys, traceback

from User import *
from BridgeObjects import *
from ConfigConstants import *

#Base Instrument Class
class BaseInstrument (EmbeddedDocument):
    # required for AVS verification
    #Name of the use
    name = StringField(max_length=50, required=True)
    #Phone no of the user
    phone = StringField(max_length=20, required=True)
    # country code
    countrycode = StringField(max_length=3, required=True)
    #address
    address = StringField(max_length=300, required=True)
    #zipcode
    zipcode = StringField(max_length=10, required=True)
    #email - dajitesh@gmail.com
    email = EmailField(required=True)
    
    currency = StringField(max_length=3, required=True,choice=ConfigConstants.ALL_CURRENCY)
    # Details of the input instruments that will be used for topups
    # type of instruments
    instrumenttype = StringField(max_length=10, required=True,default=ConfigConstants.CREDIT,choice=ConfigConstants.ALL_INSTRUMENT_TYPES)
    
    # instrument number
    # for debit card,credit card, bank for ach,
    # ==>> crypto miles, points and cashback NOT YET IMPLEMENTED
    # Required for Random charge auths - less than 1 unit of currency
    #is the instrument verified - to stop abuse - default:False
    isverified = BooleanField(default=False)
    #is the randomn auth done
    israndomauth = BooleanField(default=False)

    meta = {'allow_inheritance': True}
        
#Cashback
class CashBackInstrument (BaseInstrument):
    isenabled = BooleanField(default=False)
    

#Plastic support
#credit card
class CreditCardInstrument (BaseInstrument):
    accountnumber = StringField(max_length=20, required=True)
    networkType = StringField(max_length=10,required=True,choice=ConfigConstants.SUPPORTED_CARD_NETWORK)
    verificationcode = StringField(max_length=10)
    validdate = DateTimeField(required=True)
    
#debit card
class DebitCardInstrument (CreditCardInstrument):
    issuerbank = StringField(max_length=20, required=True)
    

#Bank
class BankInstrument (BaseInstrument):
    accountnumber = StringField(max_length=20, required=True)
    accounttype = StringField(max_length=15, required=True,choice=ConfigConstants.BANK_ACNT_TYPE)
    transfertype = StringField(max_length=20, required=True, choice =ConfigConstants.FIN_ID_CODE_TYPES )
    routingcode = StringField(max_length=20, required=True)
    bankname = StringField(max_length=20, required=True)
    
#Crypto
class CryptoInstrument (CashBackInstrument):
    walletaddress = StringField(max_length=50, required=True)
    walleturi = URLField()

#Points
class PointsInstrument (CashBackInstrument):
    conversionratio = IntField(required=True)
    connectionAPI = DictField()

#miles
class MilesInstument (PointsInstrument):
    issuerOrg = StringField(max_length=20, required=True)

    
class Wallet (DynamicDocument):
    
    #FK - Owner of the instument
    user = ReferenceField(User,passthrough=True,reverse_delete_rule=CASCADE,required=True,unique=True)
    

    primaryinstrument = EmbeddedDocumentField(BaseInstrument)
    otherinstrumentList = EmbeddedDocumentListField(BaseInstrument)
    
    
    # time created : Time the document 1st saved
    timecreated = DateTimeField()
    timeupdated = DateTimeField()
    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'wallet', 'index': ['user','instrumenttype']}

    #Static methods
    #C R U D Operations
    
    #Read
    
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getWalletByUser (usr):
        if (usr):
            try :
                qSet = Wallet.objects(user__in=User.objects.filter(id=usr.id))
                print("Get FinancialInstrument Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None

    @staticmethod
    def getPrimaryFIFromWallet (usr):
        fi = Wallet.getWalletByUser(usr)
        if (fi != None and fi['primaryinstrument']):
            return (fi['primaryinstrument']).to_json()
        else:
            return None

    @staticmethod
    def getOtherFIsFromWallet (usr):
        fi = Wallet.getWalletByUser(usr)
        if (fi != None and fi['otherinstrumentList']):
            return json_util.dumps((fi['otherinstrumentList']).to_mongo())
        else:
            return None
            


    #Create
    
    
    # it will validate with schema and save
    @staticmethod
    def createWallet (usr):
        if (usr) :
            try:
                fi = Wallet()
                fi.user = usr
                fi.timecreated = datetime.datetime.now()
                fi.timeupdated = fi.timecreated
                fi.save()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False
            
    #Update
    @staticmethod
    def addPrimaryFIOnWallet(usr,profiledict,fitypedict,instrumentdict):
        if (usr and isinstance(profiledict, dict) and isinstance(fitypedict, dict) and isinstance(instrumentdict, dict)):
            
            fi = Wallet.getWalletByUser(usr)
            #validate
            if (fi and DataModelValidator.check(BaseFIProfileSchema_,profiledict) and
                DataModelValidator.check(BaseFITypeSchema_,fitypedict)):
                switcher = {
                    ConfigConstants.CREDIT: (CreditCardSchema_,globals()["CreditCardInstrument"]()),
                    ConfigConstants.DEBIT: (DebitCardSchema_,globals()["DebitCardInstrument"]()),
                    ConfigConstants.BANK: (BankSchema_,globals()["BankInstrument"]()),
                    ConfigConstants.CRYPTO: (CryptoSchema_,globals()["CryptoInstrument"]()),
                    ConfigConstants.MILES: (MilesSchema_,globals()["MilesInstument"]()),
                    ConfigConstants.POINTS: (PointsSchema_,globals()["PointsInstrument"]()),
                    ConfigConstants.CASHBACK: (CashBackSchema_,globals()["CashBackInstrument"]()),
                    
                }
                inskey = str(fitypedict['instrumenttype']).lower()
                (genericSchema,basefidocument) = switcher.get(inskey,(None,None))

                if (genericSchema and DataModelValidator.check(genericSchema,instrumentdict )):
                    #join all three dicts
                    udict={**profiledict, **fitypedict,**instrumentdict}
                    #pprint.pprint(basefidocument._fields)
                    #pprint.pprint(udict)                    
                    
                    for key in udict.keys():
                        if key in basefidocument._fields.keys():
                            setattr(basefidocument, key, udict[key])
                        
                    fi.timeupdated = datetime.datetime.now()
                    oldbasefidocument = None
                    if (fi.primaryinstrument ):
                        oldbasefidocument = fi.primaryinstrument
                    fi.primaryinstrument = basefidocument
                    if (oldbasefidocument):
                        if (fi.otherinstrumentList):
                            fi.otherinstrumentList.append(oldbasefidocument)
                        else:
                            fi.otherinstrumentList =[oldbasefidocument]
                    try:
                        fi.save()
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
    def deletePrimaryFIOnWallet (usr):
        if (usr):
            fi = getWalletByUser(usr)
            if ( fi) :
                if (fi.otherinstrumentList):
                    fi.primaryinstrument = fi.otherinstrumentList.pop(0)
                else:
                    fi.primaryinstrument = None
                try:
                    fi.save()
                    return True
                except:
                    traceback.print_exc()
                    return False
                return True
            else:
                return False
        else:
            return False
    

        
