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

if len(argv) < 8:
    input = "/Users/mac/jython-dist/belkub.txt"
    tk_output = "/Users/mac/jython-dist/tokens.txt"
    fd_output = "/Users/mac/jython-dist/freqdist.txt"
    fdc_output = "/Users/mac/jython-dist/freqdist_complete.txt"
    cn_output = "/Users/mac/jython-dist/concordance.txt"
    cl2_output = "/Users/mac/jython-dist/collocations2.txt"
    cl3_output = "/Users/mac/jython-dist/collocations3.txt"
else:
    input = argv[1]
    tk_output = argv[2]
    fd_output = argv[3]
    fdc_output = argv[4]
    cn_output = argv[5]
    cl2_output = argv[6]
    cl3_output = argv[7]

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

with iopen(cl2_output, 'w', encoding='utf-8', errors='ignore') as out:
    bigrams, trigrams = text.collocations(10000, 3)
    for c in bigrams:
        out.write("%s %s\n" % (c[0], c[1]))

    with iopen(cl3_output, 'w', encoding='utf-8', errors='ignore') as out:
        for c in trigrams:
            out.write("%s %s %s\n" % (c[0], c[1], c[2]))

with iopen(cn_output, 'w', encoding='utf-8', errors='ignore') as out:
    for _c in text.concordance(u"правда"):
        out.write("%s%s\n" % (_c[0], _c[1]))
