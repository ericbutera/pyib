'''
Created on Jan 11, 2010

@author: eric
'''

import os
import random
from Pyib.Events.Listener import Listener

class ChuckNorris(Listener):
    
    lineCount = 0
    
    def __init__(self, Pyibber):
        Listener.__init__(self, Pyibber)
        self.Pyibber = Pyibber
        f = self.getFileHandle()
        for line in f.readlines():
            self.lineCount = self.lineCount + 1

    def handleEvent(self, Event):
        if (".chuck" != Event.PrivateMessage.privmsg[0:6]):
            return
        
        num = random.randint(1, self.lineCount)
        x = 1
        for line in self.getFileHandle().readlines():
            if (x == num):
                self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, line)
            x = x + 1

    def getFileHandle(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        return open(dir + os.sep +"chuck.txt", 'r') 
