from PySide import QtCore
from optparse import OptionParser 
import sys
import os.path
import logging
import socket
from mercury.preferences.globalsettings import *

socket.setdefaulttimeout(60.0)

parser = OptionParser()
parser.add_option(
    "-i","--ini",dest="iniFile",default=None,
    help='The path to the ini configuration file to be loaded')
parser.add_option(
    "-s","--state",dest="stateFile",default=None,
    help='The path to the state setting file to be loaded')
(options, args) = parser.parse_args()

encoding = sys.getfilesystemencoding()
if hasattr(sys, "frozen"):
    _appDir_ = os.path.dirname(unicode(sys.executable, encoding))
else:
    _appDir_ = os.path.dirname(unicode(__file__, encoding))
iniFile = options.iniFile
if iniFile == None:
    iniFile = "%s/mercury.ini" % _appDir_
    
print "Use '%s' as ini file" % iniFile
_settings_ = GlobalSettings(_appDir_, iniFile, QtCore.QSettings.IniFormat)

stateFile = options.stateFile
if stateFile == None:
    stateFile = "%s/state.ini" % _appDir_
if not os.path.exists(stateFile):
    print "State settings file does not exist, creating"
    open(stateFile, "w").close()
    
print "Use '%s' as state setting file" % stateFile
_state_ = ApplicationSettings(_appDir_, stateFile, QtCore.QSettings.IniFormat)

logName = _settings_.value('Logging/LOG_FILE', 'stderr')
print "Will log to '%s'" % logName
if logName == "stdout":
    stream = sys.stdout
elif logName == "stderr":
    stream = sys.stderr
else:
    stream = open(logName,'a')
hdlr = logging.StreamHandler(stream)
fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(fmt)
logging.root.addHandler(hdlr)
level = _settings_.value("Logging/LOG_LEVEL","INFO") 
print "Set logging level to '%s'" % level
logging.root.setLevel(getattr(logging,level))
__builtins__['settings'] = _settings_
__builtins__['state'] = _state_
__builtins__['appDir'] = _appDir_
