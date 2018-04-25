# -*- coding: utf-8 -*-
from nltk import word_tokenize, Index, FreqDist, WordNetLemmatizer

class CorpusAnalyser(object):
    def __init__(self, stemmer, raw):
        self._ignore_list = [
            ',', '-', '.', '?', '!', ':', '(', ')', '...', '``', "''", '[', ']', ';', '+', '%', '#', '=',
            u"\N{HORIZONTAL ELLIPSIS}",
            u"\N{LEFT-POINTING DOUBLE ANGLE QUOTATION MARK}",
            u"\N{RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK}",
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        ]
        _tokens = word_tokenize(raw)
        self._text = [w.lower() for w in _tokens]
        self.vocab = sorted(set(self._text))
        self._stemmer = stemmer
        self._index = Index((self._stem(_word), _i)
                                 for (_i, _word) in enumerate(self._text))

        _wnl = WordNetLemmatizer()
        self.stem_tokens = [_wnl.lemmatize(_t) for _t in _tokens]

    def concordance(self, word, width=40):
        _c = []
        key = self._stem(word)
        wc = width/4 # words of context
        for i in self._index[key]:
            lcontext = ' '.join(self._text[i-wc:i])
            rcontext = ' '.join(self._text[i:i+wc])
            ldisplay = '%*s' % (width, lcontext[-width:])
            rdisplay = '%-*s' % (width, rcontext[:width])
            _c.append((ldisplay, rdisplay))
        return _c

    def _stem(self, word):
        return self._stemmer.stem(word).lower()

    def freq_dist(self):
        _freqdist = FreqDist()
        for word in self.stem_tokens:
            if word not in self._ignore_list:
                _freqdist[word.lower()] += 1
        return _freqdist

