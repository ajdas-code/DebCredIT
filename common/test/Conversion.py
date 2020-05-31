from abc import ABC, abstractmethod
import datetime,time
import json, bson,pprint
import sys, traceback


class Conv(ABC):

    def conv(self,s):
        pass


class Convf(Conv):

    def conv(self,s):
        try:
            s = float(s)
        except ValueError:
            pass
        except TypeError:
            pass
        return s

class Convi(Conv):

    def conv(self,s):
        try:
            s = int(s)
        except ValueError:
            pass
        except TypeError:
            pass
        return s

class Convdate (Conv):

    def conv(self,s):
        try:
            s = datetime.datetime.strptime(s,"%m/%d/%Y")
        except ValueError:
            pass
        except TypeError:
            pass
        return s

class Convs(Conv):

    def conv(self,s):
        try:
            s = str(s).lower()
        except ValueError:
            pass
        except TypeError:
            pass
        return s
