import abc
import logging
from apscheduler.schedulers import *
from apscheduler.jobstores import *
from apscheduler.executors import *
from apscheduler.events import *
from apscheduler.job  import *
from MongoDataStore import *
from ConfigConstants import *
from RuntimeContext import *


class AbstractBaseBatch(metaclass=abc.ABCMeta):

    

    def _initialize(self,schedular=None, filter=None) :
        #setting runtime context
        self.runtime = RuntimeContext.getInstance()
        if (schedular):
            self.runtime.setSchd(schedular)
        #setting up DB connections
        self.dbengine = MongoDataStore().getInstance().getDBEngine()
        self.dbalias = MongoDataStore().getInstance().getDBAlias()
        # filter - to enable sharding
        self.filterattribute = filter
    
    
    # Reader Step to return read object
    @abc.abstractmethod
    def reader(self,filter=None):
        return None
        
    
    # Processing Step to return processed object
    @abc.abstractmethod
    def processor(self,filter=None):
        return None
        
        
    # Write Step to write back/Update processed object
    @abc.abstractmethod
    def writer(self,filter=None):
        return None
        
        
    # wiring together - running the Batch
    @abc.abstractmethod
    def excute(self,filter=None):
        return None
    
    