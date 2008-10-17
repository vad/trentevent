from lxml import etree
from StringIO import StringIO
from dateutil import parser

#f = StringIO('<html><a>bbb</a></html>')
xmlParser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
tree = etree.parse('agenda.xhtml', xmlParser)

#print etree.tostring(tree.getroot())
parent = '//table/tbody/tr/td[last()]/'
r = tree.xpath(parent + 'span | '+ parent + 'div')

mod = 0
for el in r:
    if el.text != None:
        try:
            dateTmp = parser.parse(el.text)
            
            #reset event specific variables
            mod = 0
            dayLong = False
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

                except:
                    mod += 1
                    dayLong = True
            if mod == 1:
                print "Titolo: %s" %el.text
            if mod == 2:
                print "Descrizione: %s" %el.text
            mod += 1
            #print "%s\nA\nA\n" % el.text

