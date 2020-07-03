import json
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import *
from MongoDataStore import *
from ConfigConstants import *

class RuntimeContext () :
    __instance = None
    def getInstance():
        """ Static access method. """
        if RuntimeContext.__instance == None:
            RuntimeContext()
        return RuntimeContext.__instance
    getInstance = staticmethod(getInstance)
    
    def __init__(self):
        self.schd = None
        self.logger = None
        self.jobstat = {}
        self.starttime = datetime.datetime.now()

    def __del__(self):
        self.schd = None
        self.logger = None
        self.jobstat = {}
        self.starttime = None
        
    def getSchd(self):
        if (not self.schd):
            raise ValueError("Set the schedular reference first before calling")
        return self.schd
    def setSchd(self, schd):
        if (not schd):
            raise ValueError("Set the schedular reference ")
        self.schd = schd
        
    def getLogger(self):
        if (not self.logger):
            raise ValueError("Set the logger reference first before calling")
        return self.logger
    def setLogger(self, logger):
        if (not logger):
            raise ValueError("Set the logger reference ")
        self.logger = logger
        
    def appendSystemJobProperties (self, jobDict):
        key = jobDict['id']
        if (key) :
            self.jobstat[key] = {}
            self.jobstat[key]['properties'] = jobDict
            self.jobstat[key]['retry'] = 0
        else :
            print('Job id - {} not found'.format(key))
    def getJSONDump (self):
        return json_dump(self.jobstat)
        
    def getJobStat (self):
        return self.jobstat
    
    def setJobStat (self, jobStat):
        self.jobstat = jobStat
        
