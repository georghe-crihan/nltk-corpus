#!/usr/bin/python
# -*- coding: utf-8 -*-
from re import compile
from io import open as iopen
from sys import argv

dic = {}
key = ""
stanza = ""
name_re = compile(r'^/([^ \t]+)\n$')
for line in iopen(argv[1], "r", encoding="utf-8", errors="ignore"):
        # Search for the label first
	m = name_re.match(line)
        if m:
		# Flush stanza
		if stanza <> "":
                    dic[key].append(stanza)
                stanza = ""
		# Set new label
		key = m.group(1)
                if key not in dic:
                    dic[key] = []
                continue
        # Just add one more line to current stanza
        stanza += line

for key in dic:
    with iopen(key + '.txt', "w", encoding="utf-8", errors="ignore") as output:
        for stanza in dic[key]:
            output.write(stanza)
