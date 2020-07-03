from __future__ import print_function
import os
import time
import atexit
from datetime import datetime, timedelta
from pytz import utc, timezone

import sys
import inspect
from cmd import Cmd
import logging
from apscheduler.schedulers import *
from apscheduler.jobstores import *
from apscheduler.jobstores.mongodb import *
from apscheduler.executors import *
from apscheduler.events import *
from apscheduler.job  import *
from MongoDataStore import *
from ConfigConstants import *
from RuntimeContext import *


            

class Listener():
    #global event dispatcher
    @staticmethod
    def listenAndDispatchEvent(event):
        context = RuntimeContext.getInstance()
        dispatcher = EventDispatcherFactory.getInstance(event)
        #check if normaal or
        if event.exception:
            #error/exception scenario
            print ('The task is wrong! ! ! ! ! ! ')
            #check if qualify for retry??
            # Use the context to check if qualify for retry then -
            # reschedule the job of immidiate execution
            # else log and record the txn table in mongo as failed transaction
        else:
            #normal scenario
            print ('Tasks run as usual...')
            # log and  record the txn table in mongo as failed transaction
        

class Jobs():
    
    # batch_validate_instruments job
    @staticmethod
    def enablePamentInstanceJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        
        print('--')
    
    # batch_validate_instruments job
    @staticmethod
    def validateInstrumentsJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        
        print('--')

    # batch_create_task_instance job
    @staticmethod
    def createTaskInstanceJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')

    # batch_execute_payment job
    @staticmethod
    def executePaymentJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')

    # batch_capture_payments job
    @staticmethod
    def capturePaymentJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')

    # batch_collect_biz_metrics job
    @staticmethod
    def collectBizMetricsJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')

    # batch_accounting_payments job
    @staticmethod
    def accountingPaymentJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')

    # batch_generate_report job
    @staticmethod
    def generateReportJob (schedularRef):
        print('--')
        #tbd
        print('Run job: Job={}, datetime={}'.format(inspect.stack()[0][0].f_code.co_name, datetime.now()))
        print('--')
        


class SysPrompt(Cmd):
    prompt = 'DebCredIt> '
    intro = "Welcome to DebCredIt schedular admin console! Type ? to list commands"

    def __init__(self,schedular):
        self.schd = schedular

    def do_pause(self,inp):
        self.schd.pause();
        print("schedular paused...")
        
    def help_pause(self):
        print("Pause the system schedular. !!!Warning!!! Pausing longer that 3 mins cause job miss!")
        
    def do_resume(self,inp):
        self.schd.resume();
        print("schedular resumed...")
        
    def help_resume(self):
        print("Resume the system schedular. !!!Warning!!! Pausing longer that 3 mins cause job miss!")
        
    def do_isrunning(self,inp):
        val = self.schd.running();
        print("Status...'{}'".format(val))
    
    def help_isrunning(self):
        print("Check if the system schedular. True means <running>, False means <not running>")

    def do_getalljobs(self,inp):
        val = self.schd.get_jobs()
        print("Jobs:")
        print(*val, sep = "\n")
        output = []
        for no in range(len(val)):
            output.extend((job(val[no])).__getstate__())
        print (output)

    def help_getalljobs(self):
        print("List all the jobs registered with this system schedular.")

    def do_getajob(self,inp):
        if (not inp):
            print("Give a job id")
        else:
            val = self.schd.get_job(inp)
            print("Job:'{}'".format(val))
            output = {}
            output= ((job(val)).__getstate__())
            print (output)

    def help_getajob(self):
        print("Get the details of a registered job in this system schedular.")


    def do_reschedule(self, inp):
        if (not inp):
            print("Give a job id")
        else:
            self.schd.reschedule_job(inp)
            print("Job '{}' rescheduled...".format(inp))
 
    def help_reschedule(self):
        print("Reschedule a job with a Job id. Note: Job will be executed immidiately")
 
    def do_printjobs(self,inp):
        print("Jobs:")
        self.schd.print_jobs()

    def help_printjobs(self):
        print("Pretty print all the jobs registered with this system schedular.")

    def do_exit(self, inp):
        print("Bye")
        return True
    
    def help_exit(self):
        print('exit the console and quit the schedular. Shorthand: x q Ctrl-D.')
 
    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
 
        print("Default: {}".format(inp))
 
    do_EOF = do_exit
    help_EOF = help_exit
 

    

