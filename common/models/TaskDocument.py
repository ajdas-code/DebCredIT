from ConfigConstants import *
from mongoengine import *
import datetime


"""
This document refers to Scheduled task template created from the user wizard
To query this DictField will be in the following way :
TaskDocument.objects(userid__id__name="Steve").
for details -- see @
>>> db.note.findOne()
>>> {
    "_id": ObjectId("'0'*24")
    "someData": {
        "someID": {
            {"name": "Steve", "age":25}
        }
    }
}

"""

class TaskDocument (DynamicDocument):
    
    #Name of the scheduled task
    taskname = StringField(max_length=200, required=True)
    
    #Start date for the task to be scheduled
    startdate = DateTimeField(default=datetime.datetime.utcnow)
    
    # End date to express till
    enddate= DateTimeField()
    
    # Frequency of schduled payments - See ConfigConstants.FREQ_TYPES# for details
    frequency= StringField(max_length=20,choices=ConfigContants.FREQ_TYPES)
    
    # equivalant cron expression for frequency - to make reads easy
    cronexpression = StringField()
    
    # enable and disable a scheduled task
    isenabled = BooleanField(default=False)
    
    # amount of money moved
    amount = DecimalField(min_value=0, force_string=False, precision=2, rounding='ROUND_HALF_DOWN',required=True)
    
    # currentcy of the above money; usually it is the sane as user instrument currency
    currency = StringField(max_length=20,required=True,choices=ConfigContants.IN_CURRENCY )
    
    # Document reference to User
    userid =  DictField(required=True)
    
    # Document reference to instrument
    userintrumentid =  DictField(required=True)
    
    # Document reference to the payee
    payeeid =  DictField(required=True)

    #Create date
    timecreated = DateTimeField()
    
    meta = {'db_alias': ConfigConstants.DB_ALIAS,'collection': 'taskdocument', 'index': ['timecreated']}
