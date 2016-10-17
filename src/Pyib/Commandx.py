'''
Created on Jan 10, 2010

@author: eric
'''

from Events.PrivateMessageEvent import PrivateMessageEvent

from Commands.PrivateMessage import PrivateMessage
from Commands.DccChat import DccChat
import Dcc.Chat 

class Commandx(object):
    '''
    command class for handling messages
    '''
    Pyibber = None
    nickAttempts = 0

    def __init__(self, Pyibber):
        '''
        Constructor
        '''
        self.Pyibber = Pyibber
        
    def createFromMessage(self, ParsedMessage):
        message = ParsedMessage.message
        
        if "PRIVMSG" == message[0:7]:
            self.handlePrivateMessage(ParsedMessage)
        
        if "PING" == message[0:4]:
            self.handlePong(ParsedMessage)
            
        if "004" == message[0:3]:
            self.handleConnect(ParsedMessage)
            self.handleJoinChannels(ParsedMessage)
            
        if "001" == message[0:3]:
            self.actualServerName = ParsedMessage.source
            
        if "NOTICE " == message[0:7] and False == self.Pyibber.isRegistered:
            self.handleRegister(ParsedMessage)
            
        if "433" == message[0:3]:
            self.handleNickInUse(ParsedMessage)
            
        if "ERROR" == message[0:5]:
            self.handleDisconnect(ParsedMessage)

    def handlePrivateMessage(self, ParsedMessage):
        privmsg = PrivateMessage()
        privmsg.createFromParsedMessage(ParsedMessage)
        
        self.handleDcc(privmsg)
        self.handleCtcp(privmsg)
        self.handleChannelMessage(privmsg)
        
    def handlePong(self, ParsedMessage):
        self.Pyibber.Connection.write("PONG :"+ self.actualServerName)
        
    def setNick(self, nick):
        self.Pyibber.Connection.write("NICK %s" % nick)
        
    def handleNickInUse(self, ParsedMessage):
        # TODO maximum freenode nick length: 16 'er1c123456789012'
        self.nickAttempts = self.nickAttempts + 1
        self.setNick(self.Pyibber.config.get("pyib", "nick") + str(self.nickAttempts))
        
    def handleRegister(self, ParsedMessage):
        self.Pyibber.isRegistered = True
        
        self.setNick(self.Pyibber.config.get("pyib", "nick"))
        
        config = self.Pyibber.config 
        params = (
            config.get("pyib", "nick"),
            config.get("pyib", "hostname"),
            config.get("pyib", "realname")
        )
        self.Pyibber.Connection.write("USER %s 8 %s %s" % params)
        # self.Pyibber.Connection.write("")
        
    def handleConnect(self, ParsedMessage):
        """
        after connecting the nick i chose might have been in use, so lets update
        the actual value
        
        String message = parsed.getMessage();
        int offset = message.indexOf(" ", 6) - 4;
        nick = message.substring(4, offset);
        jibber.getConfig().setNick(nick);
        """
        pass
    
    def handleJoinChannels(self, ParsedMessage):
        channels = self.Pyibber.config.get("pyib", "channels")
        self.Pyibber.logger.info("trying to join channels %s" % channels)
        self.Pyibber.Connection.write("JOIN %s" % channels)
            
        """x
        channels = self.Pyibber.config.get("pyib", "channels").split(",")
        print "channels:"
        print repr(channels)
        print channels
        for channel in channels:
            channel = channel.strip();
            self.Pyibber.logger.info("trying to join channel %s" % channel)
            self.Pyibber.Connection.write("JOIN %s" % channel)
        """
        
    def handleCtcp(self, PrivateMessage):
        if (PrivateMessage.origin != PrivateMessage.CTCP):
            return
        
        if ("VERSION" == PrivateMessage.privmsg):
            #ctcpResponse()
            pass
        
    def handleDcc(self, PrivateMessage):
        if (PrivateMessage.origin != PrivateMessage.CTCP):
            return

        try:
            request = DccChat()
            request.createFromPrivateMessage(PrivateMessage)
            
            chat = Dcc.Chat.Chat(self.Pyibber, request)
            self.Pyibber.DccManager.attach(chat)
        except Exception, e:
            print "unable to handle (%s) as dcc chat" % PrivateMessage.privmsg 
            print "exception: (%s)" % e
            return;
        
    def handleChannelMessage(self, PrivateMessage):
        if (PrivateMessage.origin != PrivateMessage.CHANNEL):
            return
        
        event = PrivateMessageEvent(PrivateMessage)
        self.Pyibber.Notifier.notify(event)

    def privateMessage(self, to, message):
        privmsg = PrivateMessage()
        privmsg.to = to
        privmsg.privmsg = message
        self.Pyibber.Connection.write( privmsg.execute() )
