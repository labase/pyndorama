# -*- coding: utf-8 -*-
"""
############################################################
Pyndorama - Fabric deployment
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/08/10  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2013, `GPL <http://is.gd/3Udt>__.
"""
from BeautifulSoup import BeautifulSoup as soup
from fabric.api import local  # , settings, cd, run, lcd
from base64 import b64decode as b6d
import mechanize as mcz
import cookielib
import urllib
#from tempfile import mkdtemp
KG_ORIGIN = '/home/carlo/Documentos/dev/pyndorama'
KG_DEST = '/home/carlo/Dropbox/Public/labase/pyndorama'
SOURCES = '*.py'
STORAGE = 'storage/jeppeto/__code__/'
FILES = 'file/%sjeppeto'
FILENAMES = 'index.html control.py model.py visual.py theme.css'.split()
FILESOURCES = '/src /src /src /src /src/view'.split()
PARTS = 'index.html *.py theme.css *.jpg'.split()
DESTS = '/src /src /src/view /src/view/'.split()
PLAT = 'https://activufrj.nce.ufrj.br/'
#PLAT = 'http://localhost:8888/'


def __actdep(paswd):
    _k_copy()


def __actinit(mech, paswd):
    cj = cookielib.LWPCookieJar()
    mech.set_cookiejar(cj)
    mech.open(PLAT)
    mech.select_form(nr=0)
    mech["user"] = "carlo"
    mech["passwd"] = b6d(paswd)
    results = mech.submit().read()
    cookies = mech._ua_handlers['_cookies'].cookiejar
    soup(results)
    xsrf = [ck for ck in cookies if ck.name == '_xsrf'][0]
    print (PLAT+STORAGE, xsrf)
    return xsrf.value


def __actup(mech, filename, folder=FILES, orig='/src/', single=None):
    avs = mech.open(PLAT+folder % '').read()
    #filename = 'cavalier.py'
    if filename in avs:
        mech.open(PLAT+folder % 'delete/'+'/'+filename).read()
    avs = mech.open(PLAT+folder % '').read()
    mech.select_form(nr=0)
    mech.add_file(open(KG_ORIGIN + orig + (single or filename)), 'text/plain', filename)
    mech.submit().read()


def __actsto(mech, filename, xsrf, folder=STORAGE, orig='/src/', single=None):
    file_content = open(KG_ORIGIN + orig + (single or filename))
    data = dict(_xsrf=xsrf, value=file_content)
    data = urllib.urlencode(data)
    avs = mech.open(PLAT+STORAGE+filename, data).read()
    print ('storage result for file %s: ' % filename, avs)


def actdep(paswd):
    mech = mcz.Browser()
    __actinit(mech, paswd)
    # filename in 'meme.html memit.py'.split():
    for filename in 'memit.py'.split():
        __actup(mech, filename)


def actsto(paswd):
    mech = mcz.Browser()
    xsrf = __actinit(mech, paswd.replace('_', '='))
    # filename in 'meme.html memit.py'.split():
    for filename, origin in zip(FILENAMES, FILESOURCES):
        __actsto(mech, filename, xsrf, origin)


def ktest():
    local("nosetests")


def _do_copy(source, targ):
    local("mkdir -p %s" % targ)
    local("cp -u %s -t %s" % (source, targ))


def _k_copy():
    for part, dest in zip(PARTS, DESTS):
        targ, source = KG_DEST + dest, KG_ORIGIN+part
        _do_copy(source, targ)


def kgdep():
    ktest()
    _k_copy()
    #kzip()
