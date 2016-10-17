'''
Created on Jan 11, 2010

@author: eric
'''

from Events.Event import Event
from Events.Listener import Listener

class Notifier(object):
    '''
    Event Dispatcher goodness
    '''
    listeners = []

    def __init__(self, Pyibber):
        '''
        Constructor
        '''
        self.Pyibber = Pyibber
        
    def addListener(self, Listener):
        """Make sure Listener is an instance of Events.Listener.Listener
        """
        self.listeners.append(Listener)
        
    def notify(self, Event):
        for Listener in self.listeners:
            Listener.handleEvent(Event)
