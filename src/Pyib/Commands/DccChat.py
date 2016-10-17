'''
Created on Jan 23, 2010

@author: eric
'''

import iptools

class DccChat(object):
    '''
    parses a 'DCC CHAT CHAT 2130706433 46716' request
    '''
    
    longIp  = 0
    ip      = None
    port    = 0
    nick    = ""
    ident   = ""
    host    = ""

    def __init__(self):
        '''
        Constructor
        '''
        
    def createFromPrivateMessage(self, PrivateMessage):
        self.PrivateMessage = PrivateMessage
        privmsg = PrivateMessage.privmsg
        if ("DCC CHAT CHAT" != privmsg[0:13]):
            raise Exception("Invalid argument");
        
        # 2130706433 47372
        ipEnd = privmsg.find(" ", 14)
        self.longIp = int(privmsg[14:ipEnd])
        self.ip     = iptools.long2ip(self.longIp)
        self.port   = int(privmsg[ipEnd+1:])
        print "parsed longIp(%d) ip(%s) port(%d)" % (self.longIp, self.ip, self.port)
        
        self.nick   = PrivateMessage.ParsedMessage.Netmask.nick
        self.ident  = PrivateMessage.ParsedMessage.Netmask.ident
        self.host   = PrivateMessage.ParsedMessage.Netmask.host
        print "dcc chat nick(%s) ident(%s) host(%s)" % (self.nick, self.ident, self.host)
    
    def execute(self):
        return "DCC CHAT CHAT %d %d" % (self.longIp, self.port)
