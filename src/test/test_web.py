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
from json import dumps, loads
from webmain import application
from webtest import TestApp
#from webob import Request, Response
import database
from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class TestTime_Web(unittest.TestCase):
    GAMELIST = ['_JPT_game1', '_JPT_game2']

    def setUp(self):
        database.DRECORD = database.Banco(lambda: TinyDB(storage=MemoryStorage))
        database.GRECORD = database.Banco(lambda: TinyDB(storage=MemoryStorage))
        database.GRECORD["j_e_p_p_e_t_o__"] = []
        self.app = TestApp(application)
        pass

    def test_main(self):
        """retorna o html do jeppeto."""
        result = self.app.get('/')
        #db = database.DRECORD['adm1n']
        #assert 'date'in db, 'no time in %s' % db
        assert result.status == '200 OK'
        assert '">umidqualquer</div>' in result.body, 'no admin in %s' % result.body
        pass

    def test_load_empty_game_list(self):
        """recupera lista de games vazia."""
        result = self.app.get('/storage/jeppeto/persist__/j_e_p_p_e_t_o__')
        assert result.status == '200 OK'
        assert ': []' in result.body, 'no empty list value in %s' % result.body

    def test_load_game_list(self):
        """recupera lista de games."""
        result = self._store_game_list()
        result = self.app.get('/storage/jeppeto/persist__/j_e_p_p_e_t_o__')
        assert result.status == '200 OK'
        assert TestTime_Web.GAMELIST[0] in result.body, 'no game in game list: %s' % result.body

    def _store_game_list(self):
        """salva lista de games GAMELIST."""
        data = dict(_xsrf=1234, value=TestTime_Web.GAMELIST)
        return self.app.post_json('/storage/jeppeto/persist__/j_e_p_p_e_t_o__', data)

    def test_store_game_list(self):
        """salva lista de games GAMELIST."""
        data = dict(_xsrf=1234, value=TestTime_Web.GAMELIST)
        result = self._store_game_list()
        assert result.status == '200 OK'
        gamelist = database.GRECORD['j_e_p_p_e_t_o__']
        assert TestTime_Web.GAMELIST[0] in gamelist, 'no games %s in game list: %s' % (result.body, gamelist)


if __name__ == '__main__':
    unittest.main()
