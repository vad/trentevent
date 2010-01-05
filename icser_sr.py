#!/usr/bin/env python

import sys

try:
    from icalendar import Calendar, Event
except:
    sys.path.append("icalendar-1.2-py2.5.egg")
    from icalendar import Calendar, Event

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from htmldecode import decode_htmlentities


LOCATION = "Supercinema Rovereto"

class EventReader:
    provider = ""
    doc = None
    location = ""
    file_path = ""
    url = ""
    
    def __init__(self, from_file=False):
        if from_file:
            f = open(self.file_path)
        else:
            f = urlopen(self.url)

        page = ''.join(f.readlines())
        self.doc = BeautifulSoup(page)
        f.close()
        
    #----------------------------------------------------------------------
    def get_events(self):
        """
        virtual method
        """
        pass
            
        
        
########################################################################
class SupercinemaRoveretoEventReader(EventReader):
    """
    Specialized for www.supercinemarovereto.it
    >>> scr = SupercinemaRoveretoEventReader(True)
    >>> len([e for e in scr.get_events()])
    12
    """
    location = LOCATION
    file_path = "test/data/rassegne.php"
    url = "http://www.supercinemarovereto.it/rassegne.php"

        
    def get_events(self):
        from hashlib import md5
        ap = self.doc.find('td', {"class": "main"}).findAll('p')
        
        year = 0
        for p in ap:
            p = decode_htmlentities(p.string).strip()
            if not p: continue
        
            if not year:
                year = p.split(' ')[-1]
                continue
            
            event = Event()
        
            try:
                date = p.split(' ')[0].split('/')
                desc = ' '.join(p.split(' ')[1:])
                #event.add('dtstart', dateStart)
                #event.add('dtstamp', dateStart) #maybe it's better to use NOW()
                #event.add('dtend', dateEnd)
                event.add('location', LOCATION)
                event.add('dtstart;value=date', "%s%.2d%.2d" % (int(year),
                    int(date[1]),int(date[0])))
                event.add('summary', desc)
                
                #TODO: add other info like the date!!
                md5text = desc
                
                event['uid'] = md5(md5text).hexdigest()+'@supercinemarovereto.it'
                yield event
            except:
                continue
    

def main():
    scr = SupercinemaRoveretoEventReader(True)
    events = scr.get_events()
    
    cal = Calendar()
    #cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')
    for event in events:
        cal.add_component(event)
    
    f = open('scr.ics', 'wb')
    f.write(cal.as_string())
    f.close()

if __name__ == "__main__":
    main()
