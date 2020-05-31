from schema import Schema, And, Use, Optional, SchemaError
from config.ConfigConstants import *
from urllib.parse import urlparse
import datetime,traceback
import re



"""
Set of Bride objects to the verify required data passed

"""
class DataModelValidator() :
    
    @staticmethod
    def validatedate(date_text):
        if (isinstance(date_text,datetime.datetime)):
            return True
        
        try:
            if date_text != datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
                raise ValueError
            return True
        except ValueError:
            return False
        
    @staticmethod
    def is_valid_email(email):
        if len(email) > 7:
            return bool(re.match(
                "^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))

    @staticmethod
    def uri_validator(x):
        try:
            result = urlparse(x)
            return all([result.scheme, result.netloc, result.path])
        except:
            return False

    @staticmethod
    def cronexpressionvalidator (exp_str):
        pstr = '^(*|([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])|*\/([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])) (*|([0-9]|1[0-9]|2[0-3])|*\/([0-9]|1[0-9]|2[0-3])) (*|([1-9]|1[0-9]|2[0-9]|3[0-1])|*\/([1-9]|1[0-9]|2[0-9]|3[0-1])) (*|([1-9]|1[0-2])|*\/([1-9]|1[0-2])) (*|[0-6]*\-[0-6]|[0-6])$'
        pat = re.compile(pstr)
        return bool(p.match(exp_str))

    
    @staticmethod
    def check(schema, dict):
        try:
            schema.validate(dict)
            return True
        except SchemaError:
            traceback.print_exc()
            return False



UserSchema_ = Schema(
    {
        'username': And(Use(str.lower),lambda s: len(s) > 6),
        'roles': And(Use(str.lower),lambda s: s in ConfigConstants.ROLE),
        'email': And(str,lambda s: DataModelValidator.is_valid_email(s)),
    },ignore_extra_keys=True)
    
AccountSchema_ = Schema(
    {
        'amount': And(float,lambda a: a > 0),
        'currency': And(Use(str.lower),lambda s: s in ConfigConstants.ALL_CURRENCY),
        'totalspend': And(float,lambda a: a > 0),
        'totaltopup': And(float,lambda a: a > 0),
        'maxpay': And(float,lambda a: a > 0),
    
    },ignore_extra_keys=True)



BaseFIProfileSchema_ = Schema(
    {
        'name': str,
        'address': str,
        'countrycode': Use(str.lower),
        'phone': Use(str.lower),
        'zipcode': Use(str.lower),
        'email' : And(str,lambda s: DataModelValidator.is_valid_email(s)),
    },ignore_extra_keys=True)



BaseFITypeSchema_ = Schema(
    {
        'instrumenttype': And(Use(str.lower),lambda s: s in ConfigConstants.INPUT_INSTRUMENT_TYPES),
        'currency': And(Use(str.lower),lambda s: s in ConfigConstants.ALL_CURRENCY),
    },ignore_extra_keys=True)


CreditCardSchema_ = Schema(
    {
        'accountnumber': And(str,lambda s: len(s) > 6),
        'networkType': And(Use(str.lower),lambda s: s in ConfigConstants.SUPPORTED_CARD_NETWORK),
        'verificationcode': And(str,lambda s: len(s) > 2),
        'validdate': Use(lambda s: DataModelValidator.validatedate(s)),
    },ignore_extra_keys=True)


DebitCardSchema_ = Schema(
    {
        'accountnumber': And(str,lambda s: len(s) > 6),
        'networkType': And(Use(str.lower),lambda s: s in ConfigConstants.SUPPORTED_CARD_NETWORK),
        'verificationcode': And(str,lambda s: len(s) > 2),
        'validdate': Use(lambda s: DataModelValidator.validatedate(s)),
        'issuerbank': str,
    },ignore_extra_keys=True)

BankSchema_ = Schema(
    {
        'accountnumber': And(str,lambda s: len(s) > 6),
        'accounttype': And(Use(str.lower),lambda s: s in ConfigConstants.BANK_ACNT_TYPE),
        'transfertype': And(Use(str.lower),lambda s: s in ConfigConstants.FIN_ID_CODE_TYPES),
        'routingcode': str,
        'bankname': str,
    },ignore_extra_keys=True)

CashBackSchema_ = Schema(
    {
        'isenabled': bool,
    },ignore_extra_keys=True)
    
CryptoSchema_ = Schema(
    {
        'isenabled': bool,
        'walletaddress': str,
        'walleturi': And(str,lambda s: DataModelValidator.uri_validator(s)),
    },ignore_extra_keys=True)

PointsSchema_ = Schema(
    {
        'isenabled': bool,
        'conversionratio': And(int,lambda s: s > 0 ),
        'connectionAPI': dict,
    },ignore_extra_keys=True)

MilesSchema_ = Schema(
    {
        'isenabled': bool,
        'conversionratio': And(int,lambda s: s > 0 ),
        'connectionAPI': dict,
        'issuerOrg': str,
    },ignore_extra_keys=True)
    
CashSchema_ = Schema({},ignore_extra_keys=True)

PayeeSchema_ = Schema(
    {
        'name': str,
        'address': str,
        'countrycode': Use(str.lower),
        'phone': Use(str.lower),
        'email': And(str,lambda s: DataModelValidator.is_valid_email(s)),
        'instrumenttype': And(Use(str.lower),lambda s: s in ConfigConstants.OUTPUT_INSTRUMENT_TYPES),
        'currency': And(Use(str.lower),lambda s: s in ConfigConstants.ALL_CURRENCY),
    },ignore_extra_keys=True)
          
    
TaskSchema_ = Schema(
    {
        'taskname': str,
        'startdate': Use(lambda s: DataModelValidator.validatedate(s)),
        'enddate': Use(lambda s: DataModelValidator.validatedate(s)),
        'frequency': And(Use(str.lower),lambda s: s in ConfigConstants.FREQ_TYPES),
        'cronexpression': And(str,lambda s: DataModelValidator.cronexpressionvalidator(s)),
        'amount': And(float,lambda a: a > 0),
        'currency': And(Use(str.lower),lambda s: s in ConfigConstants.ALL_CURRENCY),
    },ignore_extra_keys=True)

            
TaskInstanceSchema_ = Schema(
    {
        'runstatus': And(Use(str.lower),lambda s: s in ConfigConstants.JOB_STATUS),
        'retrycount': And(int,lambda s: s > 0 and s <= ConfigConstants.RETRY_LIMIT  ),
    },ignore_extra_keys=True)



    
