'''
Created on 16 Aug 2012

@author: alouw
'''
from PySide import QtCore
import serial
import logging

class COMPort(QtCore.QThread):
    outgoingData = QtCore.Signal(object)
    incomingData = QtCore.Signal(object)
    commsMediumStarted  = QtCore.Signal()
    commsMediumStopped  = QtCore.Signal()
    
    ports = {"COM1:":0, "COM2:":1, "COM3:":2, "COM4:":3, "COM5:":4, "COM6:":5, "COM7:":6, "COM8:":7, "COM9:":8, "COM10:":9}
    
    def __init__(self, portname, baudrate):
        super(COMPort, self).__init__()
        self.portname = portname
        self.portnumber = COMPort.ports[portname]
        self.baudrate = int(baudrate)
        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.outgoing = []
        self.port = None
        self.abort = False
        logging.debug("COMPort opening on port %s (%d) @ %s" % (self.portname,self.portnumber,self.baudrate))
        
    def openPort(self):
        self.port = serial.Serial(self.portnumber,self.baudrate,timeout=1)
        return self.port.isOpen()
    
    def closePort(self):
        self.mutex.lock()
        try:
            if self.port != None and self.port.isOpen():
                self.port.close()
                logging.debug("COMPort port %s closed" % self.portname)
                self.port = None
        finally:
            self.mutex.unlock()
    
    def enqueueData(self, buffer):
        self.mutex.lock()
        try:
            self.outgoing.append(buffer)
        finally:
            self.mutex.unlock()
            self.condition.wakeAll()
            
    def write(self, buffer):
        self.port.write(buffer)
        self.outgoingData.emit(buffer)
        
    def read(self):
        buffer = self.port.readall()
        if len(buffer) > 0:
            if buffer.startswith("DBG") or buffer.startswith("SBD"):
                logging.debug(buffer)
            else:
                return buffer
        return ""
    
    def run(self):
        if self.port != None and self.port.isOpen():
            logging.debug("COMPort port is open, closing first...")
            self.closePort()
        if not self.openPort():
            raise "Unable to open COMPort port %s" % self.portname
        self.commsMediumStarted.emit()
        while True:
            if self.abort:
                break
            incoming = self.read()
            if len(incoming) > 0:
                self.incomingData.emit(incoming)
            if len(self.outgoing) > 0:
                self.mutex.lock()
                try:
                    self.write(self.outgoing.pop(0))
                finally:
                    self.mutex.unlock()
            self.mutex.lock()
            self.condition.wait(self.mutex,100)
            self.mutex.unlock()
        self.closePort()
        self.condition.wakeAll()
        self.commsMediumStopped.emit()
        
    def shutdown(self):
        logging.debug("COMPort shutdown request")
        self.mutex.lock()
        self.abort = True
        self.mutex.unlock()
        self.condition.wakeAll()
        