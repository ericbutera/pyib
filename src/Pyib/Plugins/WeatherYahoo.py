'''
Fetches weather reports from Yahoo! Weather

Written by Thomas Upton (http://www.thomasupton.com/),
with contributions from Chris Lasher (http://igotgenes.blogspot.com/).

This code is licensed under a BY-NC-SA Creative Commons license.
http://creativecommons.org/licenses/by-nc-sa/3.0/us/

See http://www.thomasupton.com/blog/?p=202 for more information.
'''

from Pyib.Events.Listener import Listener
import urllib
from xml.dom.minidom import parse
import traceback

class WeatherYahoo(Listener):
    
    # Yahoo!'s limit on the number of days they will forecast
    DAYS_LIMIT = 2
    WEATHER_URL = 'http://xml.weather.yahoo.com/forecastrss?p=%s'
    METRIC_PARAMETER = '&u=c'
    WEATHER_NS = 'http://xml.weather.yahoo.com/ns/rss/1.0'
    
    def __init__(self, Pyibber):
        Listener.__init__(self, Pyibber)
        self.Pyibber = Pyibber
        
    def handleEvent(self, Event):
        if (".weather" != Event.PrivateMessage.privmsg[0:8]):
            return
        
        location = Event.PrivateMessage.privmsg[9:14]
        extra  = Event.PrivateMessage.privmsg[14:]

        if (len(location) is not 5 or len(extra) > 0):
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, "Usage: .weather <5 digit zipcode>.")
            return
        
        options = {
            "nocurr":       False,
            "delim":        " and ",
            "forecast":     2,
            "location":     True,
            "metric":       False,
            "verbose":      False,
            "temperature":  False,
            "conditions":   False,
            "output":       False
        }
        
        #cli_parser.add_option('-n', '--nocurr', action='store_true', help="suppress reporting the current weather conditions", default=False)
        #cli_parser.add_option('-d', '--delim', action='store', type='string', help="use the given string as a delimiter between the temperature and the conditions", default=" and ")
        #cli_parser.add_option('-f', '--forecast', action='store', type='int', help="show the forecast for DAYS days", default=0)
        #cli_parser.add_option('-l', '--location', action='store_true',help="print the location of the weather",default=False)
        #cli_parser.add_option('-m', '--metric', action='store_true', help="show the temperature in metric units (C)", default=False)
        #cli_parser.add_option('-v', '--verbose', action='store_true', help="print the weather section headers", default=False)
        #cli_parser.add_option('-t', '--temperature', action="store_true", help="print only the current temperature", default=False)
        #cli_parser.add_option('-c', '--conditions', action="store_true", help="print only the current conditions", default=False )
        #cli_parser.add_option('-o', '--output', action='store', help="print the weather conditions to a specified file name", default="")
        
        try:
            weather = self.get_weather(location, options)
        except Exception, e:
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, "You didn't do it right: %s" % e)
            return

        report = self.create_report(weather, options)

        if report == None:
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, "Unable to generate report")
            return -1
        else:
            self.Pyibber.Commandx.privateMessage(Event.PrivateMessage.to, report)

    def get_weather(self, location, options):
        """
        Fetches weather report from Yahoo!
    
        :Parameters:
        -`location`: A five digit US zip code.
        -`days`: number of days to obtain forecasts
    
        :Returns:
        -`weather_data`: a dictionary of weather data
        """
    
        # Get the correct weather url.
        url = self.WEATHER_URL % location

        if options['metric']:
            url = url + self.METRIC_PARAMETER
    
        # Parse the XML feed.
        try:
            dom = parse(urllib.urlopen(url))
        except:
            return None
        
        # Get the units of the current feed.
        # Get the location of the specified location code.
        # Get the currrent conditions.
        
        yunits = dom.getElementsByTagNameNS(self.WEATHER_NS, 'units')[0]    
        ylocation = dom.getElementsByTagNameNS(self.WEATHER_NS, 'location')[0]
        ycondition = dom.getElementsByTagNameNS(self.WEATHER_NS, 'condition')[0]
    
        # Hold the forecast in a hash.
        forecasts = []
    
        # Walk the DOM in order to find the forecast nodes.
        for i, node in enumerate(dom.getElementsByTagNameNS(self.WEATHER_NS,'forecast')):
            
            # Stop if the number of obtained forecasts equals the number of requested days
            if i >= options['forecast']:
                break
            else:
                # Insert the forecast into the forcast dictionary.
                forecasts.append (
                    {
                        'date': node.getAttribute('date'),
                        'low': node.getAttribute('low'),
                        'high': node.getAttribute('high'),
                        'condition': node.getAttribute('text')
                    }
                )
    
        # Return a dictionary of the weather that we just parsed.
        weather_data = {
            'current_condition': ycondition.getAttribute('text'),
            'current_temp': ycondition.getAttribute('temp'),
            'forecasts': forecasts,
            'units': yunits.getAttribute('temperature'),
            'city': ylocation.getAttribute('city'),
            'region': ylocation.getAttribute('region'),
        }
        
        return weather_data
    
    def create_report(self, weather_data, options):
        """
        Constructs a weather report as a string.
    
        :Parameters:
        -`weather_data`: a dictionary of weather data
        -`options`: options to determine output selections
    
        :Returns:
        -`report_str`: a formatted string reporting weather
    
        """
        if weather_data == None:
            return None
    
        report = []
        
        if options['location']:
            if options['verbose']:
                # Add the location header.
                report.append("Location:")
    
            # Add the location.
            location_str = "%(city)s %(region)s " % weather_data
            report.append(location_str)
    
        if (not options['nocurr']):
            if options['verbose']:
                # Add current conditions header.
                report.append("Current conditions:")
    
            # Add the current weather.
            curr_str = ""
            if (not options['conditions']):
                curr_str = curr_str + "%(current_temp)s%(units)s" % weather_data
    
            if (not options['conditions'] and not options['temperature']):
                curr_str = curr_str + options['delim'].decode('string_escape')
    
            if (not options['temperature']):
                curr_str = curr_str + "%(current_condition)s. " % weather_data
    
            report.append(curr_str)
    
        if (options['forecast'] > 0):
            if options['verbose']:
                # Add the forecast header.
                report.append("Forecast:")
    
            # Add the forecasts.
            for forecast in weather_data['forecasts']:
                
                forecast['units'] = weather_data['units']
            
                forecast_str = "[%(date)s High: %(high)s%(units)s Low: %(low)s%(units)s Conditions: %(condition)s] " % forecast
    
                report.append(forecast_str)
    
        report_str = " ".join(report)
        
        return report_str
