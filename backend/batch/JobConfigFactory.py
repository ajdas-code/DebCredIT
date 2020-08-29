import uuid
import pprint
from datetime import datetime, timedelta
from configparser import ConfigParser
from ConfigConstants import *
from apscheduler.triggers.cron import CronTrigger


""" This is a singleton class uses to create triggers for all system batch jobs, we need to setup
    DebCredit config file under the ../config directory
"""




class BatchConfigReader():
    
           
    def __init__(self,filename=IniFileTags.FILE_PATH):
        print("Checking file ...:{0}".format(filename))
        if (not IniFileTags.checkValidfilename(filename)):
            raise ValueError("File not usable")
        
        self.parser = ConfigParser()
        # Open the file with the correct encoding
        try:
            
            with open(filename, "r", encoding="utf-8") as f:
                self.parser.readfp(f)
        except:
            raise ValueError("Error in parsing ini file")
            
            

    def __str__(self,tag):
        print (self.parser._sections[tag])
    
    def getConfiguration(self,tag):
        return self.parser._sections[tag]
        
    
        
            

            
class JobConfigFactory():
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if JobConfigFactory.__instance == None:
            JobConfigFactory()
        return JobConfigFactory.__instance
    
    
    def __init__(self):
        """ Virtually private constructor. """
        self.globalparam = {}
        if JobConfigFactory.__instance != None:
           raise Exception("This class is a singleton!")
        else:
            try:
                self.batchconfigreader = BatchConfigReader()
                JobConfigFactory.__instance = self
                self.globalparam = self.batchconfigreader.getConfiguration(IniFileTags.BATCH_GLOBAL_TAG)
                print("Global Batch Configuation -->")
                pprint.pprint(self.globalparam)
            except:
                JobConfigFactory.__instance = None
                raise Exception("Ini file reading Error")

    def setSchedular (self, schld):
        self.schld = schld

    def _get_trigger(self, expression):
        # type: (str) -> CronTrigger
        """
        Evaluates a CronTrigger obj from cron expression
        :param expression: String representing the crons five first fields, e.g : '* * * * *'
        :return: A CronTrigger
        """
        vals = expression.split()
        vals = [(None if w == '?' else w) for w in vals]
        return CronTrigger(minute=vals[0], hour=vals[1], day=vals[2], month=vals[3], day_of_week=vals[4])

    def createTrigger (self, tag):
        if (not tag):
            raise ValueError("Tag cannot be empty")
        customparams = {}
        customparams = self.batchconfigreader.getConfiguration(tag)
        if (not any(customparams)):
            print("not custom params")
        else:
            customparams.update(self.globalparam)
        #create the Triggers
        print("...",customparams,"...")
        if not customparams[IniFileTags.CRONEXPRESSION]:
            customparams[IniFileTags.CRONEXPRESSION] = ConfigConstants.DAILY_CRON_EXPRESSION
        return CronTrigger.from_crontab(customparams[IniFileTags.CRONEXPRESSION])
        
        
    def createMaxInstance (self, tag):
        if (not tag):
            raise ValueError("Tag cannot be empty")
        customparams = {}
        customparams = self.batchconfigreader.getConfiguration(tag)
        if (not any(customparams)):
            print("not custom params")
        else:
            customparams.update(self.globalparam)
        #get the max instqance
        if not customparams[IniFileTags.MAX_INSTANCE]:
            customparams[IniFileTags.MAX_INSTANCE] = ConfigConstants.MAX_INSTANCE
        return int(customparams[IniFileTags.MAX_INSTANCE])
        
    def createCoalesce (self, tag):
        return True;
        
    def createName (self, tag):
        return tag
    
    def createId (self,tag):
        return str(uuid.uuid1())
    
    def createArgs(self, tag):
        return [self.schld,]
        
    def createReplaceExisting(self,tag):
        return True;
    
    def createTimeZone(self):
        return self.globalparam[IniFileTags.TIMEZONE_TAG]
        
            
# test methods
if __name__ == "__main__":
    
    """Main code"""
    s = JobConfigFactory()
    print (s)
    s = JobConfigFactory.getInstance()
    print (s)
    s = JobConfigFactory.getInstance()
    print (s)
