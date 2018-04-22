#!/usr/bin/env jython
# -*- coding: utf-8 -*-
#import import_site_packages
#import sqlite3
from xml.etree import ElementTree as etree
from sys import argv
#from nltk.book import *

if len(argv) < 3:
	infile = "/Users/mac/Downloads/Диалоги.webarchive"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]
 
for event, element in etree.iterparse(infile):
	if event=='start':
		if element.tag == 'body':
                    pass
	if event=='end':
		if element.tag == 'body':
                    pass
	element.clear()
