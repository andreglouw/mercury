# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/messagedialog.ui'
#
# Created: Tue Aug 14 21:33:51 2012
#      by: pyside-uic 0.2.13 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MessageDialogClass(object):
    def setupUi(self, MessageDialogClass):
        MessageDialogClass.setObjectName("MessageDialogClass")
        MessageDialogClass.resize(400, 210)
        self.text = QtGui.QLabel(MessageDialogClass)
        self.text.setGeometry(QtCore.QRect(0, 6, 399, 107))
        self.text.setText("")
        self.text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.doneButton = QtGui.QPushButton(MessageDialogClass)
        self.doneButton.setGeometry(QtCore.QRect(308, 122, 91, 85))
        self.doneButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Mercury/resources/OK_100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.doneButton.setIcon(icon)
        self.doneButton.setIconSize(QtCore.QSize(100, 100))
        self.doneButton.setObjectName("doneButton")
        self.cancelButton = QtGui.QPushButton(MessageDialogClass)
        self.cancelButton.setGeometry(QtCore.QRect(2, 122, 91, 85))
        self.cancelButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Mercury/resources/Cancel_100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon1)
        self.cancelButton.setIconSize(QtCore.QSize(100, 100))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(MessageDialogClass)
        QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), MessageDialogClass.done)
        QtCore.QObject.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), MessageDialogClass.cancel)
        QtCore.QMetaObject.connectSlotsByName(MessageDialogClass)

    def retranslateUi(self, MessageDialogClass):
        MessageDialogClass.setWindowTitle(QtGui.QApplication.translate("MessageDialogClass", "MessageDialog", None, QtGui.QApplication.UnicodeUTF8))
        MessageDialogClass.setStyleSheet(QtGui.QApplication.translate("MessageDialogClass", "font: 18pt \"Verdana\";", None, QtGui.QApplication.UnicodeUTF8))

import mercury_rc
