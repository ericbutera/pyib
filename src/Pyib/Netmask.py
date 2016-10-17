'''
Created on Jan 9, 2010

@author: eric
'''

import re

class Netmask(object):
    '''
    parses an irc netmask
    '''
    netmask = ''
    nick = ''
    ident = ''
    host = ''
    USER = 'user'
    SERVER = 'server'

    def __init__(self, source):
        '''
        ctor, pass in the source the message came from eg er1c_!n=eric@ericbutera.us
        '''
        self.netmask = source
        
        m = re.search('^([^!@]+)!([^@]+)@(.*)$', source)
        if (m is not None):
            #print "group 0(%s) 1(%s) 2(%s) 3(%s) " % (m.group(0), m.group(1), m.group(2), m.group(3))
            self.nick   = m.group(1)
            self.ident  = m.group(2)
            self.host   = m.group(3)
            self.origin = self.USER
        else:
            self.origin = self.SERVER
