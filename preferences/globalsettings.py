'''
Created on 11 Aug 2012

@author: alouw
'''
from PySide import QtCore
from UserDict import DictMixin
import sys
import logging

class GlobalSettings(QtCore.QSettings):

    __appserver__ = None

    def Instance(cls):
        if cls.__appserver__ == None:
            cls.__appserver__ = cls()
        return cls.__appserver__
    Instance = classmethod(Instance)

    def __init__(self, appDir, iniFile, format):
        super(GlobalSettings, self).__init__(iniFile, format)
        self.appDir = appDir
        self.__class__.__appserver__ = self
    
    def value(self, key, deflt=None):
        value = QtCore.QSettings.value(self, key, deflt)
        if "$(AppDir)" in value:
            return value.replace("$(AppDir)",self.appDir)
        return value
    
    def setValue(self, key, value):
        QtCore.QSettings.setValue(self, key, value)
        
    def __contains__(self, key):
        return QtCore.QSettings.contains(self, key)
    
    def __setitem__(self, name, value):
        self.setValue(name, value)
        
    def __getitem__(self, name):
        return self.value(name)

    def keys(self):
        return self.allKeys()

    def setLogLevel(self, logLevel):
        logging.root.setLevel(getattr(logging,logLevel))

class ApplicationSettings(GlobalSettings):

    def __init__(self, appDir, iniFile, format):
        super(ApplicationSettings, self).__init__(appDir, iniFile, format)
