#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
    import sqlite3
from io import open as iopen
from java.io import File
from java.nio.charset import Charset
from sys.path import append as spappend
spappend("./target/minimal-pom-1.0-SNAPSHOT-jar-with-dependencies.jar")
from org.jsoup import Jsoup
from org.jsoup.nodes import Element
from org.jsoup.select import NodeTraversor, NodeVisitor
from org.jsoup.parser import Tag
from sys import argv
#from nltk.book import *

class MyVisitor(NodeVisitor):
    def __init__(self):
        super(NodeVisitor, self).__init__()
        self._strip_list = []
        self._label_list = []

    def head(self, node, depth):
        if isinstance(node, Element):
            if len(node.ownText()) == 0 \
                 and len(node.children()) == 0 \
                 and node.tag().toString() not in [ "br" ]:
                self._strip_list.append(node)
            if node.tag().toString() == 'div' and node.className() == "im-mess-stack--pname":
                self._label_list.append(node)

    def tail(self, node, depth):
        pass

    def strip_empty_tags(self):
        for e in self._strip_list:
            e.remove()
  
    def replace_label_nodes(self):
	for node in self._label_list:
            for anchor in node.select("a"):
                if anchor.className() == "im-mess-stack--lnk":
                    new_div = Element(Tag.valueOf("div"), "")  
                    new_div.addClass("label")
                    new_div.attr("href", anchor.attr("href"))
                    new_div.appendText(anchor.attr("href"))
                    node.replaceWith(new_div)
                    break

if len(argv) < 3:
	infile = "/Users/mac/Downloads/im"
        outfile = "/Users/mac/Downloads/dialogues.html"
else:
	infile = argv[1]
	outfile = argv[2]

with iopen(outfile, "w", encoding="utf-8", errors="ignore") as output:
    input = File(infile)
    soup = Jsoup.parse(input, "UTF-8", "")

    # First, create a new document
    new_doc = Jsoup.parse("<body></body>")
    new_doc.updateMetaCharsetElement(True)
    new_doc.charset(Charset.forName("UTF-8"))
    new_body = new_doc.select("body").first()

    for element in soup.select("*"):
        if (element.tag().toString() == "ul" and element.className() == "ui_clean_list im-mess-stack--mess _im_stack_messages") or (element.tag().toString() == "div" and element.className() == "im-mess-stack--pname"):
            new_body.appendChild(element)

    # Then remove empty tags from it and transform the labels
    visitor = MyVisitor()
    NodeTraversor(visitor).traverse(new_doc);
    visitor.strip_empty_tags()
    visitor.replace_label_nodes()

    output.write(new_doc.outerHtml())
