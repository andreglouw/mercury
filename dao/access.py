'''
Created on 14 Aug 2012

@author: alouw
'''
from PySide import QtCore, QtSql
import os
import time
import logging

class DAO(QtCore.QObject):

    __appserver__ = None

    def Instance(cls):
        if cls.__appserver__ == None:
            cls.__appserver__ = DAO()
        return cls.__appserver__
    Instance = classmethod(Instance)
    
    def __init__(self):
        super(DAO, self).__init__()

    def records(cls, query=None, tablename=None, qualified=None):
        assert not (query == None and tablename == None)
        if query == None:
            if not qualified is None:
                query = QtSql.QSqlQuery("select * from %s where %s" % (tablename, qualified))
            else:
                query = QtSql.QSqlQuery("select * from %s" % (tablename))
        result = []
        if query.exec_():
            while query.next():
                sqlrecord = query.record()
                result.append(cls.dict(sqlrecord))
        else:
            logging.error("Error retrieving records from table %s" % tablename)
        return result
    records = classmethod(records)
    
    def dict(cls, sqlrecord):
        entry = {}
        for i in range(sqlrecord.count()):
            entry[sqlrecord.fieldName(i)] = sqlrecord.value(i)
        return entry
    dict = classmethod(dict)
        