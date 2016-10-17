'''
Created on Jan 9, 2010

@author: eric
'''

import asyncore
import socket
import time

from ParsedMessage import ParsedMessage

class Connection(asyncore.dispatcher):
    '''
    maintains the connection to the server
    '''
    buffer = ""
    bytesIn = 0
    bytesOut = 0
    
    connectionAttempts = 0
    reconnectWait = 3
    maxAttempts = 100

    def __init__(self, Pyibber):
        '''
        ctor, pass in the Pyibber instance
        '''
        asyncore.dispatcher.__init__(self)
        
        self.Pyibber = Pyibber
        self.omgPoniesConnect()
    
    """
    def omgPoniesConnect(self):
        print "omgPoniesConnect called"
        count = 0
        while (count < self.maxAttempts):
            config = self.Pyibber.config;
            server = str(config.get("pyib", "serverAddress"))
            port   = int(config.get("pyib", "serverPort"))
            
            self.Pyibber.logger.info('attempt %d connecting to: %s:%d' % (count, server, port))
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            x = self.connect((server, port))
            print "x: (%s)" % x
            count = count + 1
            time.sleep(self.reconnectWait)
            
        self.Pyibber.logger.error('Unable to connect to server after %d tries' % self.maxAttempts)
        self.Pyibber.stop()
    """
    
    def omgPoniesConnect(self):
        config = self.Pyibber.config;
        server = str(config.get("pyib", "serverAddress"))
        port   = int(config.get("pyib", "serverPort"))
        
        self.Pyibber.logger.info('attempt %d connecting to: %s:%d' % (self.connectionAttempts, server, port))
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((server, port))
    
    def write(self, message):
        self.Pyibber.logger.debug("socket.send: [%s]" % message)
        self.buffer = self.buffer + message + "\r\n"
        self.bytesOut += len(self.buffer)
        
    def handle_connect(self):
        pass

    def handle_close(self):
        self.Pyibber.logger.debug("connection.handle_close")
        self.close()
        
    def handle_error(self):
        self.Pyibber.logger.debug("connection.handle_error")
        self.close()

    def handle_read(self):
        data = self.recv(4096)
        self.Pyibber.logger.debug('socket.recv: [%s]' % data)
        self.bytesIn += len(data)

        lines = data.splitlines()
        for line in lines:
            message = ParsedMessage(line)
            self.Pyibber.Commandx.createFromMessage(message)

    def writable(self): 
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]
        
    """
    def arghconnect(self, server, port):
        count = 0
        while (count < self.maxAttempts):
            server = str(config.get("pyib", "serverAddress"))
            port   = int(config.get("pyib", "serverPort"))
            
            self.Pyibber.logger.info('attempt %d connecting to: %s:%d' % (count, server, port))
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((server, port))
                return
            except Exception, e:
                #self.socket.close()
                #self.socket = None
                self.Pyibber.logger.warning('socket fail: %s' % e)
                #time.sleep(self.reconnectWait)
                sys.exit(1)
            count = count + 1
            
        if self.socket is None:
            self.Pyibber.logger.error('unable to connect to server after %d tries' % self.maxAttempts)
            self.Pyibber.stop()
            return
    """
