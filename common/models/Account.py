from ConfigConstants import *
from mongoengine import *
import datetime
import json, bson
import sys, traceback

from User import *
from BridgeObjects import *



class Account (DynamicDocument):
    
    #FK - Owner of the account
    user = ReferenceField(User,passthrough=True,reverse_delete_rule=CASCADE,required=True,unique=True)
    
    #amount
    amount = DecimalField(force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)

    # currency
    currency = StringField(max_length=3, required=True,choice=ConfigConstants.ALL_CURRENCY)
    
    
    #Cumulative data on account
    #total spend
    totalspend = DecimalField(force_string=False, precision=2, rounding='ROUND_HALF_DOWN', required=True)
    #total topup
    totaltopup = DecimalField(force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)

    #Max amount of  obligation - water mark
    maxpay = DecimalField(force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)

    #current cashback
    cashback = FloatField()

    
    #Tier information
    #current Tier
    tier = IntField(min_value=0,max_value=10)
    #current fee
    feepercent = FloatField(min_value=0,max_value=100, default=ConfigConstants.DEFAULT_FEE_PERCENT)
    
    # time created : Time the document 1st saved
    timecreated = DateTimeField()
    timeupdated = DateTimeField()
    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'account', 'index': ['user']}

    #Static methods
    #C R U D Operations
    
    #Read
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getAccountByUser (usr):
        if (usr):
            try :
                qSet = Account.objects(user__in=User.objects.filter(id=usr.id))
                print("Get Account Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None
    
    def getAccountLessThanTotalSpend(totalamount):
        if (totalamount > 0) :
            return Account.objects.filter(totalspend__lt = totalamount)
        else:
            return None
    def getAccountGreaterThanOrEqualToTotalSpend(totalamount):
        if (totalamount > 0) :
            return Account.objects.filter(totalspend__gte = totalamount)
        else:
            return None
    def getAccountLessThanTotalTopUp(totalamount):
        if (totalamount > 0) :
            return Account.objects.filter(totaltopup__lt = totalamount)
        else:
            return None
    def getAccountGreaterThanOrEqualToTotalTopUp(totalamount):
        if (totalamount > 0) :
            return Account.objects.filter(totaltopup__gte = totalamount)
        else:
            return None
            
    #Create
    
    
    # it will validate with schema and save
    @staticmethod
    def createAccount (user, thedict):
        if (user):
            if ( thedict and isinstance(thedict, dict) and DataModelValidator.check(AccountSchema_,thedict)):
                try:
                    acnt = Account(**thedict)
                    acnt.timecreated = datetime.datetime.now()
                    acnt.timeupdated = acnt.timecreated
                    acnt.user = user
                    acnt.save()
                    return True
                except:
                    traceback.print_exc()
                    return False
            else:
                return False
        else:
            return False
            

    #Update
    
    
    # it will reload, validate and update
    @staticmethod
    def addFundToAccount (usr,amnt):
        if (usr and (amnt > 0)):
            Account.objects(user=usr).update(inc__amount=amnt, inc__totaltopup=amnt,set__timeupdated=datetime.datetime.now())
            return True
        else:
            return False
            
    def spendFundFromAccount (usr,amnt):
        if (usr and (amnt > 0)):
            Account.objects(user=usr).modify(dec__amount=amnt, inc__totalspend=amnt,set__timeupdated=datetime.datetime.now())
            return True
        else:
            return False
            
    def updateMaxPay(usr,payamount):
        if (usr and (payamount > 0)):
            Account.objects(user=usr).update(inc__maxpay=payamount,set__timeupdated=datetime.datetime.now())
            return True
        else:
            return False
    def updateCashBack(usr,payamount):
        if (usr and usr['cashback'] and (payamount > 0)):
            Account.objects(user=usr).update(inc__cashback=payamount,set__timeupdated=datetime.datetime.now())
            return True
        else:
            return False
    def updateTierAndFees(usr, **argv):
        if (usr ):
            acnt = getAccountByUser(usr)
            if ('tier' in argv.keys()) :
                acnt.tier = argv['tier']
            if ('feepercent' in argv.keys()):
                acnt.feepercent = argv['feepercent']
            acnt.timeupdatd = datetime.datetime.now()
            acnt.save()
            return True
        else:
            return False
                
    #Delete
    # We should not delete account for an existing user
    # if user is deleted, the account will be deleted as well
    
    

        
