#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
    import sqlite3
from io import open as iopen
from java.io import File
from sys.path import append as spappend
spappend("./target/minimal-pom-1.0-SNAPSHOT-jar-with-dependencies.jar")
from org.jsoup import Jsoup
from org.jsoup.nodes import Element
from org.jsoup.select import NodeTraversor, NodeVisitor
from sys import argv
#from nltk.book import *

class MyVisitor(NodeVisitor):
    def __init__(self):
        super(NodeVisitor, self).__init__()
        self._strip_list = []

    def head(self, node, depth):
        if isinstance(node, Element):
            if len(node.ownText()) == 0 \
                 and len(node.children()) == 0 \
                 and node.tag().toString() not in [ "br" ]:
                self._strip_list.append(node)

    def tail(self, node, depth):
        pass

    def strip_empty_tags(self):
        for e in self._strip_list:
            e.remove()
  

if len(argv) < 3:
	infile = "/Users/mac/Downloads/im_01"
        outfile = "/Users/mac/Downloads/dialogues.xml"
else:
	infile = argv[1]
	outfile = argv[2]

with iopen(outfile, "w", encoding="utf-8", errors="ignore") as output:
    input = File(infile)
    soup = Jsoup.parse(input, "UTF-8", "")
    visitor = MyVisitor()
    NodeTraversor(visitor).traverse(soup);
    visitor.strip_empty_tags()

    output.write(soup.outerHtml())
