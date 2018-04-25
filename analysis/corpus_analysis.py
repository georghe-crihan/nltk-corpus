# -*- coding: utf-8 -*-
from re import compile
from nltk import word_tokenize, Index, FreqDist, WordNetLemmatizer
from nltk.collocations import BigramAssocMeasures, TrigramAssocMeasures, BigramCollocationFinder


class CorpusAnalyser(object):
    def __init__(self, stemmer, raw):
        self._ignore_list = [
            '...', '``', "''",
            u"\N{HORIZONTAL ELLIPSIS}",
            u"\N{LEFT-POINTING DOUBLE ANGLE QUOTATION MARK}",
            u"\N{RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK}",
        ]
        _tokens = word_tokenize(raw)
        self._words = [w.lower() for w in _tokens]
        self.vocab = sorted(set(self._words))
        self._stemmer = stemmer
        self._re_numbers = compile(r"[+-]?[0-9]+")
        self._re_punctuation = compile(r"[\.,;:\-+=%\?!#\(\)\[\]]")
        self._index = Index((self._stem(_word), _i)
                                 for (_i, _word) in enumerate(self._words))

        _wnl = WordNetLemmatizer()
        self.stem_tokens = [_wnl.lemmatize(_t) for _t in _tokens]

        self._finder = BigramCollocationFinder.from_words(self._words)

    def concordance(self, word, width=40):
        _c = []
        key = self._stem(word)
        wc = width/4  # words of context
        for i in self._index[key]:
            lcontext = ' '.join(self._words[i-wc:i])
            rcontext = ' '.join(self._words[i:i+wc])
            ldisplay = '%*s' % (width, lcontext[-width:])
            rdisplay = '%-*s' % (width, rcontext[:width])
            _c.append((ldisplay, rdisplay))
        return _c

    def _stem(self, word):
        return self._stemmer.stem(word).lower()

    def freq_dist(self):
        _freqdist = FreqDist()
        for word in self.stem_tokens:
            if (word not in self._ignore_list) and \
                    self._re_numbers.match(word) is None and \
                    self._re_punctuation.match(word) is None:
                _freqdist[word.lower()] += 1
        return _freqdist

    def collocations(self, freq=None):
        if freq:
            self._finder.apply_freq_filter(freq)
        return self._finder.nbest(BigramAssocMeasures().pmi, 10)
