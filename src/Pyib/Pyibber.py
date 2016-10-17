'''
Created on Jan 9, 2010

async code stolen from http://mail.python.org/pipermail/tutor/2003-July/024006.html

@author: eric
'''

import sys
import ConfigParser
import asyncore
import time

from Connection import Connection
from Commandx import Commandx
#from ParsedMessage import ParsedMessage
from Notifier import Notifier
import Dcc.Manager

class Pyibber(object):
    '''
    Use this to create your bot
    '''
    isRegistered = False
    keep_going = True

    def __init__(self, configPath, logger):
        '''
        Pyibber ctor
        '''
        self.loadConfig(configPath)
        self.logger = logger
        self.Commandx = Commandx(self)
        self.Notifier = Notifier(self)
        self.DccManager = Dcc.Manager.Manager(self)
        self.event_loop = EventLoop()
        
    def loadConfig(self, configPath):
        self.config = ConfigParser.ConfigParser()
        self.config.read(configPath)
        
    def run(self):
        self.logger.debug('Starting Pyibber.run() loop')
        self.Connection = Connection(self)
        self.logger.debug("entering async loop")
        
        self.event_loop.schedule(1, self.check_status)
        self.event_loop.schedule(1, self.displayStatus)
        self.event_loop.go(0.5)
        
        #asyncore.loop()
        self.logger.debug("async loop finished, no more connections.")
        time.sleep(10)
        self.logger.debug("relaunching")
        self.run()
        
    def displayStatus(self,el,time):
        self.logger.info("Bytes[in(%d) out(%d)] DccCount(%d)" % (
        self.Connection.bytesIn,
        self.Connection.bytesOut,
        self.DccManager.getCount()
        ))
        self.event_loop.schedule((60*60*2), self.displayStatus)
        
    def stop(self):
        self.logger.info("Shutting down")
        sys.exit(1)
        
    def check_status(self,el,time):
        if not self.keep_going:
            self.stop()
        else:
            self.event_loop.schedule(1,self.check_status)


class EventLoop:
    socket_map = asyncore.socket_map
    def __init__ (self):
        self.events = {}

    def go (self, timeout=5.0):
        events = self.events
        while self.socket_map:
            # print 'inner-loop'
            now = int(time.time())
            for k,v in events.items():
                if now >= k:
                    v (self, now)
                    del events[k]
            asyncore.poll (timeout)

    def schedule (self, delta, callback):
        now = int (time.time())
        self.events[now + delta] = callback

    def unschedule (self, callback, all=1):
        "unschedule a callback"
        for k,v in self.events:
            if v is callback:
                del self.events[k]
                if not all:
                    break
