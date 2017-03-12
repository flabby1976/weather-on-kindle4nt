from icalendar import Calendar
import datetime
from datetime import time, timedelta
import urllib2
import codecs
import dateutil.rrule as rrule
from pytz import timezone
from tzlocal import get_localzone 
import textwrap

import sys
# get filenames
infile = sys.argv[1]
outfile = sys.argv[2]

# get local timezone    
localtz = get_localzone() 

import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()

utctz = timezone('UTC')
midnight_utc=time(0,0,0,tzinfo=utctz)
midnight_local=time(0,0,0,tzinfo=localtz)

myday = datetime.datetime.now(localtz).date() 

start = datetime.datetime(myday.year, myday.month, myday.day, tzinfo=localtz)
end = start + timedelta(1)
nextweek = start + timedelta(7)

ICAL_URLS = [
			"https://calendar.google.com/calendar/ical/robinsons.family.2013%40gmail.com/private-xxxxxxxx/basic.ics",
			"https://calendar.google.com/calendar/ical/flabby1976%40gmail.com/private-xxxxxxxx/basic.ics",
			"https://calendar.google.com/calendar/ical/7d5tsh19o5m9r4qbtibld2hhc0%40group.calendar.google.com/public/basic.ics",
			"https://recollect.net/api/places/0870DEC8-20DB-11E2-9E4B-940FC465FF45/services/208/events.en.ics?t=1485747640",
			"http://www.kayaposoft.com/enrico/ics/v1.0?country=can&fromDate=01-01-2017&toDate=31-12-2017&region=Ontario&en=1",
			]

agenda=[]
future=[]

for ICAL_URL in ICAL_URLS:

#	urllib.urlretrieve (ICAL_URL, "basic.ics", context=context)
#	cal = Calendar.from_ical(open('basic.ics','rb').read())

	cal_xml = urllib2.urlopen(ICAL_URL, context=context).read()
	cal = Calendar.from_ical(cal_xml)

	for component in cal.walk('vevent'):

		test_events=[]

	#Ignore those events with no text in the summary
		try:
			what=component.decoded("SUMMARY")
		except KeyError:
			continue # goes to next component in cal.walk

	#Get the start date/time of the event and duration (if spans more than one days)
		date_start = component.decoded('DTSTART')
		all_day =  not ( type(date_start) is datetime.datetime)
		try:
			date_end = component.decoded('DTEND')
		except KeyError:
			date_end = date_start
		duration = date_end.timetuple().tm_yday - date_start.timetuple().tm_yday
		print(duration)
		if all_day:
			 duration-=1
		
	#Need the start date to be TZ aware. If it isn't add dummy
		try:
			x = date_start.tzinfo
			test_date=date_start.astimezone(localtz)
		except AttributeError: 
			test_date = datetime.datetime.combine(date_start,midnight_local) 

	#Check if the event is recurring. If so find the startdate of the occurance immediately after the start of our window of interest
		try:
			if component['RRULE']:
				z=component['RRULE'].to_ical()
				seq_start=test_date
				test_date = rrule.rrulestr(z, dtstart=seq_start).after(start - timedelta(1), inc=True)
				if not test_date:
					continue  #No instances of this recurring event in our window, so go to next event
		except KeyError:
			pass

		test_event = {'when': test_date, 'what': component.decoded("SUMMARY"), 'all day': not ( type(date_start) is datetime.datetime )}
		test_events.append(test_event)

		for day_count in range(duration):
			next = datetime.datetime.combine(test_date.date(),midnight_local)+timedelta(day_count+1)
			test_event = {'when': next, 'what': component.decoded("SUMMARY")+" ("+ str(day_count+2)+"/"+str(duration+1)+")", 'all day': True}
			test_events.append(test_event)

	#Check if event is within our window of interest
		for test_event in test_events:
			if( test_event['when'].timetuple().tm_year == start.timetuple().tm_year ):
				if( test_event['when'].timetuple().tm_yday >= start.timetuple().tm_yday ) and (test_event['when'].timetuple().tm_yday <= nextweek.timetuple().tm_yday ):
					agenda.append(test_event)
					print(test_event, duration)

#sort by date
agenda = sorted(agenda, key=lambda k: k['when']) 
future = sorted(future, key=lambda k: k['when']) 

output = codecs.open(infile, 'r', encoding='utf-8').read()

display_lines=[]

thisday=start.strftime("%a")
for try_event in agenda:
	try_day=try_event['when'].strftime("%a")
	if not(try_day==thisday):
		display_lines += [""]
		display_lines += [try_day]
		thisday=try_day
	if try_event['all day']:
		agenda_entry  = try_event['what']
	else:
		agenda_entry  = try_event['when'].strftime("%H:%M") + ': ' +  try_event['what']

	display_lines += textwrap.fill(agenda_entry, width=30, initial_indent='', subsequent_indent='  ').splitlines()
				
count = 0
for lines in display_lines:
	output = output.replace('agenda' + str(count) + ':', lines)
	print lines
	count+=1
	if (count == 50):
		break

for count in range(16):
	output = output.replace('agenda' + str(count) + ':','')


	# Write output
codecs.open(outfile, 'w', encoding='utf-8').write(output)

