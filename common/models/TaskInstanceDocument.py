from ConfigConstants import *
from mongoengine import *
import TaskDocument
import datetime


"""
This document refers to Scheduled task instance created on the work table

"""

class TaskInstanceDocument (DynamicDocument):
    
    # Document reference to the template scheduled task. Please note - this is a lazy ref as there are infinite instances
    taskid =  LazyReferenceField(TaskDocument,passthrough=True, dbref=True, reverse_delete_rule=0,required=True)
    
    #Instance Start date
    instancerundate = DateTimeField(default=datetime.datetime.utcnow)
    
    #Status of the job
    runstatus= StringField(max_length=10,choices=ConfigContants.JOB_STATUS)
    
    # retry count
    retrycount = IntField(max_value=ConfigConstants.RETRY_LIMIT)

    

    meta = {'db_alias': ConfigConstants.DB_ALIAS, 'collection': 'taskinstancedocument','index':['taskid']}
   