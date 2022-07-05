'''
Created on 16 Aug 2012

@author: alouw
'''
from PySide import QtCore
import logging

class Command(QtCore.QObject):
    def __init__(self, **kwargs):
        super(Command, self).__init__()
        self.offset = 0
    
class Device(QtCore.QThread):
    devicePowerON = QtCore.Signal()
    devicePowerOFF = QtCore.Signal()
    deviceGPSReady = QtCore.Signal()
    deviceCOMMSReady = QtCore.Signal()
    deviceHandlerReady = QtCore.Signal()
    deviceHandlerStarted = QtCore.Signal()
    deviceHandlerStopped = QtCore.Signal()
    # Arguments: Status message 
    deviceStatusChanged = QtCore.Signal(object)
    # Arguments: MTMessage POPO
    newIncomingMessage = QtCore.Signal(object)
    # Arguments: Asset identifier, GPS location 
    newPositionMessage = QtCore.Signal(object, object)
    # Arguments: ICAO, Weather detail 
    newWeatherReport = QtCore.Signal(object, object)
    
    __message_header = "MSG "
    __interpreters = {
                      'DATE':None,
                      'GPSL':None,
                      'HUPD':None,
                      'ALRM':None,
                      'INIT':None,
                      'MOMS':None,
                      'MTMS':None
                      }
    
    def __init__(self, medium):
        super(Device, self).__init__()
        self.medium = medium
        self.abort = False
        self.commands = []
        self.current = None
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.incoming = ""
        # Connections
        self.medium.incomingData.connect(self.handleIncoming)
        
    def enqueueCommand(self, command):
        self.mutex.lock()
        try:
            self.commands.append(command)
        finally:
            self.mutex.unlock()
        self.condition.wakeAll()
        return command
    
    def prequeueCommand(self, command):
        self.mutex.lock()
        try:
            self.commands.insert(0, command)
        finally:
            self.mutex.unlock()
        self.condition.wakeAll()
        return command
        
    def dequeueIncoming(self, offset=0):
        data = ""
        self.mutex.lock()
        try:
            if offset <= 0:
                data = self.incoming
                self.incoming = ""
            else:
                data = self.incoming[offset:]
                self.incoming = self.incoming[0:offset]
        finally:
            self.mutex.unlock()
        return data

    def handleIncoming(self, data):
        self.mutex.lock()
        try:
            self.incoming.append(data)
        finally:
            self.mutex.unlock()
        self.condition.wakeAll()

    def resubmitIncoming(self, data, offset, adjustOffset=False):
        self.mutex.lock()
        try:
            if offset < 0:
                offset = 0
            self.incoming = self.incoming[0:offset]+data+self.incoming[offset:]
            if adjustOffset and self.current != None and self.current.offset > offset:
                logging.debug("Current command %s offset %d adjusted by %s bytes being resubmitted" % (self.current, self.current.offset, len(data)))
                self.current.offset += len(data)
            logging.debug("Data resubmitted for processing, left with %d unprocessed bytes" % len(self.incoming))
        finally:
            self.mutex.unlock()
        self.condition.wakeAll()
                                
    def sendMessage(self, message):
        pass
    
    def sendACK(self, message):
        pass
    
    def getGPS(self, immediate=False):
        pass
    
    def panic(self, activate=True):
        pass
    
    def highupdate(self, activate=True):
        pass
    
    def incomingMessages(self, data):
        offset = data.find(self.__class__.__message_header)
        msgPart = data[offset:]
        length = -1
        if len(msgPart) > len(self.__class__.__message_header)+1:
            logging.debug("Incoming message, looking for CR/LF")
            eol = msgPart.find("\r\n")
            if eol == -1:
                logging.debug("No CR/LF found in message data, wait for missing data")
                return None
            msgData = msgPart[eol+2:]
            length = int(msgPart[0:eol][len(self.__class__.__message_header):].strip())
            if len(msgData) >= length:
                command = self.__class__.__interpreters["MTMS"](msgData[0:length])
                logging.debug("Handling incoming data with length %d" % length)
                overflow = msgData[length:]
                # Message text is ended by CRC+CRLF -> look for CRLF and use rest as overflow
                eol = overflow.find("\r\n")
                if eol != -1:
                    overflow = overflow[eol+2:]
                    logging.debug("Skipping %d whitespace/CRC chars at end of incoming data" % (eol+2))
                if offset > 0:
                    overflow = data[0:offset]+overflow
                logging.debug("Combined under/overflow to push '%s' back onto queue" % overflow)
                self.resubmitIncoming(overflow, offset, True)
                command.offset = offset
                return command
        logging.debug("Incomplete message data, will wait for missing data")
        return None
        
    def run(self):
        self.deviceHandlerStarted.emit()
        while True:
            if self.abort:
                break
            try:
                data = ""
                if self.current == None:
                    data = self.dequeueIncoming()
                else:
                    data = self.dequeueIncoming(self.current.offset)
                if len(data) > 0:
                    if data.find(self.__class__.__message_header) >= 0:
                        command = self.incomingMessages(data)
                        if command == None:
                            offset = 0
                            if self.current != None:
                                offset = self.current.offset
                            self.resubmitIncoming(data, offset)
                        else:
                            self.prequeueCommand(command)
            except Exception, exc:
                logging.exception("Exception in Device run, ignoring...")
            self.mutex.lock()
            self.condition.wait(self.mutex, 100)
            self.mutex.unlock()
        self.deviceHandlerStopped.emit()
        logging.debug("Device Thread exiting")
        self.condition.wakeAll()

    def shutdown(self):
        logging.debug("Device shutdown request")
        self.mutex.lock()
        self.abort = True
        self.mutex.unlock()
        self.condition.wakeAll()
                