'''
Created on Jan 23, 2010

@author: eric
'''
import asyncore
import socket

class Chat(asyncore.dispatcher):
    """
    This implements the ability to handle a dcc chat with a user
    """
    
    buffer = ""

    def __init__(self, Pyibber, DccChat):
        '''
        Constructor
        '''
        asyncore.dispatcher.__init__(self)
        
        self.Pyibber = Pyibber
        self.DccChat = DccChat

        print "its ponytime: %s:%d" % (self.DccChat.ip, self.DccChat.port)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.DccChat.ip, self.DccChat.port))
    
    def write(self, message):
        self.Pyibber.logger.debug("dcc.socket.send: [%s]" % message)
        self.buffer = self.buffer + message + "\r\n"
        
    def handle_connect(self):
        print "dcc handle_connect called"
        pass

    def handle_close(self):
        print "dcc handle_close called"
        self.close()
        self.Pyibber.DccManager.detach(self)

    def handle_read(self):
        data = self.recv(8192)
        self.Pyibber.logger.debug('dcc.socket.recv: [%s]' % data)
        
        lines = data.strip().splitlines()
        for line in lines:
            #message = ParsedMessage(line)
            #self.Pyibber.Commandx.createFromMessage(message)
            print "dcc message: (%s)" % line
            self.write("you sent me: (%s)" % line)

    def writable(self): 
        return (len(self.buffer) > 0)

    def handle_write(self): 
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
