'''
Created on 11 Aug 2012

@author: alouw
'''
from PySide import QtCore, QtGui
from mercury.preferences.globalsettings import GlobalSettings
import logging
import win32api
from mercury.widgets.mwidget import MWidget 
from mercury.widgets.messagedialog import MessageDialog 
from ui_mercury import Ui_MercuryClass

class Mercury(MWidget, Ui_MercuryClass):

    __appserver__ = None

    def Instance(cls):
        if cls.__appserver__ == None:
            cls.__appserver__ = Mercury()
        return cls.__appserver__
    Instance = classmethod(Instance)

    def __init__(self,parent=None):
        super(Mercury, self).__init__(parent)
        self.__class__.__appserver__ = self
        self.permanentWidget = True
        self.stackIndex = 0
        self.showingNeonInbox = False
        self.starter = None
        self.flasher = None
        self.keyboard = None
        self.commslib = None
        self.availableStack = []
        self.breadCrumbStack = []
        self._shutdownMutex = QtCore.QMutex()
        self._shutdownWait = QtCore.QWaitCondition()
        if settings["RUN_DEBUG"] == False: #@UndefinedVariable
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(QtCore.Qt.Window)
        self.setupUi(self)

    def showEvent(self, event):
        if self.isValid:
            pass
        else:
            pass

    def pinChanged(self, text):
        if not self.starter is None and self.starter.isActive():
            self.starter.stop()
            self.starter = None
    
    def isLoggedIn(self):
        logging.debug("Logged in with pin %s, setup signal handlers" % (self.pin.text()))
        if not self.starter is None and self.starter.isActive():
            self.starter.stop()
            self.starter = None
        '''
        QObject::connect(commslib.data(),SIGNAL(commsHandlerPowerON()),this,SLOT(commsHandlerPowerON()));
        QObject::connect(commslib.data(),SIGNAL(commsHandlerPowerOFF()),this,SLOT(commsHandlerPowerOFF()));
        QObject::connect(commslib.data(),SIGNAL(commsHandlerInitialized()),this,SLOT(commsHandlerInitialized()));
        QObject::connect(commslib.data(),SIGNAL(commsHandlerCommsReady()),this,SLOT(commsHandlerCommsReady()));
        QObject::connect(commslib.data(),SIGNAL(commsHandlerGPSReady()),this,SLOT(commsHandlerGPSReady()));
        QObject::connect(commslib.data(),SIGNAL(commsHandlerDeviceReady()),this,SLOT(commsHandlerDeviceReady()));
        QObject::connect(commslib.data(),SIGNAL(systemIsReady()),this,SLOT(systemIsReady()));
        QObject::connect(commslib.data(),SIGNAL(changeStatusMessage(QString)),this,SLOT(showStatusMessage(QString)));
        QObject::connect(commslib.data(),SIGNAL(commandTimeoutError(QString)),this,SLOT(showTimeoutErrorMessage(QString)));
        QObject::connect(commslib.data(),SIGNAL(systemPowerOffRequested()),this,SLOT(confirmPowerOffRequest()));
        QObject::connect(commslib.data(),SIGNAL(newIncomingMessage()),this,SLOT(indicateIncomingMessage()));
        QObject::connect(commslib.data(),SIGNAL(incomingMessageWasOpened()),this,SLOT(incomingMessageAcknowledged()));
        '''
        self.stackedWidget.removeWidget(self.loginpage)
        self.keyboard = None
        self.availableStack.append(self)
        self.breadCrumbStack.append(self)
        self.showHomePage()
        logging.debug("Signal handlers setup, start Comms Handler")
        #commslib->startCommsHandler();

    def indicateIncomingMessage(self, stopFlashing=False):
        icon = QtGui.QIcon()
        if stopFlashing or self.showingNeonInbox:
            icon.addFile(":/Mercury/Resources/Inbox_100.png", QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.showingNeonInbox = False
        else:
            icon.addFile(":/Mercury/Resources/InboxNeon_100.png", QtCore.QSize(), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
            self.showingNeonInbox = True
        self.inboxButton.setIcon(icon)
        if not stopFlashing:
            self.flasher = QtCore.QTimer.singleShot(500, self, QtCore.SLOT("indicateIncomingMessage()"))

    def incomingMessageAcknowledged(self):
        if not self.flasher is None and self.flasher.isActive():
            self.flasher.stop()
            self.flasher = None
        self.indicateIncomingMessage(True)

    def confirmPowerOffRequest(self):
        quitter = QtCore.QTimer.singleShot(10000, self, QtCore.SLOT("shutdownSystem()"))
        msg = MessageDialog(self,"Shutting down in 10 seconds, click OK to continue working")
        msg._exec()
        if not msg.result() == 0:
            if quitter.isActive():
                quitter.stop()

    EWX_POWEROFF = 0x00000008
    EWX_FORCE = 0x00000004
    
    SHTDN_REASON_MAJOR_OPERATINGSYSTEM = 0x00020000
    SHTDN_REASON_MINOR_UPGRADE = 0x00000003
    SHTDN_REASON_FLAG_PLANNED = 0x80000000
    
    def shutdownSystem(self):
        logging.debug("Force OS Shutdown")
        if not win32api.ExitWindowsEx(Mercury.EWX_POWEROFF | Mercury.EWX_FORCE, Mercury.SHTDN_REASON_MAJOR_OPERATINGSYSTEM | Mercury.SHTDN_REASON_MINOR_UPGRADE | Mercury.SHTDN_REASON_FLAG_PLANNED):
            logging.debug("Failed to Shut Down the system.")
        if not self.commslib == None:
            QtCore.QObject.connect(self.commslib,QtCore.SIGNAL("systemIsStopped()"),self,QtCore.SLOT("systemIsStopped()"))
            self.commslib.shutdown()
        self._shutdownMutex.lock()
        self._shutdownWait.wait(self._shutdownMutex,2000)

    def showHomePage(self):
        self.stackIndex = 0;
        self.stackedWidget.setCurrentIndex(self.stackIndex)
        self.brightnessUp.setVisible(False);
        self.brightnessDown.setVisible(False);
        debugMode = settings["RUN_DEBUG"] #@UndefinedVariable
        if self.isSysAdminUser():
            debugMode = True
        if debugMode == True:
            self.quitButton.setVisible(True)
            self.composeTextButton.setEnabled(True)
            self.aviationWizardButton.setEnabled(True)
            self.panicButton.setEnabled(True)
            self.aviationWizardButton.setEnabled(True)
            self.missionButton.setEnabled(True)
            self.contactButton.setEnabled(True)
            self.medevacButton.setEnabled(True)
            self.reportLineButton.setEnabled(True)
            self.adminAsset.setEnabled(True)
            self.waypointButton.setEnabled(True)
            self.weatherButton.setEnabled(True)
            self.freeFormat.setEnabled(True)
            self.defaultContacts.setEnabled(True)
            self.quitButton.setVisible(True)
        else:
            self.quitButton.setVisible(False)
            self.composeTextButton.setEnabled(False)
            self.aviationWizardButton.setEnabled(False)
            self.panicButton.setEnabled(False)
            self.aviationWizardButton.setEnabled(False)
            self.missionButton.setEnabled(False)
            self.contactButton.setEnabled(False)
            self.medevacButton.setEnabled(False)
            self.reportLineButton.setEnabled(False)
            self.adminAsset.setEnabled(False)
            self.waypointButton.setEnabled(False)
            self.weatherButton.setEnabled(False)
            self.freeFormat.setEnabled(False)
            self.defaultContacts.setEnabled(False)
            self.quitButton.setVisible(False)
        self.adminButton.setEnabled(True)
        self.panicButton.setVisible(settings["ONSCREEN_ALARM"]) #@UndefinedVariable


    def getWidgetByIdentifier(self, seek):
        for widget in self.availableStack:
            if widget.objectName() == seek:
                return widget
        return None

    def isCurrentWidget(self, seek):
        if self.stackedWidget.currentWidget().objectName() == seek:
            return True;
        return False;

    def getStackedWidget(self, seek):
        for widget in self.availableStack:
            if widget.objectName() == seek.objectName():
                return widget;
        return None

    def pushToFront(self, gotoWidget, comebackHere=True):
        if not comebackHere and self.stackIndex > 0:
            # If we're not coming back here, remove the widget (unless it's a permanentWidget)
            popped = self.availableStack[self.stackIndex]
            if not popped.permanentWidget:
                logging.debug("Current Widget must be deleted...")
                del self.availableStack[self.stackIndex]
                self.stackedWidget.removeWidget(popped)
            if popped in self.breadCrumbStack:
                self.breadCrumbStack.remove(popped)
        if not gotoWidget == None:
            # Is the gotoWidget allready in the QStackedWidget
            idx = self.stackedWidget.indexOf(gotoWidget)
            if idx == -1:
                idx = self.stackedWidget.addWidget(gotoWidget)
            self.stackedWidget.setCurrentIndex(idx)
            # If the gotoWidget is not allready in the list of availables, push it
            if not gotoWidget in self.availableStack:
                self.availableStack.append(gotoWidget)
            self.stackIndex = self.availableStack.index(gotoWidget)
            self.breadCrumbStack.append(gotoWidget)
        else:
            self.stackIndex = 0
            self.stackedWidget.setCurrentIndex(0)

    def showHome(self):
        for popped in self.availableStack:
            if not popped.permanentWidget:
                logging.debug("Current Widget must be deleted...")
                self.availableStack.remove(popped)
                self.stackedWidget.removeWidget(popped)
            if popped in self.breadCrumbStack:
                self.breadCrumbStack.remove(popped)
        self.stackIndex = 0;
        self.stackedWidget.setCurrentIndex(self.stackIndex)

    def selectAdditPage(self):
        self.stackedWidget.setCurrentWidget(self.additionalPage)

    def selectHomePage(self):
        self.stackedWidget.setCurrentWidget(self.homePage)

    def showBack(self):
        backFrom = self.availableStack[self.stackIndex]
        if not backFrom.permanentWidget:
            logging.debug("Current Widget must be deleted...")
            del self.availableStack[self.stackIndex]
            self.stackedWidget.removeWidget(backFrom)
        if backFrom in self.breadCrumbStack:
            self.breadCrumbStack.remove(backFrom)
        if len(self.breadCrumbStack) > 0:
            backTo = self.breadCrumbStack[-1]
            idx = self.stackedWidget.indexOf(backTo)
            if idx == -1:
                self.stackIndex = 0;
                self.stackedWidget.setCurrentIndex(self.stackIndex)
            else:
                self.stackIndex = self.availableStack.index(backTo)
                self.stackedWidget.setCurrentWidget(backTo)
        else:
            self.showHome()
   
    def getInbox(self):
        widget = self.getWidgetByIdentifier("inbox")
        if widget == None:
            widget = Inbox()
            widget.setObjectName("inbox")
        return widget

    def getTextComposer(self):
        widget = self.getWidgetByIdentifier("composetext")
        if widget == None:
            widget = ComposeText()
            widget.setObjectName("composetext")
        return widget

    def getRecipientSelect(self, showDefaults=False):
        widget = self.getWidgetByIdentifier("recipientselect")
        if widget == None:
            widget = RecipientSelect(0, showDefaults)
            widget.setObjectName("recipientselect")
        return widget

    def showDefaultRecipients(self):
        widget = self.getWidgetByIdentifier("recipientselect")
        if widget == None:
            widget = RecipientSelect(0, True)
            widget.setObjectName("recipientselect")
        self.pushToFront(widget,True)

    def showInbox(self, comebackHere=True):
        self.pushToFront(self.getInbox(),comebackHere)

    def showOutbox(self, comebackHere=True):
        widget = self.getWidgetByIdentifier("outbox")
        if widget == None:
            widget = Outbox()
            widget.setObjectName("outbox")
        self.pushToFront(widget,comebackHere)
