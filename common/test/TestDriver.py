from abc import ABC, abstractmethod

from mongoengine import *
import datetime,time
import json, bson,pprint
import sys, traceback

from ConfigConstants import *

from User import *
from Account import *
from Payee import *
from FinancialInstrument import *
from BridgeObjects import *
from MongoDataStore import *
from CustomCSVReader import *
from Entity import *


class Test(object):
    
    def __init__(self,configfilename="testdata.ini"):

        #attr
        self.usr = None
        self.acnt = None
        self.pye = None
        self.wallet = None
        self.currentdc = None
        self.dbengine = None

        #reading test data base data
        if (configfilename):
            self.config = DBConfigReader(configfilename)
        else:
            traceback.print_exc()
            raise ValueError("Initialize error! Check the the input files")


        #creating a conection to test db - Connect
        try:
            self.config.toString()
            print("Connecting to DB host @ -->{0}".format(self.config.getHost()))
            self.dbengine = connect(db=self.config.getDB(),host=self.config.getHost(),alias=ConfigConstants.DB_ALIAS)
        except:
            traceback.print_exc()
            self.dbengine = None

        #Sanity check: has this initialized propery
        if (not self.dbengine):
            raise ValueError("Error in initializing Test Driver")


    def reset (self):
        self.usr = None
        self.acnt = None
        self.pye = None
        self.wallet = None
        self.currentdc = None
        
        
    def cleanup(self):
        try:
            disconnect()
        except:
            traceback.print_exc()
        self.dbengine = None
        self.reset()

    def processATestRecord (self, dc):

        self.currentdc = dc
        if (not isinstance(dc, DataContainer)):
            raise ValueError("DataContainer obj required")

        #user Entity
        ue = UserEntity(self.currentdc)
        ue.createANDread()
        ue.updateANDread()
        self.usr = ue.docReference()

        #account entity
        ae = AccountEntity(self.currentdc)
        ae.createANDread(self.usr)
        ae.updateANDread(self.usr)
        self.acnt = ae.docReference()

        #payee entity
        pe = PayeeEntity(self.currentdc)
        pe.createANDread(self.usr)
        pe.updateANDread(self.usr)
        self.pye = pe.docReference()

        #wallet entity
        we = WalletEntity(self.currentdc)
        we.createANDread(self.usr)
        we.updateANDread(self.usr)
        self.wallet = we.docReference()


        
        #cleanup
        we.delete()
        pe.delete(self.usr)
        ae.delete()
        ue.delete()

        self.reset()


# test methods
if __name__ == "__main__":

    #setup
    test = Test("testdata.ini")
    builder = TestDataBuilder("TestData_DebCredit.csv")
    pprint.pprint("-----------@@Main--------")

    #get test data steam
    for item in builder.processNext():

        #print data
        print("_____________")
        print("User attr")
        pprint.pprint(getattr(item,"User",None))
        print("_____________")
        print("Account attr")
        pprint.pprint(getattr(item,"Account",None))
        print("_____________")
        print("Payee attr")
        pprint.pprint(getattr(item,"Payee",None))
        print("_____________")
        print("Wallet attr")
        pprint.pprint(getattr(item,"Wallet",None))
        print("_____________")


        #perform test
        try:
            test.processATestRecord(item)
            print("^^^^^^^^^^^^^Success^^^^^^^^^^^^^")
        except:
            traceback.print_exc()
        time.sleep(2)        
        print("Next...")

        
    pprint.pprint("-----------@@Done--------")
    test.cleanup()

    
