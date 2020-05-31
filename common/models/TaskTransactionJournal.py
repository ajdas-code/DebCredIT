ffrom ConfigConstants import *
from mongoengine import *
import datetime
from BridgeObject import *
import json, bson
import sys, traceback

from User import *
from Account import *
from Payee import *
from FinancialInstrument import *
from TaskDocument import *
from TaskInstanceDocument import *



"""
This document is collection of journals (appends) - this will be used to generate monthly reports of the user and our business metrics

"""

class TaskTransactionJournal (DynamicDocument):
    

       
    #Instance Start date
    executionrdate = DateTimeField(default=datetime.datetime.utcnow)
    
    # amount of money moved
    amount = DecimalField(min_value=0, force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)
    
    # currentcy of the above money; usually it is the sane as user instrument currency
    incurrency = StringField(max_length=20,required=True,choices=ConfigContants.IN_CURRENCY )

    # currentcy of the above money; usually it is the sane as user instrument currency
    outcurrency = StringField(max_length=20,required=True,choices=ConfigContants.OUT_CURRENCY )
        
    #fee paid
    feeamount = DecimalField(min_value=0, force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)
    
    # currentcy of the above money; usually it is the sane as user instrument currency
    feecurrency = StringField(max_length=20,required=True,choices= ConfigContants.OUT_CURRENCY )

    # Document reference to User object id as it is read only copy from  mongoose/Node JS
    userid =  DictField(required=True)
    
    # Document reference to Instrument  object id  as it is read only copy from  mongoose/Node JS
    userintrumentid =  DictField(required=True)
    
    # Document reference to the payee  object id  as it is read only copy from  mongoose/Node JS
    payeeid =  DictField(required=True)
    
    # Document reference to the template scheduled task. Please note - this is a lazy ref as there are infinite instances
    taskid =  LazyReferenceField(TaskDocument,passthrough=True, dbref=False, reverse_delete_rule=0,required=True)

    # Document reference to the template scheduled task. Please note - this is a lazy ref as there are infinite instances
    taskinstanceid =  LazyReferenceField(TaskInstanceDocument,passthrough=True, dbref=False, reverse_delete_rule=0,required=True)
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS, 'collection': 'tasktransactionjournal','index':['executionrdate'] }
    

    
   