import sys, time
from Daemon import Daemon
 
class MyDaemon(Daemon):
    def __init__(self,pidf):
        super(MyDaemon,self).__init__(pidf)
        
    def run(self):
        while True:
            print("....working..")
            time.sleep(3)
            
if __name__ == "__main__":
    daemon = MyDaemon('daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
