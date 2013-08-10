#! /usr/bin/env python
# -*- coding: UTF8 -*-
"""
############################################################
Pyndorama - Teste
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
import unittest
#from json import dumps, loads
from webmain import app
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
                return 'adm1n', 0001

        database.DRECORD = _Record(DRECORD)
        self.app = TestApp(app)
        pass

    def test_main(self):
        "retorna o html do memit."
        result = self.app.get('/')
        db = database.DRECORD['adm1n']
        assert 'date'in db, 'no time in %s' % db
        assert result.status == '200 OK'
        assert '<div id="doc_id">adm1n</div>' in result, 'no admin in %s' % result.body
        pass

    def test_lib(self):
        "retorna a biblioteca brython."
        result = self.app.get('/brython.js')
        assert result.status == '200 OK'
        assert 'brython.js www.brython.info' in result, 'no brython in %s' % result.body[:200]
        pass

    def test_meme_py(self):
        "retorna o arquivo meme.py."
        result = self.app.get('/meme.py')
        assert result.status == '200 OK'
        assert 'Memit - Principal' in result, 'no brython in %s' % result.body[:200]
        pass

    def test_post_register(self):
        "registra o cabecalho do teste."
        #result = self.app.post('/record/head',dumps(DRECORD))
        result = self.app.post_json('/record/head', DRECORD)
        assert result.status == '200 OK'
        assert 'it3m' in result, 'no admin in %s' % result.body
        pass

    def test_post_piece(self):
        "registra a colocacao de uma peca."
        record = dict(adm1n=dict(pec=0, cas=0, tem=0))
        result = self.app.post_json('/record/piece', record)
        assert result.status == '200 OK'
        assert 'pec' in result.body, 'no peca in %s' % result.body
        pass

    def test_change_phase(self):
        "registra a mudança de fase."
        record = dict(adm1n=dict(fas=0, pcs=range(9), tem=0))
        result = self.app.post_json('/record/phase', record)
        assert result.status == '200 OK'
        assert 'fas' in result.body, 'no fase in %s' % result.body
        pass

    def test_end_game(self):
        "registra o fim do jogo."
        record = dict(adm1n=dict(fim=0, tem=0))
        result = self.app.post_json('/record/end', record)
        assert result.status == '200 OK'
        assert 'fim' in result.body, 'no end in %s' % result.body
        pass

if __name__ == '__main__':
    unittest.main()
