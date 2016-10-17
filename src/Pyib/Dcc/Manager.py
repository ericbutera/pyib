'''
Created on Jan 23, 2010

@author: eric
'''

class Manager(object):
    '''
    manager class for handling multiple dcc chats
    '''
    chats = []

    def __init__(self, Pyibber):
        '''
        ctor!
        '''
        self.Pyibber = Pyibber
        
    def attach(self, Chat):
        self.Pyibber.logger.info("adding chat session with (%s)" % Chat.DccChat.nick)
        self.chats.append(Chat)

    def detach(self, Chat):
        try:
            print "trying to remove (%s) from dcc chats" % Chat
            self.chats.remove(Chat)
        except Exception:
            pass

    def getCount(self):
        return len(self.chats)
