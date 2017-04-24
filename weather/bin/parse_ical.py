from icalendar import Calendar
import datetime
from datetime import time, timedelta
import urllib2
import codecs
import dateutil.rrule as rrule
from pytz import timezone
import textwrap

def make_local(test_date):
    try:
        x = test_date.tzinfo
        new_date=test_date.astimezone(localtz)
    except AttributeError: 
        new_date = datetime.datetime.combine(test_date,midnight_local)
#    print new_date
    return new_date

import sys
# get filenames
infile = sys.argv[1]
outfile = sys.argv[2]

import ssl
import cgi

# This allows the kindle to access https:// 
context = ssl._create_unverified_context()

#get options
import yaml
configs = yaml.safe_load(file('weather.conf.new','r'))
ICAL_URLS = configs['ICAL_URLS']
localtz=timezone(configs['localtz'])

# set local timezone
start=datetime.datetime.now(localtz)
localtz=start.tzinfo

utctz = timezone('UTC')
midnight_utc=time(0,0,0,tzinfo=utctz)
midnight_local=time(0,0,0,tzinfo=localtz)

start = datetime.date.today()
start = datetime.datetime.combine(start, midnight_local)

print(start)

#start = datetime.datetime(myday.year, myday.month, myday.day, tzinfo=localtz)
end = start + timedelta(1)
nextweek = start + timedelta(21)

agenda=[]

for ICAL_URL in ICAL_URLS:

    try:
        cal_xml = urllib2.urlopen(ICAL_URL, context=context).read()
    except urllib2.HTTPError:
        print('URL error: '+ ICAL_URL)
        continue # skip URL with errors

    try:
        cal = Calendar.from_ical(cal_xml)
    except ValueError:
        continue # skip files with errors

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

        test_start=make_local(date_start)
        test_end=make_local(date_end)
         
        duration = test_end.timetuple().tm_yday - test_start.timetuple().tm_yday 

        if all_day:
            duration-=1

        test_date=test_start
        
    #Check if the event is recurring. If so find the startdate of the occurance immediately after the start of our window of interest
        try:
            if component['RRULE']:
                z=component['RRULE'].to_ical()
                seq_start=test_date
                test_date = rrule.rrulestr(z, dtstart=seq_start).after(start - timedelta(1), inc=True)
                if not test_date:
                    continue  #No instances of this recurring event in our window, so go to next event
        except KeyError:
            pass #Not recurring

        test_event = {'when': test_date, 'what': component.decoded("SUMMARY"), 'all day': not ( type(date_start) is datetime.datetime )}
        test_events.append(test_event)

        for day_count in range(duration):
            next = datetime.datetime.combine(test_date.date(),midnight_local)+timedelta(day_count+1)
            test_event = {'when': next, 'what': component.decoded("SUMMARY")+" (Day "+ str(day_count+2)+"/"+str(duration+1)+")", 'all day': True}
            test_events.append(test_event)

    #Check if event is within our window of interest
        for test_event in test_events:
            if( test_event['when'].timetuple().tm_year == start.timetuple().tm_year ):
                if( test_event['when'].timetuple().tm_yday >= start.timetuple().tm_yday ) and (test_event['when'].timetuple().tm_yday <= nextweek.timetuple().tm_yday ):
                    agenda.append(test_event)
                    print(test_event)

#sort by date
agenda = sorted(agenda, key=lambda k: k['when']) 

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
    lines=lines.decode('utf-8')
    print lines
    output = output.replace('agenda' + str(count) + ':', cgi.escape(lines))
    count+=1
    if (count == 50):
        break

for count in range(16):
    output = output.replace('agenda' + str(count) + ':','')

    # Write output
codecs.open(outfile, 'w', encoding='utf-8').write(output)

