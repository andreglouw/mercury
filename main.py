import sys
import os
import logging
from PySide import QtCore, QtSql, QtGui
from mercury.preferences.globalsettings import GlobalSettings
from mercury.views.mercurview import Mercury

class QTracApplication(QtGui.QApplication):
    def __init__(self, args):
        super(QTracApplication, self).__init__(args)
        dbname = settings["DB_PATH"] #@UndefinedVariable
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(dbname)
        if not db.open():
            logging.error("Unable to open Database from file %s" % dbname)
        else:
            logging.info("Opened Database from file %s" % dbname)
        self.setQuitOnLastWindowClosed(False)
        self.setOrganizationName("Data Scout")
        self.setOrganizationDomain("datascout.co.za")
        self.setApplicationName("mercury")
        self.setApplicationVersion(str(settings["MAJOR_VERSION"])) #@UndefinedVariable

    def forceQuit(self):
        logging.error("Forcing Application to quit")
        self.quit()
                    
def run():
    # Create the Qt Application
    app = QTracApplication(sys.argv)

    f = QtCore.QFile("%s/mercury.css" % appDir)  #@UndefinedVariable
    if f.exists() and f.open(QtCore.QIODevice.ReadOnly):
        app.setStyleSheet(str(f.readAll()));
        f.close();
    else:
        logging.error("Could not open stylesheet")
    window = Mercury()
    if settings["TOUCHSCREEN"] == True: #@UndefinedVariable
        app.setOverrideCursor(QtCore.Qt.BlankCursor)
    window.move(0, 0)
    window.showMaximized()
    # Run the main Qt loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    run()