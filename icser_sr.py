#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
#from dateutil import parser
from icalendar import Calendar, Event
from urllib import urlopen

LOCATION = "Supercinema Rovereto"

## DECODE HTML ENTITIES
from htmlentitydefs import name2codepoint as n2cp
import re

def substitute_entity(match):
    ent = match.group(2)
    if match.group(1) == "#":
        return unichr(int(ent))
    else:
        cp = n2cp.get(ent)

        if cp:
            return unichr(cp)
        else:
            return match.group()

def decode_htmlentities(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]

## END DECODE HTML ENTITIES

file = urlopen("http://www.supercinemarovereto.it/rassegne.php")
doc = BeautifulSoup(''.join(file.readlines()))

ap = doc.find('td', {"class": "main"}).findAll('p')

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')


year = 0
for p in ap:
    p = decode_htmlentities(p.string).strip()
    if not p: continue

    if not year:
        year = p.split(' ')[-1]
        continue
    
    event = Event()

    date = p.split(' ')[0].split('/')
    desc = ' '.join(p.split(' ')[1:])
    #event.add('dtstart', dateStart)
    #event.add('dtstamp', dateStart) #maybe it's better to use NOW()
    #event.add('dtend', dateEnd)
    event.add('location', LOCATION)
    event.add('dtstart;value=date', "%s%.2d%.2d" % (int(year),
        int(date[1]),int(date[0])))
    event.add('summary', desc)
    cal.add_component(event)

f = open('scr.ics', 'wb')
f.write(cal.as_string())
f.close()

