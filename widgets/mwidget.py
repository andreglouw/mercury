'''
Created on 11 Aug 2012

@author: alouw
'''
from PySide import QtCore, QtGui

class MWidget(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(MWidget, self).__init__(parent)
        self.permanentWidget = False
        self.isValid = False
