#!/usr/bin/python2

# Kindle Weather Display
# Matthew Petroff (http://www.mpetroff.net/)
# September 2012
#
# Updated for Environment Canada weather data
# Andrew Robinson
# December 2016

import urllib2
from xml.dom import minidom
import datetime
import codecs

#translations for icon codes for Environment Canada weather data
dict = {'00': 'fair',
'01': 'few-clouds',
'02': 'few-clouds',
'03': 'partly-clouds',
'04': 'mostly-clouds',
'05': 'few-clouds',
'06': 'scattered-showers',
'07': 'rain-snow',
'08': 'snow',
'09': 'scattered-thunderstorms',
'10': 'overcast',
'12': 'showers',
'13': 'rain',
'14': 'freezing-rain',
'15': 'rain-snow',
'16': 'snow',
'17': 'snow',
'18': 'blizzard',
'19': 'thunderstorms',
'22': 'partly-clouds',
'23': 'scattered-fog',
'24': 'fog',
'27': 'sleet',
'28': 'rain-sleet',
'29': ' ',
'30': 'fair',
'31': 'few-clouds',
'32': 'few-clouds',
'33': 'partly-clouds',
'34': 'mostly-clouds',
'35': 'few-clouds',
'36': 'scattered-showers',
'37': 'rain-snow',
'38': 'snow',
'39': 'scattered-thunderstorms',
'40': 'blizzard',
'43': 'wind',
'44': 'smoke'}

import sys
# get filenames
infile = sys.argv[1]
outfile = sys.argv[2]

#get options
import yaml
configs = yaml.safe_load(file('weather.conf.new','r'))
#Code of my city
CODE = configs['CODE']

import ssl
# This allows the kindle to access https:// 
context = ssl._create_unverified_context()

#url for Environment Canada
url = "https://dd.weather.gc.ca/citypage_weather/xml/" + CODE + ".xml"

#Num days to extract
days=4

# Parse temperatures
dates = [None]*days
highs = [None]*days
lows = [None]*days
icons = [None]*days

#read the weather XML
weather_xml = urllib2.urlopen(url, context=context).read()
dom = minidom.parseString(weather_xml)

#Get current conditions
curr_temp = dom.getElementsByTagName('currentConditions')[0].getElementsByTagName('temperature')[0].childNodes[0].data
curr_temp = str(int(round(float(curr_temp))))
curr_code = dom.getElementsByTagName('currentConditions')[0].getElementsByTagName('iconCode')[0].childNodes[0].data
curr_icon = dict[curr_code]

try:
	feel_temp = dom.getElementsByTagName('currentConditions')[0].getElementsByTagName('windChill')[0].childNodes[0].data
	feel_temp = str(int(round(float(feel_temp))))
except IndexError:
	try:
		feel_temp = dom.getElementsByTagName('currentConditions')[0].getElementsByTagName('humidex')[0].childNodes[0].data
		feel_temp = str(int(round(float(feel_temp))))
	except IndexError:
		feel_temp = curr_temp
	
#Get weather forecast elements
xml_forecasts = dom.getElementsByTagName('forecastGroup')[0].getElementsByTagName('forecast')

#Deal with the first entry seprately
#This is the either 'Today' or 'Tonight'
now = xml_forecasts[0].getElementsByTagName('period')[0].getAttribute('textForecastName')

dates[0] = xml_forecasts[0].getElementsByTagName('period')[0].childNodes[0].data
mycode = xml_forecasts[0].getElementsByTagName('abbreviatedForecast')[0].getElementsByTagName('iconCode')[0].childNodes[0].data
icons[0] = dict[mycode]

if "Today" in now:
	highs[0] = xml_forecasts[0].getElementsByTagName('temperatures')[0].getElementsByTagName('temperature')[0].childNodes[0].data
	lows[0] = xml_forecasts[1].getElementsByTagName('temperatures')[0].getElementsByTagName('temperature')[0].childNodes[0].data
	offset=2
else:
	highs[0] = curr_temp
	lows[0] = xml_forecasts[0].getElementsByTagName('temperatures')[0].getElementsByTagName('temperature')[0].childNodes[0].data
	offset=1

print (dates[0], highs[0], lows[0], icons[0])

for i in range(days-1):

    day = i+1
    dates[day] = xml_forecasts[2*i+offset].getElementsByTagName('period')[0].childNodes[0].data
    highs[day] = xml_forecasts[2*i+offset].getElementsByTagName('temperatures')[0].getElementsByTagName('temperature')[0].childNodes[0].data
    lows[day] = xml_forecasts[2*i+offset+1].getElementsByTagName('temperatures')[0].getElementsByTagName('temperature')[0].childNodes[0].data
    mycode = xml_forecasts[2*i+offset].getElementsByTagName('abbreviatedForecast')[0].getElementsByTagName('iconCode')[0].childNodes[0].data
    icons[day] = dict[mycode]
    print (dates[day], highs[day], lows[day], icons[day])


#
# Preprocess SVG
#

# Open SVG to process
output = codecs.open(infile, 'r', encoding='utf-8').read()

output = output.replace('CURR_TEMP',curr_temp)
output = output.replace('FEEL_TEMP',feel_temp)

# Insert icons and temperatures
output = output.replace('ICON_ONE',icons[0]).replace('ICON_TWO',icons[1]).replace('ICON_THREE',icons[2]).replace('ICON_FOUR',icons[3])
output = output.replace('HIGH_ONE',str(highs[0])).replace('HIGH_TWO',str(highs[1])).replace('HIGH_THREE',str(highs[2])).replace('HIGH_FOUR',str(highs[3]))
output = output.replace('LOW_ONE',str(lows[0])).replace('LOW_TWO',str(lows[1])).replace('LOW_THREE',str(lows[2])).replace('LOW_FOUR',str(lows[3]))

# Insert days of week
output = output.replace('DAY_THREE',dates[2]).replace('DAY_FOUR',dates[3])

# Write output
codecs.open(outfile, 'w', encoding='utf-8').write(output)
