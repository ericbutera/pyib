"""This is the launcher script for pyib.

Lolwut.
""" 
from Pyib import Pyibber
from Pyib.Plugins.ChuckNorris import ChuckNorris
from Pyib.Plugins.WeatherYahoo import WeatherYahoo
from Pyib.Plugins.UrlCatcher import UrlCatcher

import sys
import logging

try:
    ini = str(sys.argv[1])
except Exception:
    ini = "localhost.ini"

# Fri, 02 Jul 2004 13:06:18 DEBUG    A debug message
LOG_FILENAME = "/tmp/pyibber-%s.log" % ini
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
    format='[%(asctime)s][%(levelname)s][%(message)s]',
    #datefmt='%a, %d %b %Y %H:%M:%S'
    datefmt='%Y.%m.%d %H:%M:%S'
)
logger = logging.getLogger('Pyib')

bot = Pyibber(ini, logger)
bot.Notifier.addListener(ChuckNorris(bot))
bot.Notifier.addListener(WeatherYahoo(bot))
bot.Notifier.addListener(UrlCatcher(bot))

print "main.py calling bot.run()"

bot.run()
    
print "bot.run() finished"
