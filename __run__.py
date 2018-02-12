#!/usr/bin/env jython
# -*- coding: utf-8 -*-
import import_site_packages
#import sqlite3
from xml.etree import ElementTree as etree
from sys import argv
from os import mkdir
from os.path import exists,isdir
#from nltk.book import *
from subprocess import call 

def write_resource(filepath, data):
	from base64 import b64decode
	print "path: ", ilepath
	f = open(filepath, 'w')
	f.write(b64decode(data))
	f.close()
	
def infer_filename(url):
	from urlparse import urlparse
	from os.path import basename
	a = urlparse(url)
	return basename(a.path)

output_directory = '1'
if not exists(output_directory) or not isdir(output_directory):
	mkdir(output_directory)

if len(argv) < 2:
	infile = "/Users/mac/Downloads/Диалоги.webarchive"
else:
	infile = argv[1]
 
call([ 'plutil', '-convert', 'xml1', '-o', infile + '.xml', infile])
#texts()
dic = {}
c = 1
filepath = ''
for event, element in etree.iterparse(infile + '.xml'):
	if event=='start':
		if element.tag == 'dict':
			dic.clear()
			filepath = output_directory + '/%d' % (c,)
			print "PATH:", filepath
	if event=='end' and filepath:
		if element.tag == 'dict':
			print infer_filename(dic['url'])
			if 'cont' in dic:
				print "path: ", filepath
				write_resource(filepath, dic['cont'])
			if 'resp' in dic:
				write_resource(filepath + '.xml', dic['resp'])
			c =+ 1
		if element.tag == 'key':
			if element.text=='WebResourceURL':
				tag = 'url'
				continue
			if element.text=='WebResourceResponse':
				tag = 'resp'
				continue
			if element.text=='WebResourceData':
				tag = 'cont'
				continue
			if element.text=='WebResourceMIMEType':
				tag = 'mime'
				continue
			print element.tag, element.text
			continue
		if element.tag == 'data':
			dic[tag] = element.text
			continue
		if element.tag == 'string':
			dic[tag] = element.text 
		print element.tag
	element.clear()
