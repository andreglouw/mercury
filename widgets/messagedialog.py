'''
Created on 11 Aug 2012

@author: alouw
'''
from PySide import QtCore, QtGui
import logging
from ui_messagedialog import Ui_MessageDialogClass

class MessageDialog(QtGui.QDialog, Ui_MessageDialogClass):
    def __init__(self, parent, message, hasCancel=False):
        super(MessageDialog, self).__init__(parent)
        self.setupUi(self)
        if hasCancel:
            self.cancelButton.setVisible(True)
        else:
            self.cancelButton.setVisible(False)
        self.text.setText(message)

    def done(self):
        QtGui.QDialog.done(1)

    def cancel(self):
        QtGui.QDialog.done(0)
