#!/usr/bin/env python
import time
import types
import StringIO
from xml.etree.ElementTree import ElementTree

# git://github.com/tallstreet/tallstreet.git/
# yos/crawl

class object_dict(dict):
    """object view of dict, you can
    >>> a = object_dict()
    >>> a.fish = 'fish'
    >>> a['fish']
    'fish'
    >>> a['water'] = 'water'
    >>> a.water
    'water'
    >>> a.test = {'value': 1}
    >>> a.test2 = object_dict({'name': 'test2', 'value': 2})
    >>> a.test, a.test2.name, a.test2.value
    (1, 'test2', 2)
    """
    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        d = self.__getitem__(item)
        # if value is the only key in object, you can omit it
        if isinstance(d, dict) and 'value' in d and len(d) == 1:
            return d['value']
        else:
            return d

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

import xml.etree.ElementTree as ET
# from object_dict import object_dict

def __parse_node(node):
    tmp = object_dict()
    # save attrs and text, hope there will not be a child with same name
    if node.text:
        tmp['value'] = node.text
    for (k,v) in node.attrib.items():
        tmp[k] = v

    for ch in node.getchildren():
        cht = ch.tag
        chp = __parse_node(ch)

        if cht not in tmp: # the first time, so store it in dict
            tmp[cht] = chp
            continue

        old = tmp[cht]
        if not isinstance(old, list):
            tmp.pop(cht)
            tmp[cht] = [old] # multi times, so change old dict to a list
        tmp[cht].append(chp) # add the new one

    return tmp

def xml_parse(content):
    """parse a xml file to a dict"""
    f = StringIO.StringIO(content)
    xml_parse_logos(f)

    t = ET.parse(f).getroot()
    tree = object_dict({t.tag: __parse_node(t)})

    print tree

