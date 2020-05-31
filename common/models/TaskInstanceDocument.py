from ConfigConstants import *
from mongoengine import *
import datetime
from BridgeObject import *
import json, bson
import sys, traceback
from TaskDocument import *


"""
This document refers to Scheduled task instance created on the work table

"""

class TaskInstance (DynamicDocument):
    
    # Document reference to the template scheduled task. Please note - this is a lazy ref as there are infinite instances
    task =  ReferenceField(Task,passthrough=True,reverse_delete_rule=True,required=True,unique=True)
    
    #Instance Start date
    instancerundate = DateTimeField(default=datetime.datetime.utcnow)
    
    #Status of the job
    runstatus= StringField(max_length=10,choices=ConfigContants.JOB_STATUS)
    
    # retry count
    retrycount = IntField(max_value=ConfigConstants.RETRY_LIMIT)

    # time created : Time the document 1st saved
    timecreated = DateTimeField()
    timeupdated = DateTimeField()

    meta = {'db_alias': ConfigConstants.DB_ALIAS, 'collection': 'taskinstance','index':['task']}
    
    
    #Static methods
    #C R U D Operations
    
    #Read
    
    #Return Cursor wrapped in queryset
    #please "del <querySet>" after use
    @staticmethod
    def getInstaceByTask (tsk):
        if (tsk):
            try :
                qSet = Account.objects(task__in=Task.objects.filter(id=tsk.id))
                print("Get Account Query: {}".format(qSet._query))
                return qSet.first()
            except:
                traceback.print_exc()
                return None
        else:
            return None
            
    # it will validate with schema and save
    @staticmethod
    def createInstance (tsk, thedict):
        if (tsk):
            if ( thedict && isinstance(thedict, dict) && BridgeObjects.DataModelValidator.check(TaskInstanceSchema_,thedict)):
                try:
                    instance = TaskInstance(**thedict)
                    instance.timecreated = datetime.datetime.now()
                    instance.timeupdated = instance.timecreated
                    instance.task = user
                    instance.save()
                    return True
                except:
                    traceback.print_exc()
                    return False
            else:
                return False
        else:
            return False
    
    @staticmethod
    def deleteInstance (instance):
        
        try:
            if (instance):
                instance.delete()
                return True
            else:
                return False
        except:
            traceback.print_exc()
            return False