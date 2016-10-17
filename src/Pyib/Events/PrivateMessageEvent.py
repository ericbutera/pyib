'''
Created on Jan 11, 2010

@author: eric
'''
from Pyib.Commands import PrivateMessage
from Event import Event

class PrivateMessageEvent(Event):
    '''
    represents a private message event
    '''

    def __init__(self, PrivateMessage):
        '''
        ctor
        '''
        self.PrivateMessage = PrivateMessage
