'''
Created on 15 Aug 2012

@author: alouw
'''
from UserDict import DictMixin
import models
import constants

class POPO(DictMixin, object):
    
    def __init__(self, kwargs):
        super(POPO, self).__init__()
        self._values = kwargs

    def __setitem__(self, name, value):
        self._values[name] = value
        
    def __getitem__(self, name):
        return self._values.get(name)

    def keys(self):
        return self._values.keys()

class MTMessage(POPO):
    
    def __init__(self, kwargs):
        super(MTMessage, self).__init__(kwargs)
        self._recipients = None

    def recipients(self):
        if self._recipients == None:
            self._recipients = models.RecipientModel.recipientsForMessage(self["id"], constants.INCOMING)
        return self._recipients
            
class MOMessage(POPO):
    
    def __init__(self, kwargs):
        super(MOMessage, self).__init__(kwargs)
        self._recipients = None

    def recipients(self):
        if self._recipients == None:
            self._recipients = models.RecipientModel.recipientsForMessage(self["id"], constants.OUTGOING)
        return self._recipients
            