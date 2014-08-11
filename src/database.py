#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Main - Pyany branch
############################################################

:Author: *Carlo E. T. Oliveira*
:Author: *Erica Nogueira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/15
:Status: This is a "work in progress"
:Revision: 0.1.1
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from os import environ
#from couchdb import Server

URL = environ.get('CLOUDANT_URL')
_DOCBASES = ['keystore']


class Server:

    def __init__(self, url=URL):
        pass


class Activ(Server):
    """Active database"""
    keystore = {}

    def __init__(self, url=URL):
        Server.__init__(self, url)
        act = self
        """
        test_and_create = lambda doc: doc in act and act[doc] or act.create(doc)
        for attribute in _DOCBASES:
            setattr(Activ, attribute, test_and_create(attribute))
        """

    def erase_database(self):
        """erase tables"""
        for table in _DOCBASES:
            try:
                del self[table]
            except:
                pass


#try:
if True:
    __ACTIV = Activ()
    DRECORD = __ACTIV.keystore
#except Exception:
    #DRECORD = None


if __name__ == "__main__":
    #print([rec for rec in DRECORD])
    recs = {n: rec for n, rec in enumerate(DRECORD)}
    print (recs)
    ques = str(input("apaga?('apaga'/<indice>)"))
    if ques == 'apaga':
        __ACTIV.erase_database()
    elif int(ques) in recs:
        print (DRECORD[recs[int(ques)]])
