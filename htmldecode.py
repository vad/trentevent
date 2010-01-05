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
    """    
    >>> decode_htmlentities('&#38;')
    u'&'
    >>> decode_htmlentities('abc')
    'abc'
    """

    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
    return entity_re.subn(substitute_entity, string)[0]

## END DECODE HTML ENTITIES
