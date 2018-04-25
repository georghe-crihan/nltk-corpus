#!/usr/bin/env jython
# -*- coding: utf-8 -*-
from platform import python_implementation
if python_implementation() == 'Jython':
    import import_site_packages
from io import open as iopen
from sys import argv
from nltk.stem.snowball import RussianStemmer
from nltk import FreqDist
from analysis.corpus_analysis import CorpusAnalyser
#from pprint import pprint

if len(argv) < 6:
    input = "/Users/mac/jython-dist/belkub.txt"
    tk_output = "/Users/mac/jython-dist/tokens.txt"
    fd_output = "/Users/mac/jython-dist/freqdist.txt"
    fdc_output = "/Users/mac/jython-dist/freqdist_complete.txt"
    cn_output = "/Users/mac/jython-dist/concordance.txt"
else:
    input = argv[1]
    tk_output = argv[2]
    fd_output = argv[3]
    fdc_output = argv[4]
    concordance = argv[5]

text = CorpusAnalyser(
#    SnowballStemmer('russian', ignore_stopwords=False),
    RussianStemmer(ignore_stopwords=False),
    iopen(input, 'r', encoding='utf-8', errors='ignore').read()
)
fd = text.freq_dist()

with iopen(fd_output, 'w', encoding='utf-8', errors='ignore') as out:
    for t in FreqDist(dict(fd.most_common()[-100:])):
        out.write("%s %d %f\n" % (t, fd[t], fd.freq(t)))
    out.write(u"-----\n")

    for t in fd.most_common(100):
        out.write("%s %d\n" % (t[0], t[1]))

with iopen(fdc_output, 'w', encoding='utf-8', errors='ignore') as out:
    for t in sorted(fd.iterkeys()):
        out.write("%s %d %f\n" % (t, fd[t], fd.freq(t)))

with iopen(tk_output, 'w', encoding='utf-8', errors='ignore') as out:
    for t in text.stem_tokens:
        out.write(t + "\n")

with iopen(cn_output, 'w', encoding='utf-8', errors='ignore') as out:
    for _c in text.concordance(u"правда"):
        out.write("%s%s\n" % (_c[0], _c[1]))
