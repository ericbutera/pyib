'''
Created on Jan 9, 2010

@author: eric
'''
from Netmask import Netmask

class ParsedMessage(object):
    '''
    parses a raw message from the server into something more friendly
    '''
    source      = ''
    message     = ''
    rawMessage  = ''

    def __init__(self, rawMessage):
        '''
        Constructor
        '''
        self.rawMessage = rawMessage
        
        if ":" == rawMessage[0:1]:
            offset = rawMessage.find(" ")
            self.source  = rawMessage[1:offset]
            self.message = rawMessage[offset+1:]
        else:
            self.source  = 'local-server'
            self.message = rawMessage
            
        self.Netmask = Netmask(self.source)
