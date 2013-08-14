#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Time-Web - Main
############################################################

:Author: *Carlo E. T. Oliveira*
:Author: *Erica Nogueira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/08/10
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
from couchdb import Server
#URL ='https://app16304533.heroku:jcwpDKuQWnXmrooAlgBXWnPl@app16304533.heroku.cloudant.com'
URL = "https://app16956802.heroku:TJl26jbJwff5Ks8JpAb8ldt5@app16956802.heroku.cloudant.com"
_DOCBASES = ['keystore']


class Activ(Server):
    "Active database"
    keystore = {}

    def __init__(self, url=URL):
        Server.__init__(self, url)
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
