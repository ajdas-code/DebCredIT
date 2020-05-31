from ConfigConstants import *
from mongoengine import *
import datetime
from BridgeObject import *
import json, bson
import sys, traceback
from User import *
from Account import *
from Payee import *
from FinancialInstrument import *


class Task (DynamicDocument):
    
    #Name of the scheduled task
    taskname = StringField(max_length=200, required=True,unique=True)
    
    #Start date for the task to be scheduled
    startdate = DateTimeField(required=True,default=datetime.datetime.utcnow)
    
    # End date to express till
    enddate= DateTimeField(required=True)
    
    # Frequency of schduled payments - See ConfigConstants.FREQ_TYPES# for details
    frequency= StringField(max_length=20,required=True,choices=ConfigContants.FREQ_TYPES)
    
    # equivalant cron expression for frequency - to make reads easy
    cronexpression = StringField(required=True)
    
    # enable and disable a scheduled task
    isenabled = BooleanField(default=False)
    
    # amount of money moved
    amount = DecimalField(min_value=0, force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)
    
    # currentcy of the above money; usually it is the sane as user instrument currency
    currency = StringField(max_length=20,required=True,choices=ConfigContants.IN_CURRENCY )
    
    # Document reference to User
    user =  ReferenceField(User,passthrough=True,reverse_delete_rule=True,required=True)
    
    # Document reference to instrument
    instrument =  ReferenceField(Wallet,passthrough=True,reverse_delete_rule=True,required=True)
    
    # Document reference to the payee
    payee =  ReferenceField(Payee,passthrough=True,reverse_delete_rule=True,required=True)

    # Document reference to the payee
    account =  ReferenceField(Account,passthrough=True,reverse_delete_rule=True,required=True)

     # time created : Time the document 1st saved
    timecreated = DateTimeField()
    timeupdated = DateTimeField()
    
    
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'task', 'index': ['taskname','user','account','instrument','payee']}



    #Static methods
    #C R U D Operations
    
    #Read
    
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getAllTaskByUser (usr):
        if (usr):
            try :
                qSet = Task.objects(user__in=User.objects.filter(id=usr.id))
                print("Get Task Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None

    def getAllTaskByPayee (pye):
        if (pye):
            try :
                qSet = Task.objects(payee__in=Payee.objects.filter(id=pye.id))
                print("Get Task Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None
    
    def getAllTaskByUserAndPayee (usr,pye):
        if (usr && pye):
            try :
                qSet = Task.objects(user__in=User.objects.filter(id=usr.id) & Q(payee__in=Payee.objects.filter(id=pye.id)))
                print("Get Task Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None
            
    def getTaskByUserAndPayeeAndTaskName (usr,pye,tname):
        if (usr && pye && tname):
            try :
                qSet = Task.objects(Q(user__in=User.objects.filter(id=usr.id)) & Q(payee__in=Payee.objects.filter(id=pye.id)) &Q(taskname=tname))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None

    #---------------------------------------------

    def getAllTaskByAccount (acnt):
        if (acnt):
            try :
                qSet = Task.objects(account__in=Account.objects.filter(id=acnt.id))
                print("Get Task Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None

    
    def getAllTaskByAccountAndPayee (acnt,pye):
        if (acnt && pye):
            try :
                qSet = Task.objects(account__in=Account.objects.filter(id=acnt.id) & Q(payee__in=Payee.objects.filter(id=pye.id)))
                print("Get Task Query: {}".format(qSet._query))
                return qSet
            except:
                traceback.print_exc()
                return None
        else:
            return None
            
    def getTaskByAccountAndPayeeAndTaskName (acnt,pye,tname):
        if (acnt && pye && tname):
            try :
                qSet = Task.objects(Q(account__in=Account.objects.filter(id=acnt.id)) &
                    Q(payee__in=Payee.objects.filter(id=pye.id)) &Q(taskname=tname))
                print("Get Payee Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None
            
    #-----------------------------------------
    

    #Create
    
    
    # it will validate with schema and save
    @staticmethod
    def createPayee (usr,acnt, pye, fi, thedict):
        if ( usr && acnt && pye && fi && thedict
            && isinstance(thedict, dict)
            && BridgeObjects.DataModelValidator.check(TaskSchema_,thedict)):
            try:
                tsk = Task(**thedict)
                tsk.user = usr
                tsk.account = acnt
                tsk.instrument= fi
                tsk.payee = pye
                tsk.timecreated = datetime.datetime.now()
                tsk.timeupdated = tsk.timecreated
                tsk.save()
                return True
            except:
                traceback.print_exc()
                return False
        else:
            return False

            
    #Update
    @staticmethod
    def updateTask (tsk, udict):
        if (udict && isinstance(udict, dict)):
            if (tsk):
                for key in udict.keys():
                    if key not in [k for k,v in tsk._fields.iteritems()]
                        del udict[key]
                for key in udict.keys():
                    setattr(tsk, key, udict[key])
                tsk.timeupdated = datetime.datetime.now()
                try:
                    tsk.save()
                    return True
                except:
                    traceback.print_exc()
                    return False
            else:
                return False
        else:
            return False

            
    
    #delete
    
    
    # it will delete
    #
    @staticmethod
    def deleteTask (tsk):
        
        try:
            if (tsk):
                tsk.delete()
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False
    
