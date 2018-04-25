#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
    import sqlite3
from sys import argv

if len(argv) < 3:
	infile = "/Users/mac/Downloads/Диалоги.webarchive"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]

#execfile("analysis/analyser.py") 
import analysis.analyser
