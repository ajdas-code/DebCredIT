""" This is a singleton class uses to initialize mongo datastore
    In order to initialize the url of database, we need to setup
    DebCredit config file under the ../config directory
"""
from mongoengine import *
from ConfigParser import *
import os.path
import traceback
from ConfigConstants import *




class DBConfigReader():
    
           
    def __init__(self,filename=IniFileTags.FILE_PATH):
        
        if (IniFileTags.checkValidFilename(filename)):
            raise ValueError("File not usable")
        parser = SafeConfigParser()
        # Open the file with the correct encoding
        with open(filename, "r", encoding="utf-8") as f:
            parser.readfp(f)
            self.password = (parser.get(IniFileTags.MONGO_TAG, IniFileTags.PASSWORD_TAG)).strip()
            self.host = (parser.get(IniFileTags.MONGO_TAG, IniFileTags.HOST_TAG)).strip()
            self.user = (parser.get(IniFileTags.MONGO_TAG, IniFileTags.USER_TAG)).strip()
            self.db = (parser.get(IniFileTags.MONGO_TAG, IniFileTags.DB_TAG)).strip()
        if not self.password:
            self.password = ConfigConstants.DEFAULT_PASS
        if not self.host:
            self.host = ConfigConstants.DEFAULT_HOST
        if not self.user:
            self.user = ConfigConstants.DEFAULT_USER
        if not self.db:
            self.db = ConfigConstants.DEFAULT_DB
            
            

    def __str__(self):
        print ('Password(encoded):', self.password.encode('utf-8'))
        print ('Password:', self.password)
        print ('host    :', self.host)
        print ('db      :', self.db)
        print ('user     :', self.user)
    
    def getPassword(self):
        return self.password
    def getHost(self):
        return self.host
    def getUser(self):
        return self.user
    def getDB(self):
        return self.db
        
            

            
class MongoDataStore():
    __instance = None
    @staticmethod
    def getInstance():
    """ Static access method. """
        if MongoDataStore.__instance == None:
            MongoDataStore()
        return MongoDataStore.__instance
    #getInstance = staticmethod(getInstance)
    
    
    def __init__(self):
        """ Virtually private constructor. """
        if MongoDataStore.__instance != None:
           raise Exception("This class is a singleton!")
        else:
            try:
                self.dbconfigreader = DBConfigReader()
                str(self.dbconfigreader)
                self.dbengine = mongoengine.connect(db=self.dbconfigreader.getDB(),username=self.dbconfigreader.getUser(),
                password=self.dbconfigreader.getPassword(),
                host=self.dbconfigreader.getHost(),alias=ConfigConstant.DB_ALIAS)
                MongoDataStore.__instance = self
            except:
                MongoDataStore.__instance = None
                raise Exception("DB connection Error")
                self.dbengine = None
    def __del__(self):
        try:
            mongoengine.disconnect(alias=ConfigConstant.DB_ALIAS)
            
        except:
            MongoDataStore.__instance = None
            raise Exception("DB connection Error")
        self.dbengine = None
                
    def getDBConfigReader(self):
        return self.dbconfigreader
        
    def getDBEngine(self):
        return self.dbengine

    def getDBAlias (self):
        return ConfigConstant.DB_ALIAS
        
            
# test methods
if __name__ == "__main__":
    
    """Main code"""
    s = MongoDataStore()
    print (s)
    s = MongoDataStore.getInstance()
    print (s)
    s = MongoDataStore.getInstance()
    print (s)