from abc import ABC, abstractmethod

import datetime,time
import json, bson,pprint
import sys, traceback

from User import *
from Account import *
from Payee import *
from FinancialInstrument import *
from BridgeObjects import *
from MongoDataStore import *


############################################################################
# ABSTRACT ENTITY
###########################################################################

class Entity(object):

    def __init__(self,dc):
        self.dc  = dc

    def createANDread(self):
        pass

    def updateANDread(self):
        pass

    def delete (self):
        pass

    def docReference(self):
        pass


################################################################
# USER ENTITY
###############################################################

class UserEntity(Entity):
    def _init__(self,dc):
        super(self.__class__,self).__init__(dc)
        self.doc = None
    def createANDread(self):
        pprint.pprint("Creating the User Document...")
        if (User.createUser(self.dc.User)):
            usr = User.getUserByEmail(self.dc.User['email'])
            if usr:
                pprint.pprint("Reading the User Document")
                pprint.pprint(usr.__dict__)
                self.doc = usr
            else:
                raise ValueError("!!!!Could not find user...create_read failed!!!")
        else:
            raise ValueError("!!!!Could not find user...creation failed!!!")

    def updateANDread(self):

        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        udict = {'username': self.dc.User['email']}
        pprint.pprint("Updating the User Document...")        
        if (User.updateUserByUserName(self.dc.User['username'],udict)):
            usr = User.getUserByEmail(self.dc.User['email'])
            if usr:
                pprint.pprint("Reading the updated User Document")                
                pprint.pprint(usr.__dict__)
            else:
                raise ValueError("!!!!Could not find user...update_read failed!!!")
        else:
            raise ValueError("!!!!Could not find user...Update failed!!!")

    def docReference(self):
        return self.doc

    def delete(self):
        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        pprint.pprint("Deleting the User Document...")        
        if (User.deleteUserByEmail(self.dc.User['email'])):
            pprint.pprint("Congrats=====Deleting  of record finished")
        else:
            raise ValueError("!!!!Could not find user...delete failed!!!")
        


################################################################
# ACCOUNT ENTITY
###############################################################

class AccountEntity(Entity):
    def _init__(self,dc):
        super(self.__class__,self).__init__(dc)
        self.doc = None
        
    def createANDread(self,usr):
        pprint.pprint("Creating the Account Document...")
        if (Account.createAccount (usr,self.dc.Account)):
            acnt = Account.getAccountByUser(usr)
            if acnt:
                pprint.pprint("Reading the Account Document")
                print("amount -->{0}, totalspend -->{1}, totaltopup -->{2}".format(acnt.amount,acnt.totalspend,acnt.totaltopup))
                self.doc = acnt
            else:
                raise ValueError("!!!!Could not find account...create_read failed!!!")
        else:
            raise ValueError("!!!!Could not find account...creation failed!!!")

    def updateANDread(self,usr):

        if (not self.doc):
            raise ValueError("Create Should be called first!!")

        pprint.pprint("adding fund to the Account Document...")        
        if (Account.addFundToAccount ( usr , 100.01)):
            acnt = Account.getAccountByUser(usr)            
            if acnt:
                pprint.pprint("Reading the updated account Document")                
                print("amount -->{0}, totalspend -->{1}, totaltopup -->{2}".format(acnt.amount,acnt.totalspend,acnt.totaltopup))                
                #validation
                assert self.doc.id == acnt.id , "Mismatch in Document ids"
            else:
                raise ValueError("!!!!Could not find account...update_read failed!!!")
        else:
            raise ValueError("!!!!Could not find account...Update failed!!!")

        
        acnt = None

        pprint.pprint("spending fund from the Account Document...")        
        if (Account.spendFundFromAccount ( usr , 100.01)):
            acnt = Account.getAccountByUser(usr)            
            if acnt:
                pprint.pprint("Reading the updated account Document")                
                print("amount -->{0}, totalspend -->{1}, totaltopup -->{2}".format(acnt.amount,acnt.totalspend,acnt.totaltopup))                
                #validation
                assert self.doc.id == acnt.id , "Mismatch in Document ids"
            else:
                raise ValueError("!!!!Could not find account...update_read failed!!!")
        else:
            raise ValueError("!!!!Could not find account...Update failed!!!")

    def docReference(self):
        return self.doc

    def delete(self):
        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        pprint.pprint("Delete User will cascade the Account document delete...")        


