#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
from io import open as iopen
from xml.etree.ElementTree import iterparse, XMLParser
from sys import argv
from re import compile

if len(argv) < 3:
	infile = "/Users/mac/Downloads/im_01"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]

junk = compile(
               "(_im_mess_)-?[0-9]+|" + \
               "(_im_mess_)-?[0-9]+_[0-9]+_[0-9]+|" + \
               "(_im_msg_media)-?[0-9]+|" + \
               "(_audio_row_)-?[0-9]+_[0-9]+"
)
parser = XMLParser()
if python_implementation() != 'Jython':
    parser._parser.UseForeignDTD(True)
parser.entity['nbsp'] = ' '
tag = {}
for event, element in iterparse(infile, parser=parser, events=['start']):
    class_attr = element.get("class", "")
    m = junk.match(class_attr)
    val = m.group(1) if m is not None and m.group(1) is not None else ""
    try:
        tag["%s:%s:%s" % (element.tag, junk.sub(val, class_attr), m.group(1))] = None
    except AttributeError:
        tag["%s:%s" % (element.tag, junk.sub(val, class_attr))] = None
    element.clear()

with open(outfile, "w") as out:
    
    for k in sorted(tag):
        out.write(k + "\n")
    out.close()
