'''
Created on 11 Aug 2012

@author: alouw
'''
from ctypes import *
mercurydao = windll.MercuryDAO

MAX_MESSAGE_BUFFER = 190

class msg_data(Structure):
    _fields_ = [("msg_length",c_uint),
                ("buffer",c_char_p)]
