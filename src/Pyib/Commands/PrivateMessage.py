'''
Created on Jan 10, 2010

@author: eric
'''

class PrivateMessage(object):
    '''
    private message parsing class
    '''
    
    to      = ""
    privmsg = ""
    origin  = None
    isAction= False
    
    MSG     = 'msg'
    CHANNEL = 'channel'
    CTCP    = 'ctcp'

    def __init__(self):
        '''
        Constructor
        '''
        
    def createFromParsedMessage(self, ParsedMessage):
        self.ParsedMessage = ParsedMessage
        message = ParsedMessage.message
        
        toEndOffset = message.find(" ", 8)
        self.to = message[8:toEndOffset]
        
        # PRIVMSG + 1space + recipient + (1space + 1colon)
        messageOffset = toEndOffset + 1 + 1
        self.privmsg = message[messageOffset:len(message)]
        
        actionChar = chr(1)
        
        if (actionChar+"ACTION" == self.privmsg[0:7]):
            self.isAction = True
            
        if ("#" == self.to[0:1]):
            self.origin = self.CHANNEL
        elif (True != self.isAction and actionChar == self.privmsg[0:1]):
            self.origin = self.CTCP
            self.privmsg = self.privmsg[1:(len(self.privmsg)-1)]
        else:
            self.origin = self.MSG
            
        if (True == self.isAction):
            self.privmsg = self.privmsg[8:(len(self.privmsg)-1)]

    def isAction(self):
        return self.isAction
    
    def getParsedMessage(self):
        return self.ParsedMessage
    
    def execute(self):
        return "PRIVMSG %s :%s" % (self.to, self.privmsg)
