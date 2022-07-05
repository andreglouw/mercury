'''
Created on 15 Aug 2012

@author: alouw
'''
from PySide import QtCore, QtGui, QtSql
from access import DAO
from popos import MTMessage, MOMessage
import constants

class MOMessageModel(QtSql.QSqlTableModel):

    MO_ID_COLUMN            = 0
    MO_TIMESTAMP_COLUMN     = 1
    MO_TEXT_COLUMN          = 2
    MO_RECIPIENT_COLUMN     = 3
    MO_SILENT_COLUMN        = 4
    MO_STATUS_COLUMN        = 5
    
    header_data = [
                   {'col':MO_ID_COLUMN,'align':QtCore.Qt.Horizontal,'title':'ID'},
                   {'col':MO_STATUS_COLUMN,'align':QtCore.Qt.Horizontal,'title':''},
                   {'col':MO_SILENT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Visible'},
                   {'col':MO_TIMESTAMP_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Sent'},
                   {'col':MO_RECIPIENT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Recipient'},
                   {'col':MO_TEXT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Message'},
                   ]
    
    def __init__(self):
        super(MOMessageModel, self).__init__()
        self.setTable("motextmessage")
        self.setFilter("silent = 'f'")
        for detail in MOMessageModel.header_data:
            self.setHeaderData(detail['col'],detail['align'],detail['title'])
        self.select()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            rec = self.record(index.row())
            value = rec.value(index.column())
            if index.column() == MOMessageModel.MO_STATUS_COLUMN:
                value = ""
            elif index.column() == MOMessageModel.MO_RECIPIENT_COLUMN:
                recs = RecipientModel.recipientsForMessage(rec.value("id"), constants.OUTGOING)
                text = ""
                first = True
                for recipient in recs:
                    if first:
                        text = recipient["description"]
                    else:
                        text = "%s;" % recipient["description"]
                if len(text) == 0:
                    text = "<Unknown>"
                value = text
            elif index.column() == MOMessageModel.MO_TIMESTAMP_COLUMN:
                value = rec.value("timestamp")
            return value
        elif role == QtCore.Qt.DecorationRole:
            rec = self.record(index.row())
            if index.column() == MOMessageModel.MO_STATUS_COLUMN:
                status = rec.value(index.column())
                icon = QtGui.QIcon()
                if status == constants.MO_WAITING:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailWaiting"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif status == constants.MO_BUSY:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailBusy"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif status == constants.MO_SENT:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailSent"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                elif status == constants.MO_ACKED:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailAcked"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailError"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                return icon
        return QtSql.QSqlTableModel.data(self, index, role)
    
    def message(self, row):
        sqlrecord = self.record(row)
        return MOMessage(DAO.dict(sqlrecord))
    
class MTMessageModel(QtSql.QSqlTableModel):

    MT_CONTAINERID_COLUMN   = 0
    MT_SEQINDEX_COLUMN      = 1
    MT_SEQCOUNT_COLUMN      = 2
    MT_ID_COLUMN            = 3
    MT_ITRACID_COLUMN       = 4
    MT_TIMESTAMP_COLUMN     = 5
    MT_TEXT_COLUMN          = 6
    MT_RECIPIENT_COLUMN     = 7
    MT_SILENT_COLUMN        = 8
    MT_STATUS_COLUMN        = 9
    
    header_data = [
                   {'col':MT_ID_COLUMN,'align':QtCore.Qt.Horizontal,'title':'ID'},
                   {'col':MT_ITRACID_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Ref'},
                   {'col':MT_STATUS_COLUMN,'align':QtCore.Qt.Horizontal,'title':''},
                   {'col':MT_SILENT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Visible'},
                   {'col':MT_TIMESTAMP_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Received'},
                   {'col':MT_RECIPIENT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Sender'},
                   {'col':MT_TEXT_COLUMN,'align':QtCore.Qt.Horizontal,'title':'Message'},
                   {'col':MT_SEQINDEX_COLUMN,'align':QtCore.Qt.Horizontal,'title':''},
                   {'col':MT_SEQCOUNT_COLUMN,'align':QtCore.Qt.Horizontal,'title':''},
                   {'col':MT_CONTAINERID_COLUMN,'align':QtCore.Qt.Horizontal,'title':''}
                   ]
    
    def __init__(self):
        super(MTMessageModel, self).__init__()
        self.setTable("mttextmessage")
        self.setFilter("silent = 'f'")
        for detail in MTMessageModel.header_data:
            self.setHeaderData(detail['col'],detail['align'],detail['title'])
        self.select()
        
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            rec = self.record(index.row())
            value = rec.value(index.column())
            if index.column() == MTMessageModel.MT_STATUS_COLUMN:
                value = ""
            elif index.column() == MTMessageModel.MT_RECIPIENT_COLUMN:
                recs = RecipientModel.recipientsForMessage(rec.value("id"), constants.INCOMING)
                text = ""
                first = True
                for recipient in recs:
                    if first:
                        text = recipient["description"]
                    else:
                        text = "%s;" % recipient["description"]
                if len(text) == 0:
                    text = "<Unknown>"
                value = text
            elif index.column() == MTMessageModel.MT_TIMESTAMP_COLUMN:
                value = rec.value("timestamp")
            return value
        elif role == QtCore.Qt.DecorationRole:
            rec = self.record(index.row())
            if index.column() == MTMessageModel.MT_STATUS_COLUMN:
                status = rec.value(index.column())
                icon = QtGui.QIcon()
                if status == constants.MT_UNREAD:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailWaiting"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                else:
                    icon.addPixmap(QtGui.QPixmap(":/Common/EmailOpened"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                return icon
        return QtSql.QSqlTableModel.data(self, index, role)
    
    def message(self, row):
        sqlrecord = self.record(row)
        return MTMessage(DAO.dict(sqlrecord))
    
    def createMessage(self, message, recipientIds):
        sqlrecord = self.record()
        for i in range(sqlrecord.count()):
            sqlrecord.setValue(sqlrecord.fieldName(i),object[sqlrecord.fieldName(i)])
        if self.insertRecord(-1, sqlrecord):
            # Link recipients
            return True
        return False

class RecipientModel(QtSql.QSqlTableModel):
    def __init__(self):
        super(RecipientModel, self).__init__()
        self.setTable("recipient")
        self.select()
        
    def orderByClause(self):
        return "ORDER by type,description"
    
    def data(self, index, role):
        return QtSql.QSqlTableModel.data(self, index, role)
    
    def recipientsForMessage(cls, messageId, messageType):
        query = QtSql.QSqlQuery("select * from recipient where id in (select recipient from msgrecip where message = ? and msgtype = ?)")
        query.addBindValue(messageId)
        query.addBindValue(messageType)
        return DAO.records(query)
    recipientsForMessage = classmethod(recipientsForMessage)
        
    def linkMessageRecipients(cls, msgId, msgType, recipientIds):
        if recipientIds == None or len(recipientIds) == 0:
            return True
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO msgrecip (message,recipient,msgtype) VALUES (?,?,?)")
        query.addBindValue([msgId]*len(recipientIds))
        query.addBindValue(recipientIds)
        query.addBindValue([msgType]*len(recipientIds))
        return query.execBatch()
    linkMessageRecipients = classmethod(linkMessageRecipients)
    
    def recipientWithITRACId(self, itracId):
        query = QtSql.QSqlQuery("SELECT * FROM recipient WHERE itracid = ?")
        query.addBindValue(itracId)
        if query.exec_() and query.next():
            return DAO.dict(query.record())
        return None
    recipientWithITRACId = classmethod(recipientWithITRACId)
        