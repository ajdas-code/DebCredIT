#CSV data to dicts
import os,csv,time,sys,pprint,copy
from ConfigConstants import *
from Conversion import *


SkipConversion_ = ['phone','countrycode','verificationcode','accountnumber','zipcode',]
# Class to convert a csv file to a list of dictionaries.

class DataContainer(object):
    PROFILE = 'profile'
    FI = 'fi'
    INSTRUMENT = 'instrument'
    
    @staticmethod
    def processWallet(adict):
        profileattbr = ['name','address','countrycode','phone','zipcode', 'email']
        fiattbr = ['instrumenttype','currency']
        instrumentdict = {}
        if ( not adict or not isinstance(adict,dict) ):
            return None
        else:
            instrumentdict = copy.deepcopy(adict)
        profiledict = {}
        fidict = {}
        for ikey,ivalue in adict.items():
            if (ikey in profileattbr):
                profiledict.update({ikey:ivalue})
                del instrumentdict[ikey]
            elif (ikey in fiattbr):
                fidict.update({ikey:ivalue})
                del instrumentdict[ikey]
            else:
                pass
        return { DataContainer.PROFILE:profiledict,DataContainer.FI:fidict, DataContainer.INSTRUMENT:instrumentdict}
        
        


class TestDataBuilder (object):


    def __init__(self,filename):
        if (filename and IniFileTags.checkValidfilename(filename)):
            self.filename = filename
        else:
            raise ValueError("Filename either doesn't exist or unable to load")
    
        
    def processNext(self):
     
        # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs
        reader = csv.DictReader(open(self.filename, 'r'))
        for line in reader:
            datacontainer = DataContainer()
            for item in line.items():
                (tempkey,value) = item
                (attrb,innerkey) = tempkey.split("_")
                if (innerkey not in SkipConversion_):
                    value = Convdate().conv(value)                
                    value = Convf().conv(value)

                
                if (attrb not in datacontainer.__dict__):
                    datacontainer.__dict__.update({attrb:{innerkey:value}})
                else:
                    #setattr(datacontainer,attrb,{innerkey:value})
                    datacontainer.__dict__[attrb].update({innerkey:value})
            datacontainer.Wallet = DataContainer.processWallet(datacontainer.Wallet)
            yield datacontainer
    

# Calls the csv_dict_list function, passing the named csv

if __name__ == "__main__":
    
    """Main code"""
    builder = TestDataBuilder(sys.argv[1])
    pprint.pprint("-----------@@Main--------")
    
    
    for item in builder.processNext():
        print("_____________")
        
        print("User attr")
        pprint.pprint(getattr(item,"User",None))
        
        print("Account attr")
        pprint.pprint(getattr(item,"Account",None))
        
        print("Payee attr")
        pprint.pprint(getattr(item,"Payee",None))
        
        print("Wallet attr")
        pprint.pprint(getattr(item,"Wallet",None))
        
        #time.sleep(2)
        print("_____________")
    
