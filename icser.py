from lxml import etree
from StringIO import StringIO

#f = StringIO('<html><a>bbb</a></html>')
parser = etree.XMLParser(ns_clean=True, remove_blank_text=True)
tree = etree.parse('agenda.xhtml', parser)

#print etree.tostring(tree.getroot())
r = tree.xpath('//table/tbody/tr/td[last()]/span')

print len(r)

for span in r:
    if span.text != None:
        print "%s\nA\nA\n" % span.text

