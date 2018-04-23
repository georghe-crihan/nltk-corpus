#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
    import sqlite3
from io import open as iopen
from bs4 import BeautifulSoup 
from sys import argv
#from nltk.book import *

if len(argv) < 3:
	infile = "/Users/mac/Downloads/im_01"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]

with iopen(outfile, "w", encoding="utf-8", errors="ignore") as output:
    soup = BeautifulSoup(iopen(infile, "r", encoding="utf-8", errors="ignore"), "html.parser")
    for element in soup.find_all(): 
        if len(element.text) == 0:
            element.extract()
    output.write(soup)
    output.close()
