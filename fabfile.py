# -*- coding: utf-8 -*-
"""
############################################################
Pyndorama - Fabric deployment
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: $Date: 2013/07/16  $
:Status: This is a "work in progress"
:Revision: $Revision: 0.01 $
:Home: `Labase <http://labase.nce.ufrj.br/>`__
:Copyright: ©2013, `GPL <http://is.gd/3Udt>__. 
"""
from BeautifulSoup import BeautifulSoup as soup
from fabric.api import local, settings, cd, run, lcd
from base64 import b64decode as b6d
import mechanize as mcz
from tempfile import mkdtemp
KG_ORIGIN = '/home/carlo/Dropbox/Android/git/pyndorama'
KG_DEST = '/home/carlo/Dropbox/Public/labase/pyndorama'
#KG_DEST = '/tmp/kwarwp'
SOURCES = '*.py'
KSOURCES = 'kuarup.py tchuk.py kuarupfest.py tkinter_factory.py'
KG_IMAGES = '/home/carlo/Dropbox/Android/git/vitallino/src/public/image'
PARTS = '/src/kwarwp.html /src/dropmeme.html /src/*.py /src/public/image/*.* /brython.js /libs/*.js'.split()
DESTS = '/src /src /src /src/public/image / /libs'.split()
def hello():
    print("Hello world!")
PLAT = 'https://activufrj.nce.ufrj.br/'
#PLAT = 'http://localhost:8888/'
def __actdep(paswd):
    _k_copy()
def __actinit(mech,paswd):
    mech.open(PLAT)
    
    mech.select_form(nr=0)
    mech["user"] = "carlo"
    mech["passwd"] = b6d(paswd)
    results = mech.submit().read()
    soup(results)
    print (PLAT+'file/memit/')
def __actup(mech, filename, folder = 'file/%smemit', orig = '/src/', single = None):
    avs = mech.open(PLAT+folder%'').read()
    #filename = 'cavalier.py'
    if filename in avs:
        mech.open(PLAT+folder%'delete/'+ '/' + filename).read()
    avs = mech.open(PLAT+folder%'').read()
    mech.select_form(nr=0)
    mech.add_file(open(KG_ORIGIN + orig + (single or filename)), 'text/plain', filename)
    results = mech.submit().read()
def actdep(paswd="bGFiYXNlNGN0MXY="):
    mech = mcz.Browser()
    __actinit(mech,paswd)
    # filename in 'meme.html memit.py'.split():
    for filename in 'memit.py'.split():
        __actup(mech, filename)
def actfig(paswd):
    mech = mcz.Browser()
    __actinit(mech)
    PHASES = 7
    PIECES = 9
    #self.faces = ['valor.png','beleza.png','conforto.png'] * PHASES
    backs = (['back%02d.jpg'%(phase)
        for phase in range(PHASES)], 'soil.jpg')
    puzzle = (['puzzle%02d.jpg'%(phase)
        for phase in range(PHASES)], 'soil.jpg')
    jigs = (['jigs%02d_%02d.jpg'%(phase,face) for face in range(PIECES)
        for phase in range(PHASES)], 'soil.jpg')
    faces = (['face%02d_%02d.jpg'%(phase,face) for face in [0,1,2]
        for phase in range(PHASES)], 'soil.jpg')
    pieces = (['piece%02d_%02d.png'%(kind,piece)
        for piece in range(PIECES) for kind in [0,1]], 'soil.jpg')
    for finename in faces:
        __actup(mech, filename, folder = 'studio/%smemit', orig = '/src/public/image/')
def ktest():
    local("nosetests")

def _do_copy(source,targ):
    local ("mkdir -p %s"%targ)
    local("cp -u %s -t %s"%(source,targ))

def _nk_copy():
    targ = KG_DEST+'/src'
    _do_copy(KSOURCES,targ)
    targ =  KG_DEST +'/src/public/image'
    _do_copy(KG_IMAGES,targ)
    targ = KG_DEST+'/brython.js'
    _do_copy(KSOURCES,targ)
    targ =  KG_DEST +'/libs'
    _do_copy(KG_IMAGES,targ)

def _k_copy():
    for part, dest in zip(PARTS, DESTS):
        targ, source = KG_DEST + dest, KG_ORIGIN +part
        _do_copy(source, targ)

def kgdep():
    ktest()
    _k_copy()
    #kzip()
