from lxml import etree
from dateutil import parser
from icalendar import Calendar, Event
import time

#f = StringIO('<html><a>bbb</a></html>')
xmlParser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
tree = etree.parse('agenda.xhtml', xmlParser)

#print etree.tostring(tree.getroot())
parent = '//table/tbody/tr/td[last()]/'
r = tree.xpath(parent + 'span | '+ parent + 'div')

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

mod = 0
for el in r:
    if el.text != None:
        try:
            dateTmp = parser.parse(el.text)
            
            #reset event specific variables
            mod = 0
            dayLong = False
            event = Event()

            #prevent that Lines like "Sabato" are parsed correctly
            if len(el.text) < 15: 
                continue
            date = dateTmp
            dateText = el.text
            
            print "DATA:"
            print date
        except:
            if mod == 0:
                hourText = el.text.replace('.', ':')
                print "Ora: %s" % el.text
                count = hourText.count(':')
                
                #if exceptions have been raised, maybe it's not an hour (DAYLONG event)
                try:
                    # there should always be at least one hour
                    pos = hourText.find(':')
                    textStartHour = hourText[pos-2:pos+3]
                    timeStart = parser.parse(textStartHour)
                    
                    dateStart = date.replace(hour = timeStart.hour, minute = timeStart.minute)
                    print dateStart

                    #if there are more hours, then they are start and end time
                    if count == 2:
                        #find next hour
                        pos = hourText.find(':', pos + 1)
                        textEndHour = hourText[pos-2:pos+3]
                        timeEnd = parser.parse(textEndHour)
                    else:
                        from dateutil.relativedelta import relativedelta

                        #if no end hour specified, then set it to start + 2h
                        timeEnd = timeStart + relativedelta(hours = 2)
                    
                    dateEnd = date.replace(hour = timeEnd.hour, minute = timeEnd.minute)
                    print dateEnd
                    event.add('dtstart', dateStart)
                    event.add('dtstamp', dateStart) #maybe it's better to use NOW()
                    event.add('dtend', dateEnd)
                    
                    #TODO: use UID to avoid duplication importing in the calendar manager
                    #print 'UID'
                    #event['uid'] = time.mktime(dateStart.timetuple())
                    #print event['uid']
                    
                except:
                    mod += 1
                    dayLong = True
            if mod == 1:
                event.add('summary', el.text)
                print "Titolo: %s" %el.text
            if mod == 2:
                event.add('description', el.text)
                event.add('priority', 5)

                if dayLong:
                    event.add('dtstart;value=date', "%d%d%d" % (date.year, date.month, date.day))

                cal.add_component(event)
                print "Descrizione: %s" %el.text
            mod += 1


f = open('abitarelaterra.ics', 'wb')
f.write(cal.as_string())
f.close()

