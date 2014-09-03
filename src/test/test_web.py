#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Teste
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/09/02
:Status: This is a "work in progress"
:Revision: 0.1.0
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.
"""
import unittest
#from json import dumps, loads
from webmain import application
from webtest import TestApp
#from webob import Request, Response
import database
ITEM = 'it3m'
ADM, HEA, PEC, PHA, END = 'adm1n head peca fase fim'.split()
DRECORD = dict(adm1n=dict(name=ITEM, item_id=ITEM))
#database.DRECORD = DRECORD


class TestTime_Web(unittest.TestCase):

    def setUp(self):
        class _Record(dict):

            def save(self, arg):
                self['adm1n'].update(arg)
                return 'adm1n'

        database.DRECORD = _Record(DRECORD)
        database.GRECORD = _Record(DRECORD)
        self.app = TestApp(application)
        pass

    def test_main(self):
        "retorna o html do jeppeto."
        result = self.app.get('/')
        #db = database.DRECORD['adm1n']
        #assert 'date'in db, 'no time in %s' % db
        assert result.status == '200 OK'
        assert '">umidqualquer</div>' in result.body, 'no admin in %s' % result.body
        pass

    def _est_lib(self):
        "retorna a biblioteca brython."
        result = self.app.get('/brython.js')
        assert result.status == '200 OK'
        assert 'brython.js www.brython.info' in result, 'no brython in %s' % result.body[:200]
        pass

    def _est_meme_py(self):
        "retorna o arquivo control.py."
        result = self.app.get('/control.py')
        assert result.status == '200 OK'
        assert 'Pyndorama - Principal' in result, 'no brython in %s' % result.body[:200]
        pass

    def _est_post_register(self):
        "registra o cabecalho do teste."
        #result = self.app.post('/record/head',dumps(DRECORD))
        result = self.app.post_json('/storage/jeppeto/persist__/agame', dict(obj=1234))
        assert result.status == '200 OK'
        assert 'OK' in result.body, 'no admin in %s' % result.body
        #assert
        pass

    def _est_post_piece(self):
        "registra a colocacao de uma peca."
        record = dict(adm1n=dict(pec=0, cas=0, tem=0))
        result = self.app.post_json('/record/piece', record)
        assert result.status == '200 OK'
        assert 'pec' in result.body, 'no peca in %s' % result.body
        pass


if __name__ == '__main__':
    unittest.main()
