#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
from io import open as iopen
from xml.etree.ElementTree import iterparse, XMLParser, tostring as ETtostring
from sys import argv
from subprocess import call

if len(argv) < 3:
	infile = "/Users/mac/Downloads/im_01"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]

#call([ 'tidy', '-o', outfile, '-asxml', infile ])

#with iopen(outfile, "w", encoding="utf-8", errors="ignore") as output:
if True:
    parser = XMLParser()
    if python_implementation() != 'Jython':
        parser._parser.UseForeignDTD(True)
    parser.entity['nbsp'] = ' '
    for event, element in iterparse(outfile, parser=parser, events=['start']):
#        if element.tag == "div" and element.get("class", "") == "im-mess-stack--content":
        if (element.tag == "ul" and element.get("class", "") == "ui_clean_list im-mess-stack--mess _im_stack_messages") or (element.tag == "div" and element.get("class", "") == "im-mess-stack--pname") :
            print ETtostring(element, encoding='utf-8')
        element.clear()
#    output.close()
