#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Time-Web - Main
############################################################

:Author: *Carlo E. T. Oliveira*
:Author: *Erica Nogueira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/05/24
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from couchdb import Server

_DOCBASES = ['keystore']

class Activ(Server):
    "Active database"
    keystore = {}
    
    def __init__(self, url=None):
        Server.__init__(self)
        act = self
        test_and_create = lambda doc: doc in act and act[doc] or act.create(doc)
        for attribute in _DOCBASES:
            setattr(Activ, attribute, test_and_create(attribute))

    def erase_database(self):
        'erase tables'
        for table in _DOCBASES:
            try:
                del self[table]
            except:
                pass


try:
    __ACTIV = Activ()
    DRECORD = __ACTIV.keystore
except Exception:
    DRECORD = None

