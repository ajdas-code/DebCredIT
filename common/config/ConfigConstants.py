"""
Set of ini file tags
"""

class IniFileTags():


    @staticmethod
    def checkValidfilename (filename):
        if not os.path.exists(filename):
            return False
        if not os.path.isfile(filename):
            return False
        if not os.access(filename, os.R_OK):
            return False
        return True

    #Location of Config file
    FILE_PATH = "../config/debcredit_config.ini"
    
    #Config file DB Key tags
    MONGO_TAG='db_details'
    HOST_TAG= 'host'
    PASSWORD_TAG='password'
    USER_TAG= 'user'
    DB_TAG = 'db'
    
    #config file global Batch key tags
    BATCH_GLOBAL_TAG = "batch_global_details"
    TIMEZONE_TAG = "timezone"
    EXECUTION_WINDOW = "execution_window"
    SHARDING = "sharding"
    SHARDING_ATTRIBUTE = "sharding_attribute"
    CRONEXPRESSION = "cronexpression"
    MAX_INSTANCE = "max_instance"
    
    #config file validate instrument batch
    BATCH_ENABLE_PAYMENT_INSTANCE_TAG = "batch_enable_payment_instance"
    #config file validate instrument batch
    BATCH_VALIDATE_INSTRUMENT_TAG = "batch_validate_instruments"
    #config file task instance creation batch
    BATCH_CREATE_TASK_TAG = "batch_create_task_instance"
    #config file payment execution batch
    BATCH_EXECUTE_PAYMENT_TAG = "batch_execute_payment"
    #config file capture payments batch
    BATCH_CAPTURE_PAYMENTS_TAG = "batch_capture_payments"
    #config file biz metrics collection and "enable payee batch"
    BATCH_COLLECT_BIZ_METRICS_TAG = "batch_collect_biz_metrics"
    #config file accounting reconcilation batch
    BATCH_ACCOUNTING_PAYMENTS_TAG = "batch_accounting_payments"
    #config file monthly report generation batch
    BATCH_GENERATE_REPORT_TAG = "batch_generate_report"
    



"""
   Set of Programming defaults
"""

class ConfigConstants():

    #default logger
    LOGGER_FILE = "../config/debcredit.log"
    # retry limit
    RETRY_LIMIT = 5
    
    # Default DB values if config is not available
    DEFAULT_HOST= 'mongodb://admin:qwerty@localhost/production'
    DEFAULT_DB='test',
    DEFAULT_USER='user',
    DEFAULT_PASS='12345',
    DB_ALIAS ='debit_credit'
    
    #Default cronexpression for system batch is config is not available
    DAILY_CRON_EXPRESSION = "0 0 1 ? * * *"
    MONTHLY_CRON_EXPRESSION = "0 0 23 ? * * *"
    
    # Batch job default max instance
    MAX_INSTANCE = 1
    
    #################################################################
    #
    #  Attention!!!
    #  Attention!!!
    #
    #  The following constants needs to be moved to ini config file
    #  They are NOT programming constants. Change the models as they
    #  are used there.
    #################################################################
    #
    # Job Frequence
    DAILY = 'daily'
    MONTHLY = 'monthly'
    WEEKLY = 'weekly'
    YEARLY = 'yearly'
    ONCE = 'once'
    """ alternate day or week or month or year"""
    LOOP_DAILY = 'loop_daily'
    LOOP_MONTHLY = 'loop_monthly'
    LOOP_WEEKLY = 'loop_weekly'
    LOOP_YEARLY = 'loop_yearly'
    """ bofore end of month """
    BEFORE_EOMONTH = 'before_eomonth'
    FREQ_TYPES = (DAILY,MONTHLY,WEEKLY,YEARLY,ONCE,LOOP_DAILY,LOOP_MONTHLY,LOOP_WEEKLY,LOOP_YEARLY,BEFORE_EOMONTH)
    
    # Supported Currency
    # Into the system
    USD = 'usd'# usa
    GBP = 'gbp'# uk
    SGN = 'sgn;'# singapore
    EUR = 'eur'# euro
    AED = 'aed'# UAE
    CAD = 'cad'# canada
    AUD = 'aud'# australia
    CNY = 'cny'# china
    IN_CURRENCY = (USD,GBP,SGN,EUR,AED,CAD,AUD,CNY)
    #out of the system
    INR = 'inr' # india
    PHP = 'php' # phillipines
    BDT = 'bdt'# bangladesh
    MXN = 'mxn'# mexico
    VND = 'vnd' # vietnam
    NGN = 'ngn' # nigeria
    PKR = 'pkr' # pakistan
    EGP = 'egp' # egypt
    OUT_CURRENCY = (INR,PHP,BDT,MXN,VND,NGN,PKR,EGP)
    
    
    # Status of Jobs
    NEW_JOB = "new"
    RUNNING_JOB = "running"
    ABORTED_JOB = "aborted"
    FAILED_JOB = "failed"
    COMPLETED_JOB = "completed"
    JOB_STATUS = (NEW_JOB,RUNNING_JOB,ABORTED_JOB,FAILED_JOB,COMPLETED_JOB )
    
    #Transfer Type
    WIRE = 'wire'
    ACH  = 'ach'
    
    #Financial instrument identifier code
    SWIFT = 'swift'
    IBAN = 'iban'
    IFSC = 'ifsc'
    
    #Roles
    USER = 'user'
    ADMIN  = 'admin'
    ROLE = (USER, ADMIN)
    