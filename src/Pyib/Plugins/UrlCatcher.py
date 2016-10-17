'''
Created on Jan 11, 2010

@author: eric
'''

import sqlite3
import re
import urllib;

from pyquery import PyQuery as pq
from lxml import etree

import threading


from Pyib.Events.Listener import Listener

class UrlCatcher(Listener):

    conn = None
    
    def __init__(self, Pyibber):
        Listener.__init__(self, Pyibber)
        self.Pyibber = Pyibber
        self.createTables()

    def handleEvent(self, Event):
        self.Event = Event
        self.parseAndSave(Event)

        m = Event.PrivateMessage.privmsg
        if (".urlcatcher" == m or ".urlcatcher help" == m):
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, ".urlcatcher commands: .urlcatcher latest; .urlcatcher topassholes")
            return
        
        if (".urlcatcher latest" == m):
            self.handleLatest(Event)
            return
        
        if (".urlcatcher topassholes" == m):
            self.handleTop(Event)
            return
        
    def handleTop(self, Event):
        try:
            sql = """SELECT nick, count(*) AS recordCount FROM urlcatcher_link GROUP BY nick ORDER BY recordCount DESC LIMIT 5"""
            c = self.connection().cursor()
            c.execute(sql)
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, "Nick: Url count")
            for row in c:
                line = row[0] +": "+ str(row[1])
                self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, line)
        except Exception, e:
            self.Pyibber.logger.warning("urlcatcher unable to fetch latest links: %s" % e)
        
    def handleLatest(self, Event):
        try:
            sql = """SELECT * FROM urlcatcher_link ORDER BY createdDate DESC LIMIT 5"""
            c = self.connection().cursor()
            c.execute(sql)
            x = 1
            for row in c:
                line = str(x) +" "+ row[0] +" by "+ row[1] +" at "+ row[4]
                self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, line)
                x = x + 1
        except Exception, e:
            self.Pyibber.logger.warning("urlcatcher unable to fetch latest links: %s" % e)

    def parseAndSave(self, Event):
        matched = re.findall(r"((?:http|https|ftp)://[^ ]+)", Event.PrivateMessage.privmsg)
        for url in matched:
            try:
                self.insertUrl(
                    url, 
                    Event.PrivateMessage.ParsedMessage.Netmask.nick, 
                    Event.PrivateMessage.ParsedMessage.Netmask.netmask, 
                    Event.PrivateMessage.to
                )
                
                self.fetchAndDisplay(url);
            except Exception, e:
                self.Pyibber.logger.warning("urlcatcher unable to save link: %s" % e)

    def createTables(self):
        c = self.connection().cursor()
        try:
            c.execute('''create table urlcatcher_link (
                url TEXT,
                nick VARCHAR(32),
                netmask VARCHAR(255),
                channel VARCHAR(64),
                createdDate DATE
            )''')
        except Exception:
            self.Pyibber.logger.info("urlcatcher db table exists")
    
    def connection(self):
        if (self.conn is None):
            dbpath = self.Pyibber.config.get("pyib", "dbpath");
            self.conn = sqlite3.connect(dbpath)
        return self.conn
    
    def insertUrl(self, url, nick, netmask, channel):
        conn = self.connection()
        c = conn.cursor()
        values = [url, nick, netmask, channel]
        c.execute("insert into urlcatcher_link values (?, ?, ?, ?, DATETIME('NOW'))", values);
        conn.commit()
        
    def isUrlSafe(self, url):
        if (url.count(":") > 1):
            return False
        if (url.count("@") > 0):
            return False
        
        return True

    def threaded(callback=lambda *args, **kwargs: None, daemonic=False):
        """Decorate  a function to run in its own thread and report the result
        by calling callback with it."""
        def innerDecorator(func):
            def inner(*args, **kwargs):
                target = lambda: callback(func(*args, **kwargs))
                t = threading.Thread(target=target)
                t.setDaemon(daemonic)
                t.start()
            return inner
        return innerDecorator
       
    @threaded()
    def fetchAndDisplay(self, url):
        if (True != self.isUrlSafe(url)):
            return
        
        try:
            #f = urllib.urlopen(url)
            data = urllib.urlopen(url).read()
            d = pq(data)
            title = d("title").text()
            title = title.replace("\n", "").replace("\r", "")

            self.Pyibber.Commandx.privateMessage(self.Event.PrivateMessage.to, "Saved [%s]" % title)
        except Exception, e:
            return None
