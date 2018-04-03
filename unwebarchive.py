#!/usr/bin/env python

from sys import argv, exit
from os.path import basename, exists
from types import StringType, IntType, InstanceType, ListType
from subprocess import call, Popen, PIPE
from plistlib import readPlist, Data

fl = []

def url_to_name(url):
    from urllib2 import urlparse
    return basename(urlparse.urlparse(url).path)

def descend_tree(_pl, subcomp='', allCont=False):
    if type(_pl) == ListType:
        pl = {str(x): _pl[x] for x in range(len(_pl)) }
    else:
        pl = _pl

    for t in pl:
        if type(pl[t]) not in [StringType, InstanceType]:
            descend_tree(pl[t], subcomp + '_' + t, allCont=allCont)
            continue

        if t == 'WebResourceData':
            _ext = ''
        elif t == 'WebResourceMIMEType':
            _ext = '.MIMEType'
        elif t == 'WebResourceURL':
            _ext = '.URL'
        elif t == 'WebResourceFrameName':
            _ext = '.FrameName'
        elif t == 'WebResourceTextEncodingName':
            _ext = '.TextEncodingName'
        elif t == 'WebResourceResponse':
            _ext = '.Response'
        else:
            _ext = ''

        if _ext != '' and not allCont:
            continue

        _fname = '%s/%s%s' % (argv[2], subcomp + '_' + t, _ext)
        if 'WebResourceURL' in pl:
            _u = url_to_name(pl['WebResourceURL'])
            _f = '%s/%s' % (argv[2], _u)
            if _f + _ext in fl or exists(_f + '_ext'):
                c = 0
                _tf = '%s_%02d%s' % (_f, c, _ext)
                while _tf in fl or exists(_tf):
                    c+=1
                    _tf = '%s_%02d%s' % (_f, c, _ext)
                _f = _tf
            if len(_u) <= 20:
                fl.append(_f + _ext)
                _fname = _f + _ext

        with open(_fname, "w") as out:
            out.write(pl[t].data if isinstance(pl[t], Data) else pl[t])
            out.close()
        if t == 'WebResourceResponse':
            call(['plutil', '-convert', 'xml1', _fname])

if len(argv) < 4:
    print("Usage: %s infile.webarchive output/path <-d|...>" % (argv[0],))
    exit(1)

p = Popen(['plutil', '-convert', 'xml1', argv[1], '-o', '-'], stdout=PIPE)
pl = readPlist(p.stdout)
#pl = readPlist(argv[1])

descend_tree(pl, basename(argv[1]), argv[3]=='-d')