class SchedulerMain():
    

    SysJobstores_ = {
        'mongo': MongoDBJobStore(database= ((MongoDataStore.getInstance()).getDBConfigReader()).getDB(),
        collection='system_jobs',
        host= ((MongoDataStore.getInstance()).getDBConfigReader()).getHost(),
        user= ((MongoDataStore.getInstance()).getDBConfigReader()).getUser(),
        password= ((MongoDataStore.getInstance()).getDBConfigReader()).getPassword(),
        ),
        'default': MemoryJobStore(alias='system_jobs')
    }

    SysExecutors_ = {
        'default': {'type': 'threadpool', 'max_workers': 24},
        'processpool': ProcessPoolExecutor(max_workers=9)
    }

    SysJobDefaults_ = {
        'coalesce': False,
        'max_instances': 1,
        'misfire_grace_time': 300
    }


    def __init__(self):
        
        #prepare the ini details
        self.jobconfig = JobConfigFactory.getInstance()
        
        #setting up logger
        logging.basicConfig(filename=ConfigConstants.LOGGER_FILE, filemode='w',
        level=logging.INFO, format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
        self.sched_logger = logging.getLogger("debcredit")

        #setting up schedular
        self.scheduler = BackgroundScheduler(daemon=True)
        self.scheduler.configure(jobstores=SysJobstores_,
        executors=SysExecutors_,
        job_defaults=SysJobDefaults_,
        logger=self.sched_logger,
        timezone=self.jobconfig.createTimeZone())
        self.sched_logger.info("Background Schedular initiated...")
        # Setting up a sysprompt
        self.prompt = SysPrompt(self.scheduler)
        self.sched_logger.info("SysPrompt initiated...")
        self.jobconfig.setSchedular(self.scheduler)
        RuntimeContext.getInstance().setSchd(self.scheduler)
        RuntimeContext.getInstance().setLogger(self.sched_logger)
        self.sched_logger.info("init done...")

    def addSystemJobs (self):

        #0 enablePamentInstanceJob
        self.sched_logger.info("enablePamentInstanceJob registration initiated...")
        self.scheduler.add_job(Jobs.enablePamentInstanceJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_ENABLE_PAYMENT_INSTANCE_TAG),executor='processpool')
        self.sched_logger.info("enablePamentInstanceJob registration done...")
                
        #1 validateInstrumentsJob
        self.sched_logger.info("validateInstrumentsJob registration initiated...")
        self.scheduler.add_job(Jobs.validateInstrumentsJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_VALIDATE_INSTRUMENT_TAG),executor='processpool')
        self.sched_logger.info("validateInstrumentsJob registration done...")
        
        #2 createTaskInstanceJob
        self.sched_logger.info("createTaskInstanceJob registration initiated...")
        self.scheduler.add_job(Jobs.createTaskInstanceJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_CREATE_TASK_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_CREATE_TASK_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_CREATE_TASK_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_CREATE_TASK_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_CREATE_TASK_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_CREATE_TASK_TAG),executor='processpool')
        self.sched_logger.info("createTaskInstanceJob registration done...")
        
        
        #3 executePaymentJob
        self.sched_logger.info("executePaymentJob registration initiated...")
        self.scheduler.add_job(Jobs.executePaymentJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_EXECUTE_PAYMENT_TAG),executor='processpool')
        self.sched_logger.info("executePaymentJob registration done...")
        
        
        #4 capturePaymentJob
        self.sched_logger.info("capturePaymentJob registration initiated...")
        self.scheduler.add_job(Jobs.capturePaymentJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_CAPTURE_PAYMENTS_TAG),executor='processpool')
        self.sched_logger.info("capturePaymentJob registration done...")
        
        
        #5 collectBizMetricsJob
        self.sched_logger.info("collectBizMetricsJob registration initiated...")
        self.scheduler.add_job(Jobs.collectBizMetricsJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_COLLECT_BIZ_METRICS_TAG),executor='processpool')
        self.sched_logger.info("collectBizMetricsJob registration done...")
        
        
        #6 accountingPaymentJob
        self.sched_logger.info("accountingPaymentJob registration initiated...")
        self.scheduler.add_job(Jobs.accountingPaymentJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_ACCOUNTING_PAYMENTS_TAG),executor='processpool')
        self.sched_logger.info("accountingPaymentJob registration done...")
        
        
        #7 generateReportJob
        self.sched_logger.info("generateReportJob registration initiated...")
        self.scheduler.add_job(Jobs.generateReportJob,
        args=self.jobconfig.createArgs(IniFileTags.BATCH_GENERATE_REPORT_TAG),
        trigger=self.jobconfig.createTrigger(IniFileTags.BATCH_GENERATE_REPORT_TAG),
        id=self.jobconfig.createId(IniFileTags.BATCH_GENERATE_REPORT_TAG),
        name=self.jobconfig.createName(IniFileTags.BATCH_GENERATE_REPORT_TAG),
        coalesce=self.jobconfig.createCoalesce(IniFileTags.BATCH_GENERATE_REPORT_TAG),
        max_instances=self.jobconfig.createMaxInstance(IniFileTags.BATCH_GENERATE_REPORT_TAG),executor='processpool')
        self.sched_logger.info("generateReportJob registration done...")
        
        # add all the system jobs properties to Runtime context.
        systemjoblist = self.schd.get_jobs()
        for no in range(len(systemjoblist)):
            RuntimeContext.getInstance().appendSystemJobProperties((job(systemjoblist[no])).__getstate__())
        self.sched_logger.info("Adding of job properties to runtime context done...")

    
    def addSystemListener (self):
        self.sched_logger.info("System event listener registration initiated...")
        self.scheduler.add_listener(Listener.listenAndDispatchEvent, EVENT_ALL)
        self.sched_logger.info("System event listener registration done...")


    
    def run(self):
        self.sched_logger.info("Background Schedular about to start...")
        self.scheduler.start()
        self.sched_logger.info("Background Schedular started...")
        self.sched_logger.info("Launching command shell to interact schedular...")
        self.prompt.cmdloop()


    def __del__(self):
        atexit.register(lambda: self.scheduler.shutdown())
    


if __name__ == '__main__':
    mainCtrl = SchedulerMain()
    mainCtrl.addSystemJobs()
    mainCtrl.addSystemListener()
    mainCtrl.run()
    print("End..")
    