################################################################
# PAYEE ENTITY
###############################################################

class PayeeEntity(Entity):
    def _init__(self,dc):
        super(self.__class__,self).__init__(dc)
        self.doc = None
        
    def createANDread(self,usr):
        pprint.pprint("Creating the Payee Document...")
        if (Payee.createPayee (usr,self.dc.Payee)):
            pye = Payee.getPayeeByUserAndPayeeName(usr,self.dc.Payee['name'])
            if pye:
                pprint.pprint("Reading the Payee Document")
                print("name -->{0}, email -->{1}, phone -->{2}".format(pye.name,pye.email,pye.phone))
                self.doc = pye
            else:
                raise ValueError("!!!!Could not find Payee...create_read failed!!!")
        else:
            raise ValueError("!!!!Could not create payee...creation failed!!!")

    def updateANDread(self,usr):

        if (not self.doc):
            raise ValueError("Create Should be called first!!")

        pprint.pprint("adding CASH as funding instrument to the Payee Document...")        
        if (Payee.addTargetFIOnPayee ( usr , {},email=self.dc.Payee['email'])):
            pye = Payee.getPayeeByUserAndPayeeEmail(usr,self.dc.Payee['email'])
            if pye:
                pprint.pprint("Reading the updated Payee Document")                
                print("instrumenttype -->{0}, targetinstrument._cls -->{1}".format(pye.instrumenttype,pye.targetinstrument._cls))                
                #validation
                assert self.doc.id == pye.id , "Mismatch in Document ids"
            else:
                raise ValueError("!!!!Could not find added payee...update_read failed!!!")
        else:
            raise ValueError("!!!!Could not find Payee...Update failed!!!")

    def docReference(self):
        return self.doc

    def delete(self,usr):
        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        if (Payee.deletePayee(usr,email=self.dc.Payee['email'])):
            pprint.pprint("Congrats=====Deleting  of Payee record finished")
        else:
            raise ValueError("!!!!Could not find payee...delete failed!!!")
        
            
        
        

################################################################
# WALLET ENTITY
###############################################################

class WalletEntity(Entity):
    def _init__(self,dc):
        super(self.__class__,self).__init__(dc)
        self.doc = None
        
    def createANDread(self,usr):
        pprint.pprint("Creating the Wallet Document...")
        if (Wallet.createWallet (usr)):
            wallet = Wallet.getWalletByUser(usr)
            if wallet:
                pprint.pprint("Reading the Wallet shell  Document")
                print("owner username -->{0}, owner email -->{1}, owner.roles -->{2}".format(wallet.user.username,
                                                                                             wallet.user.email,wallet.user.roles))
                self.doc = wallet
            else:
                raise ValueError("!!!!Could not find Wallet shell...create_read failed!!!")
        else:
            raise ValueError("!!!!Could not create wallet shell...creation failed!!!")

    def updateANDread(self,usr):
        
        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        
        pprint.pprint(" ading CARD as primary funding instrument to the wallet Document...")        
        if (Wallet.addPrimaryFIOnWallet ( usr ,
                                          self.dc.Wallet['profile'],
                                          self.dc.Wallet['fi'],
                                          self.dc.Wallet['instrument'])):
            ojson = Wallet.getPrimaryFIFromWallet (usr)
            if (ojson):
                pprint.pprint("Reading back the primary FI from Wallet...")
                pprint.pprint(ojson)
            else:
                raise ValueError("!!!!Could not find added payee...update_read failed!!!")
        else:
            raise ValueError("!!!!Could not find Payee...Update failed!!!")

    def docReference(self):
        return self.doc

    def delete(self):
        if (not self.doc):
            raise ValueError("Create Should be called first!!")
        pprint.pprint("Wallet will be a CASCADE delete with user")
        


