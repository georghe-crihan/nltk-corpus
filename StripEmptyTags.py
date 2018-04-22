#!/usr/bin/env jython
# -*- coding: utf-8 -*-
#import import_site_packages
#import sqlite3
from io import open as iopen
from bs4 import BeautifulSoup 
from sys import argv
#from nltk.book import *

#def recursively_empty(e):
#    if e.text:
#        return False
#    return all((recursively_empty(c) for c in e.iterchildren()))

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
    print soup
#        if recursively_empty(element):
#            parent.remove(element)
#        if element.tag == "div" and element.get("class", "") == "im-mess-stack--content":
#        if element.tag == "ul" and element.get("class", "") == "ui_clean_list im-mess-stack--mess _im_stack_messages":
#            print ETtostring(element, encoding='utf-8')
#        element.clear()
#    output.close()
